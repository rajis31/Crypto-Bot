from coinbase.wallet.client import Client
import config
import json
import http.client
import csv
from datetime import datetime as dt
import hmac
import hashlib
import pprint

client = Client(config.api_key, config.api_secret)
print(client)

# Coinbase Auth class 
class Auth():
    def __init__(self, API_KEY, API_SECRET, PASSPHRASE=""):
        self.API_KEY    = API_KEY
        self.API_SECRET = API_SECRET
        self.PASSPHRASE = PASSPHRASE

    def generate(self,method, path, body=""):
        timestamp = dt.now().strftime('%s')
        message   = timestamp + method + path + body
        signature = hmac.new(self.API_SECRET.encode(),
                             message.encode('utf-8'),
                             digestmod=hashlib.sha256)
        signature_hex = signature.hexdigest()

        
        headers = {}
        headers["CB-ACCESS-KEY"]        = self.API_KEY
        headers["CB-ACCESS-SIGN"]       = signature_hex
        headers["CB-ACCESS-TIMESTAMP"]  = timestamp
        headers["CB-ACCESS-PASSPHRASE"] = self.PASSPHRASE      
        headers["Content-Type"]         = 'application/json'
        return headers
    
# Get list of accounts
accounts = client.get_accounts()
assert isinstance(accounts.data, list)
print(accounts)
print(accounts.keys())

for account in accounts.data:
    print("Currency: {}, Amount: {}".format(account.currency, account.balance.amount))
    
# for account in accounts.data:
#     print(account.get_transactions())

# User info 
print(client.get_auth_info())

# Products 
conn    = http.client.HTTPSConnection("api.coinbase.com")
auth    = Auth(config.api_key,config.api_secret,"")
headers = auth.generate(method="GET",path="/api/v3/brokerage/products")
payload = ''
print(headers)

try: 
    conn.request("GET", "/api/v3/brokerage/products", payload, headers)
    res    = conn.getresponse()
    data   = json.loads(res.read().decode("utf-8"))
    print(type(data))
    print(len(data))
    print(data.keys())
    print(data["products"][0])
    
    
    
except Exception as x:
    print(x) 
    
conn.close()