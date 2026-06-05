# import requests
# from django.utils import timezone
# from django.conf import settings

# def normalize_phone_number(phone_number:str)-> str:
#     # شماره موبایل رو به فرمت اصلی کاوه نگار تبدیل میکند
#     phone_number = str(phone_number).strip().replace('','').replace('-','')

#     if phone_number.startswith('0'):
#         mobile = '98' + phone_number[1:]
#     elif phone_number.startswith('+98'):
#         mobile = phone_number[1:]
#     return mobile


# def send_sms_kavenegar(phone_number:str, message:str, commit:bool=True)-> dict:
#     # ارسال پیامک با استفاده از API کاوه نگار
#     # commit اگر True بود پیامک ارسال میشه 
#     # commit اگر False بود فقط شبیه سازی میشه برای تست


#     if not commit:
#         print(f'SIMULATING SMS to {phone_number}: {message}')
#         return {'success': True, 'result': 'simulated send'}

#     api_key = settings.KAVENEGAR_API_KEY
#     sender = settings.KAVENEGAR_SENDER
#     receptor = normalize_phone_number(phone_number)

#     if not api_key or not sender:
#         print('Kavenegar API_key or Sender Number not configured in settings.')
#         return{'success': False, 'error': 'kavenegar configuration missing.'}


#     if not receptor:
#         print('Invalide Mobile number provided.')
#         return {'success': False, 'error': 'Invalid mobile number.'}

#     url = f'https://api.kavenegar.com/v1/{api_key}/sms/send.json'

#     payload = {
#         'receptor': receptor,
#         'sender': sender,
#         'message': message
#     }

#     try:
#         response = requests.post(url, data=payload, timeout=10)
#         response.raise_for_status()
#         result = response.json

#         # بررسی وضعیت پاسخ API کاوه نگار
#         # اگر به درستی رسیده باشه به کاوه نگار باید status=200 برگردونه
#         if result.get('return', {}).get('status') == 200:
#             print(f'sms send successfuly to {receptor} kavenegar result: {result}')
#             return{'success': True, 'result': result}

#         else:
#             error_message = result.get('return',{}).get('message', 'unknow Error from kavenegar.')
#             print(f'kavenegar API error for {receptor}: {error_message}. full_response: {result}')
#             return{'success': False, 'error': error_message, 'result': result}

#     except requests.exceptions.Timeout:
#         print(f'sms sending time out to {receptor}.')
#         return{'success': False, 'error': 'Request Time out.'}

#     except requests.exceptions.RequestException as e:
#         print(f'An error occurrd during kavenegar request to {receptor}: {e}.')
#         return{'success': False, 'error': str(e)}

#     except Exception as e:
#         print(f'An unexpected error occurrd in send_sms_kavenegar : {e}')
#         return{'success': False, 'error': 'An unexpected error occurrd.'}

# send_sms = send_sms_kavenegar

import requests
from django.utils import timezone
from django.conf import settings

def normalize_phone_number(phone_number: str) -> str | None:
    """
    شماره موبایل را به فرمت استاندارد بین‌المللی (+98...) یا داخلی (98...) تبدیل می‌کند.
    اگر ورودی نامعتبر بود None برمی‌گرداند.
    """
    if not isinstance(phone_number, str):
        phone_number = str(phone_number)

    # حذف فاصله‌ها، خط تیره و هر کاراکتر غیر عددی دیگر
    cleaned_number = ''.join(filter(str.isdigit, phone_number))

    mobile = None  # مقدار پیش‌فرض

    if cleaned_number.startswith('09') and len(cleaned_number) == 11:
        # مثال: 09123456789 -> 989123456789
        mobile = '98' + cleaned_number[1:]
    elif cleaned_number.startswith('9') and len(cleaned_number) == 10:
        # مثال: 9123456789 -> 989123456789
        mobile = '98' + cleaned_number
    elif cleaned_number.startswith('989') and len(cleaned_number) == 12:
        # مثال: 989123456789 -> 989123456789 (بدون تغییر)
        mobile = cleaned_number
    elif cleaned_number.startswith('+989') and len(cleaned_number) == 13:
         # مثال: +989123456789 -> 989123456789 (علامت + حذف می شود)
         mobile = cleaned_number[1:]


    # اگر بعد از تمام تبدیل‌ها، شماره موبایل معتبر نبود
    if mobile is None or not mobile.startswith('989'):
        print(f"Invalid or unnormalizable phone number provided: {phone_number} (cleaned: {cleaned_number})")
        return None # یا می توانید phone_number را برگردانید اگر می خواهید شماره اصلی را نگه دارید

    return mobile


