import requests
from django.utils import timezone
from django.conf import settings

def normalize_phone_number(phone_number:str)-> str:
    # شماره موبایل رو به فرمت اصلی کاوه نگار تبدیل میکند
    phone_number = str(phone_number).strip().replace('','').replace('-','')

    if phone_number.startswith('0'):
        mobile = '98' + phone_number[1:]
    elif phone_number.startswith('+98'):
        mobile = phone_number[1:]
    return mobile


def send_sms_kavenegar(phone_number:str, message:str, commit:bool=True)-> dict:
    # ارسال پیامک با استفاده از API کاوه نگار
    # commit اگر True بود پیامک ارسال میشه 
    # commit اگر False بود فقط شبیه سازی میشه برای تست


    if not commit:
        print(f'SIMULATING SMS to {phone_number}: {message}')
        return {'success': True, 'result': 'simulated send'}

    api_key = settings.KAVENEGAR_API_KEY
    sender = settings.KAVENEGAR_SENDER
    receptor = normalize_phone_number(phone_number)

    if not api_key or not sender:
        print('Kavenegar API_key or Sender Number not configured in settings.')
        return{'success': False, 'error': 'kavenegar configuration missing.'}


    if not receptor:
        print('Invalide Mobile number provided.')
        return {'success': False, 'error': 'Invalid mobile number.'}

    url = f'https://api.kavenegar.com/v1/{api_key}/sms/send.json'

    payload = {
        'receptor': receptor,
        'sender': sender,
        'message': message
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        result = response.json

        # بررسی وضعیت پاسخ API کاوه نگار
        # اگر به درستی رسیده باشه به کاوه نگار باید status=200 برگردونه
        if result.get('return', {}).get('status') == 200:
            print(f'sms send successfuly to {receptor} kavenegar result: {result}')
            return{'success': True, 'result': result}

        else:
            error_message = result.get('return',{}).get('message', 'unknow Error from kavenegar.')
            print(f'kavenegar API error for {receptor}: {error_message}. full_response: {result}')
            return{'success': False, 'error': error_message, 'result': result}

    except requests.exceptions.Timeout:
        print(f'sms sending time out to {receptor}.')
        return{'success': False, 'error': 'Request Time out.'}

    except requests.exceptions.RequestException as e:
        print(f'An error occurrd during kavenegar request to {receptor}: {e}.')
        return{'success': False, 'error': str(e)}

    except Exception as e:
        print(f'An unexpected error occurrd in send_sms_kavenegar : {e}')
        return{'success': False, 'error': 'An unexpected error occurrd.'}

send_sms = send_sms_kavenegar