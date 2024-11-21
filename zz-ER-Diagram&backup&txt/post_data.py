import requests

url = 'http://127.0.0.1:8000/order/orders/'
headers = {
    'Content-Type': 'application/json',
    # 'Authorization': 'Token your_token_here'  # Include if authentication is required
}
data = {
    "user_profile": 3,
    "status": "pending",
    "total_amount": 1100.0,
    "shipping_address": 5,
    "order_items": [
        {
            "variant_id": 3,
            "quantity": 11,
            "price": 200.0
        }
    ]
}

try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Will raise an HTTPError for bad responses
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.HTTPError as err:
    print("HTTP error occurred:", err)
except requests.exceptions.ConnectionError as err:
    print("Connection error occurred:", err)
except requests.exceptions.Timeout as err:
    print("Timeout error occurred:", err)
except requests.exceptions.RequestException as err:
    print("An error occurred:", err)
    
# python test-code.py