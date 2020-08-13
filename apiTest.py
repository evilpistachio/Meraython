import pprint
import pandas as pd
import numpy as np
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
import requests
from meraki_sdk.exceptions.api_exception import APIException
import getpass

api_key = str(getpass.getpass(prompt='Provide the API key associated with your account: '))
# key: str = api_key
url = "https://api.meraki.com/api/v0/organizations"

headers = {'X-Cisco-Meraki-API-Key': f'{api_key}'}

r = requests.get(url, headers=headers)
pprint.pprint(r.content.decode('utf-8'))
