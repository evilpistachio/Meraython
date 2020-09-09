import requests
import pprint
import pandas as pd
import json

STORES_USERNAME = input("Username: \n")
STORES_PASSWORD = input("Password: \n")
OTP = input("VIP Access: \n")
Bearer = input("Credential ID (SYMC12345678) - \n")
Auth_URL = "https://secretServerURL/SecretServer/oauth2/token"
DATA = {"username": f"{STORES_USERNAME}",
        "password": f"{STORES_PASSWORD}",
        "grant_type": "password",
        "domain": "stores",
        "OTP": f"{OTP}"}

headers = {
  'Authorization': "Bearer" + f"{Bearer}",
  'Content-Type': 'application/x-www-form-urlencoded'}

pprint.pprint(headers)

access_token_request = requests.post(url=Auth_URL, headers=headers, data=DATA, verify=False)
token1 = json.loads(access_token_request.text)
access_token1 = pd.DataFrame(token1, index=token1)
token = access_token1['access_token'][0]

selected_secret_id = input("Which Secret would you like to retrieve? - Please input Secret ID - '1234' for example\n ")

URL = f'https://secretServerURL/SecretServer/api/v1/secrets/{selected_secret_id}/fields/APIkey'
HEADERS = {'Authorization': "Bearer" + " " + f"{token}"}
payload = {}
response = requests.get(url=URL, headers=HEADERS, verify=False, data=payload)
print(json.loads(response.text))