def send_sms_kavenegar(phone_number: str, message: str, commit: bool = True) -> dict:
    """
    ارسال پیامک با استفاده از API کاوه نگار.
    commit: اگر True بود پیامک ارسال می‌شود، در غیر این صورت شبیه‌سازی می‌شود.
    """
    if not commit:
        print(f'SIMULATING SMS to {phone_number}: {message}')
        # شبیه سازی کردن پیامک بدون ارسال واقعی
        return {'success': True, 'result': 'simulated send'}

    api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
    sender = getattr(settings, 'KAVENEGAR_SENDER', None)

    if not api_key or not sender:
        error_msg = 'Kavenegar API_key or Sender Number not configured in settings.'
        print(error_msg)
        return {'success': False, 'error': error_msg}

    receptor = normalize_phone_number(phone_number)

    if not receptor:
        error_msg = f'Invalid Mobile number provided: {phone_number}'
        print(error_msg)
        return {'success': False, 'error': error_msg}

    url = f'https://api.kavenegar.com/v1/{api_key}/sms/send.json'

    payload = {
        'receptor': receptor,
        'sender': sender,
        'message': message
    }

    try:
        # استفاده از session برای مدیریت بهتر connection ها
        session = requests.Session()
        response = session.post(url, data=payload, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        result_json = response.json() # پارس کردن JSON response

        # بررسی وضعیت پاسخ API کاوه نگار
        # Status code 200 از سمت API کاوه نگار به معنی موفقیت در دریافت درخواست است
        # وضعیت ارسال واقعی پیامک در فیلد 'status' برمیگردد
        
        # به نظر میرسد منظور از result.get('return', {}).get('status') == 200
        # چک کردن وضعیت کلی پاسخ JSON از کاوه نگار است، نه وضعیت ارسال پیامک
        # برای وضعیت ارسال پیامک باید به کلید 'entries' و سپس 'status' در response نگاه کرد.
        # اما برای سادگی، فرض می کنیم response['return']['status'] == 200 نشانه موفقیت کلی است.

        if result_json and 'return' in result_json and result_json['return'].get('status') == 200:
            print(f'SMS sent successfully to {receptor}. Kavenegar result: {result_json}')
            return {'success': True, 'result': result_json}
        else:
            # استخراج پیام خطا از پاسخ کاوه نگار

            error_message = result_json.get('return', {}).get('message', 'Unknown Error from Kavenegar.')
            print(f'Kavenegar API error for {receptor}: {error_message}. Full response: {result_json}')
            return {'success': False, 'error': error_message, 'result': result_json}

    except requests.exceptions.Timeout:
        error_msg = f'SMS sending timed out to {receptor}.'
        print(error_msg)
        return {'success': False, 'error': error_msg}

    except requests.exceptions.RequestException as e:
        # این شامل خطاهای HTTP (مانند 4xx, 5xx) و خطاهای دیگر اتصال می شود
        error_msg = f'An error occurred during Kavenegar request to {receptor}: {e}.'
        print(error_msg)
        # اگر response وجود داشت، سعی می کنیم پیام خطا را استخراج کنیم
        error_details = getattr(e, 'response', None)
        if error_details is not None:
            try:
                error_json = error_details.json()
                error_msg += f" Response: {error_json}"
            except:
                error_msg += f" Response Text: {error_details.text}"
        return {'success': False, 'error': error_msg}

    except Exception as e:
        # گرفتن خطاهای پیش بینی نشده دیگر
        error_msg = f'An unexpected error occurred in send_sms_kavenegar: {e}.'
        print(error_msg)
        return {'success': False, 'error': 'An unexpected error occurred.'}

# تعیین تابع اصلی برای ارسال اس ام اس
send_sms = send_sms_kavenegar