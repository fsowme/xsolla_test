import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

# xsolla
MERCHANT_ID = int(os.getenv('MERCHANT_ID'))
PROJECT_ID = int(os.getenv('PROJECT_ID'))
API_KEY = os.getenv('API_KEY')
TOKEN_URL = f'https://api.xsolla.com/merchant/v2/merchants/{MERCHANT_ID}/token'
SECRET_KEY = os.getenv('SECRET_KEY')

# player data
USER_ID = os.getenv('USER_ID')
USER_EMAIL = os.getenv('EMAIL')

# purchase data
PURCHASE_AMOUNT = float(os.getenv('AMOUNT'))
PURCHASE_CURRENCY = os.getenv('CURRENCY')


def get_token():
    auth = HTTPBasicAuth(MERCHANT_ID, API_KEY)
    get_token_data = {
        'user': {
            'id': {'value': USER_ID},
            'email': {'value': USER_EMAIL}
        },
        'settings': {
            'project_id': PROJECT_ID,
            'mode': 'sandbox'
        },
        'purchase': {
            'checkout': {'amount': PURCHASE_AMOUNT, 'currency': PURCHASE_CURRENCY}
        }
    }
    response_data = requests.post(TOKEN_URL, json=get_token_data, auth=auth).json()
    return response_data['token']
