import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.test import Client
from django.conf import settings
import json


@pytest.fixture
def client():
    return Client()


authority_value_test = 'A000000000011111111112222222222333333'


@pytest.mark.django_db
def test_payment_process_success(order, client):
    authority_value = authority_value_test
    # محاسبه قیمت
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    mock_response_payload = {
        'data': {
            'code': 100,
            'message': 'OK',
            'authority': authority_value,
            'fee_type': 'Merchant',
            'fee': rial_total_price,
        },
        'errors': None,
    }

    # شبیه سازی پاسخ زرین پال
    mock_zarinpal_response = MagicMock()
    mock_zarinpal_response.status_code = 200
    mock_zarinpal_response.json.return_value = mock_response_payload
    mock_zarinpal_response.raise_for_status.return_value = None
    
    # ساخت url برای ویوی پرداخت
    url = reverse('payment:payment_process')

    session = client.session
    session['order_id'] = str(order.id)
    session.save()

    with patch('requests.post', return_value=mock_zarinpal_response) as mock_post:
        response = client.get(url)

    # بررسی پاسخ
    assert response.status_code == 302

    # بررسی url redirect شده
    redirect_url = response.url
    assert 'https://payment.zarinpal.com/pg/StartPay/' in redirect_url
    assert authority_value in redirect_url

    # در دیتابیس authority اطمینان از ذخیره 
    order.refresh_from_db()
    assert order.zarinpal_authority == authority_value
    assert order.status == 'PEN'

    mock_post.assert_called_once()


@pytest.mark.django_db
def test_payment_callback_success(order, client):
    # آماده سازی داده ها
    authority_value = authority_value_test
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    order.zarinpal_authority = authority_value
    order.save()

    # پاسخ مورد انتظار زرین پال برای تایید پرداخت موفق
    mock_verify_response_payload = {
        'data': {
            'code': 100,
            'message': 'OK',
            'ref_id': 'A000000000099999999998888888888777777',
            'fee_type': 'Merchant',
            'fee': rial_total_price,
        },
        'errors': None,
    }

    mock_verify_response = MagicMock()
    mock_verify_response.status_code = 200
    mock_verify_response.json.return_value = mock_verify_response_payload

    # ساخت url callback  با پارامترهای صحیح
    callback_url = reverse('payment:payment_callback') + f'?authority={authority_value}&status=OK'

    with patch('payment.views.requests.post', return_value=mock_verify_response) as mock_post:
        response = client.get(callback_url)

        # بررسی نتایج
        assert response.status_code == 302
        assert response.url.startswith(reverse('payment:custom_success'))

        mock_post.assert_called_once()
        call_args, call_kwargs = mock_post.call_args

        assert call_kwargs['url'] == 'https://payment.zarinpal.com/pg/v4/payment/verify.json'

        sent_data = json.loads(call_kwargs['data'])
        assert sent_data['merchant_id'] == settings.ZARINPAL_MERCHANT_ID
        assert sent_data['amount'] == rial_total_price
        assert sent_data['authority'] == authority_value

        # چک کردن headers
        assert call_kwargs['headers']['accept'] == 'application/json'
        assert call_kwargs['headers']['content-type'] == 'application/json'

        order.refresh_from_db()
        # چک کردن آپدیت سفارش در دیتابیس
        assert order.is_paid is True
        assert order.zarinpal_ref_id == 'A000000000099999999998888888888777777'
        assert order.zarinpal_payment_code == '100'
