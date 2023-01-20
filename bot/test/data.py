from coinbase.wallet.client import Client
import config
import json
import http.client
import csv
from datetime import datetime as dt
from datetime import timedelta
import hmac
import hashlib
from pprint import pprint
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column,String, Integer, Float, create_engine, DateTime


BASE = declarative_base()

# Coinbase API Auth Class
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

# DB functions 
def connect():
    username  = config.db_username
    password = config.db_password
    db       = config.db
    host     = config.db_host
    url      = f"mysql+pymysql://{username}:{password}@{host}/{db}"
    con      = create_engine(url)
    return con
    
    
# Define Models
class OHLC(BASE):
    __tablename__="ohlc"
    id         = Column(Integer, primary_key=True) 
    created_at = Column(DateTime)
    symbol     = Column(String)
    time       = Column(Integer)
    low        = Column(Float(precision=2))
    high       = Column(Float(precision=2))
    open       = Column(Float(precision=2))
    close      = Column(Float(precision=2))
    volume     = Column(Integer)
    

# Data Gathering Functions 
def get_ohlc_data(symbol="BTC-USD", 
                  granularity=3600, 
                  start=int(dt.now().timestamp())-3600, 
                  end=int(dt.now().timestamp())):
    
    conn    = http.client.HTTPSConnection("api.exchange.coinbase.com")
    auth    = Auth(config.api_key,config.api_secret,"")
    path    = f"/products/{symbol}/candles?granularity={granularity}"
    headers = auth.generate(method="GET",path=path)
    payload = ''
    
    
    try: 
        conn.request("GET", f"/products/{symbol}/candles?granularity=3600&start={start}&end={end}", payload, headers)
        res    = conn.getresponse()
        data   = json.loads(res.read().decode("utf-8"))
        return data
       
    except Exception as x:
        print(x) 
        
    conn.close()

# Data Storing 
def store_ohlc_data(symbol, data):
    engine  = connect()
    session = Session(engine)
    
    try:
        if data:
            for datum in data: 
                time       = datum[0]
                low        = datum[1]
                high       = datum[2]
                open       = datum[3]
                close      = datum[4]
                volume     = datum[5]
                created_at = dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
                
                ohlc = OHLC(symbol=symbol, 
                            created_at = created_at,
                            time=time, 
                            low = low, 
                            high = high, 
                            open = open, 
                            close = close, 
                            volume = volume)
                session.add(ohlc)
                session.commit()
                
            session.flush()
            session.close()
            engine.dispose()
    except:
        print("Could not store market data.")


data = get_ohlc_data()
store_ohlc_data(symbol="BTC-USD", data=data)
