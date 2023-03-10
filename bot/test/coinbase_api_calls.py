from coinbase.wallet.client import Client
import config
import json
import http.client
import csv
from datetime import datetime as dt
import hmac
import hashlib
from pprint import pprint

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
        headers["User-Agent"]           = "Something"         
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
#pprint(client.get_auth_info())

# Transactions 
#pprint(accounts)
#pprint(client.get_transactions( "4585aff9-e099-59b0-906f-3802bfc4d99f"))

# All methods in client object 
pprint(dir(client))

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

# OHLC Data
# pprint(client.get_exchange_rates())
# pprint(client.get_historic_prices())
print("OHLC Data")
conn    = http.client.HTTPSConnection("api.exchange.coinbase.com")
auth    = Auth(config.api_key,config.api_secret,"")
headers = auth.generate(method="GET",path="/products/BTC-USD/candles?granularity=3600")
payload =''

try: 
    now = int(dt.now().timestamp())-10000
    print(now)
    conn.request("GET", f"/products/BTC-USD/candles?granularity=3600&start={now}", payload, headers)
    res    = conn.getresponse()
    data   = json.loads(res.read().decode("utf-8"))
    pprint(data)
    
    #time   = bucket start time
    #low    = lowest price during the bucket interval
    #high   = highest price during the bucket interval
    #open   = opening price (first trade) in the bucket interval
    #close  = closing price (last trade) in the bucket interval
    #volume = volume of trading activity during the bucket interval
    
except Exception as x:
    print(x) 
    
conn.close()