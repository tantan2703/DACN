from django.shortcuts import render

def thanks(request):
    return render(request, 'Musical/thanks.html')

# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import requests
import hmac
import hashlib

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def momo_payment(request):
    if request.method == 'POST':
        endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
        partnerCode = "MOMO"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        orderInfo = "pay with MoMo"
        redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
        ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
        amount = "50000"
        orderId = "8b65d471-a66b-471f-a67b-008c7a31280c"
        requestId = "c0e28e49-a99e-4f0d-8fb7-7aa2ef54b1ea"
        requestType = "captureWallet"
        extraData = ""  # pass empty value or Encode base64 JsonString

        # Tạo chữ ký
        rawSignature = (
            f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}"
            f"&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}"
            f"&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
        )
        h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
        signature = h.hexdigest()

        # Dữ liệu gửi đi
        momo_data = {
            'partnerCode': partnerCode,
            'partnerName': "Test",
            'storeId': "MomoTestStore",
            'requestId': requestId,
            'amount': amount,
            'orderId': orderId,
            'orderInfo': orderInfo,
            'redirectUrl': redirectUrl,
            'ipnUrl': ipnUrl,
            'lang': "vi",
            'extraData': extraData,
            'requestType': requestType,
            'signature': signature
        }

        # In ra JSON request
        print("--------------------JSON REQUEST----------------")
        print(json.dumps(momo_data, indent=4))

        # Gửi HTTP POST request tới endpoint của MoMo
        momo_url = "https://test-payment.momo.vn/v2/gateway/api/create"
        headers = {'CONTENT_TYPE': 'application/json'}
        response = requests.post(momo_url, json=momo_data, headers=headers)

        # Xử lý kết quả và trả về
        result = response.json()
        pay_url = result.get('payUrl', '')

        # In ra JSON response
        print("--------------------JSON RESPONSE----------------")
        print(json.dumps(result, indent=4))

        return JsonResponse({'payUrl': pay_url})
    else:
        return JsonResponse({'error': 'Invalid request method'})

