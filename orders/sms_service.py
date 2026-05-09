import requests

def send_sms_to_number_users(numbers, message):
    results = []

    for number in numbers:
        #واقعی پنل پیامکی رو باید وارد کنیم API اینجا 
        response = requests.post(
            "آدرس sms",
            json={
                'to': number,
                message: message,
            },
            timeout=10
        )

        results.append({
            'number': number,
            'status_code': response.status_code,
            'success': response.ok,
            'response': response.text,
        })

    return results