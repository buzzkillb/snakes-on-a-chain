import time
import sys
import datetime
import urllib
import json
import requests
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "127.0.0.1" # My Ubuntu VPS
port = 8086 # default port
user = "admin" # the user/password created for the VPS influxDB database, with write access
password = "admin" 
dbname = "coingecko_ogre_btc" # the database we created earlier
interval = 60 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# think of measurement as a SQL table, it's not...but...
measurement = "measurement"
# location will be used as a grouping tag later
blockchain = "denarius"

ts = int(time.time())
print(ts)
grafanatime=ts * 1000000000
print(grafanatime)

coingecko_ogre_url = requests.get('https://api.coingecko.com/api/v3/coins/denarius/tickers?exchange_ids=trade_ogre')
coingecko_ogre_data = json.loads(coingecko_ogre_url.text)
coingecko_ogre_price = coingecko_ogre_data['tickers']

for r in coingecko_ogre_price:
    if r['target'] == 'BTC':
        ogre_last_btc = float(r['last'])
        print format(ogre_last_btc, '0.8f')
        ogre_volume_btc = float(r['volume'])
        print format(ogre_volume_btc, '0.8f')
        ogre_converted_last_btc_btc = float(r['converted_last']['btc'])
        print format(ogre_converted_last_btc_btc, '0.8f')
        ogre_converted_last_btc_eth = float(r['converted_last']['eth'])
        print format(ogre_converted_last_btc_eth, '0.8f')
        ogre_converted_last_btc_usd = float(r['converted_last']['usd'])
        print format(ogre_converted_last_btc_usd, '0.8f')
        ogre_converted_volume_btc_btc = float(r['converted_volume']['btc'])
        print format(ogre_converted_volume_btc_btc, '0.8f')
        ogre_converted_volume_btc_eth = float(r['converted_volume']['eth'])
        print format(ogre_converted_last_btc_eth, '0.8f')
        ogre_converted_last_btc_usd = float(r['converted_last']['usd'])
        print format(ogre_converted_last_btc_usd, '0.8f')
        ogre_converted_volume_btc_btc = float(r['converted_volume']['btc'])
        print format(ogre_converted_volume_btc_btc, '0.8f')
        ogre_converted_volume_btc_eth = float(r['converted_volume']['eth'])
        print format(ogre_converted_volume_btc_eth, '0.8f')
        ogre_converted_volume_btc_usd = float(r['converted_volume']['usd'])
        print format(ogre_converted_volume_btc_usd, '0.8f')

data = [
  {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": grafanatime,
              "fields": {
                  "ogre_last_btc" : ogre_last_btc,
                  "ogre_volume_btc" : ogre_volume_btc,
                  "ogre_converted_last_btc_btc" : ogre_converted_last_btc_btc,
                  "ogre_converted_last_btc_eth" : ogre_converted_last_btc_eth,
                  "ogre_converted_last_btc_usd" : ogre_converted_last_btc_usd,
                  "ogre_converted_volume_btc_btc" : ogre_converted_volume_btc_btc,
                  "ogre_converted_volume_btc_eth" : ogre_converted_volume_btc_eth,
                  "ogre_converted_volume_btc_usd" : ogre_converted_volume_btc_usd
              }
          }
        ]
        # Send the JSON data to InfluxDB
client.write_points(data)
        # Wait until it's time to query again...
