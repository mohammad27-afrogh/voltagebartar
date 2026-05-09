import pytest
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from decimal import Decimal
from datetime import timedelta

from products.models import Product, Discount, Comment

@pytest.mark.django_db
def test_product_creation_success(product_instance, category, brand, features):
    assert product_instance.category == category
    assert product_instance.features == features
    assert product_instance.brand == brand

    assert product_instance.product_type == 'SEED'
    assert product_instance.commodity_status == 'AVA'
    assert product_instance.name == 'Rose_Seedling'

    assert product_instance.base_price == Decimal('15000.00')
    assert str(product_instance) == 'Rose_Seedling'

@pytest.mark.django_db
def test_product_creation_with_missing_optional_fields(category, features):
    product =  Product.objects.create(
        name = 'only Required Fields',
        slug = 'only_req',
        category = category,
        features = features,
        inventory = 10,
        base_price = '15000.00',
        product_type = 'FER',
        short_description = 'minimal',
    )
    assert product.brand is None
    assert product.successful_sales_count == 0

@pytest.mark.django_db
def test_product_final_price_on_discount(product_instance):
    assert product_instance.final_price == Decimal('15000.00')

@pytest.mark.django_db
def test_product_final_price_whit_active_discount(product_instance):

    Discount.objects.create(
        product = product_instance,
        discount_percentage  = Decimal('30.00'),
        start_date = timezone.now().date(),
        end_date = timezone.now().date(),
    )
    expected_price = Decimal('10500.00')

    assert product_instance.final_price == expected_price

@pytest.mark.django_db
def test_product_final_price_with_expired_discount(product_instance):
    yesterday = timezone.now().date() - timedelta(days=1)

    Discount.objects.create(
        product = product_instance,
        discount_percentage = Decimal('15000.00'),
        start_date = yesterday,
        end_date = yesterday,
    )

    assert product_instance.final_price == Decimal('15000.00')

@pytest.mark.django_db
def test_final_price_select_best_discount(product_instance):
    Discount.objects.create(
        product = product_instance,
        discount_percentage = Decimal('30.00'),
        start_date = timezone.now().date(),
        end_date = timezone.now().date(),
    )
    Discount.objects.create(
        product=product_instance,
        discount_percentage = Decimal('20.00'),
        start_date=timezone.now().date(),
        end_date=timezone.now().date(),
    )
    Discount.objects.create(
        product=product_instance,
        discount_percentage = Decimal('10.00'),
        start_date=timezone.now().date(),
        end_date=timezone.now().date(),
    )
    expected_price = Decimal('10500.00')

    assert product_instance.final_price == expected_price

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username = 'tester',
        password = 'password123',
        email = 'user@test.com'
    )

@pytest.mark.django_db
def test_product_comment_creation(product_instance, user):
    comment = Comment.objects.create(
        product = product_instance,
        user = user,
        body_comment = 'Gret Product fast shipping'
    )

    assert comment.product == product_instance
    assert comment.user == user
    assert product_instance.comments.count() == 1
    assert product_instance.get_absolute_url() == f'/products/{product_instance.slug}/'
