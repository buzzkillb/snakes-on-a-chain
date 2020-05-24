# crontab -e
# * * * * * $(which python) /home/denarius/python/coingecko_southxchange_btc.py >> ~/cron.log 2>&1

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
user = "admin" # the user/password created for the VPS, with write access
password = "admin" 
dbname = "coingecko_southxchange_btc" # the database we created earlier
interval = 60 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# think of measurement as a SQL table, it's not...but...
measurement = "measurement"
# location will be used as a grouping tag later
blockchain = "denarius"

# Get current epochtime
ts = int(time.time())
print(ts)
# Convert epochtime to what Grafana appears to want
grafanatime=ts * 1000000000
print(grafanatime)

coingecko_southx_url = requests.get('https://api.coingecko.com/api/v3/coins/denarius/tickers?exchange_ids=south_xchange')
coingecko_southx_data = json.loads(coingecko_southx_url.text)
coingecko_southx_price = coingecko_southx_data['tickers']

for r in coingecko_southx_price:
    if r['target'] == 'BTC':
        southx_last_btc = float(r['last'])
        print format(southx_last_btc, '0.8f')
        southx_volume_btc = float(r['volume'])
	print format(southx_volume_btc, '0.8f')
	southx_converted_last_btc_btc = float(r['converted_last']['btc'])
	print format(southx_converted_last_btc_btc, '0.8f')
        southx_converted_last_btc_eth = float(r['converted_last']['eth'])
        print format(southx_converted_last_btc_eth, '0.8f')
        southx_converted_last_btc_usd = float(r['converted_last']['usd'])
        print format(southx_converted_last_btc_usd, '0.8f')
        southx_converted_volume_btc_btc = float(r['converted_volume']['btc'])
        print format(southx_converted_volume_btc_btc, '0.8f')
        southx_converted_volume_btc_eth = float(r['converted_volume']['eth'])
        print format(southx_converted_volume_btc_eth, '0.8f')
        southx_converted_volume_btc_usd = float(r['converted_volume']['usd'])
        print format(southx_converted_volume_btc_usd, '0.8f')
        
data = [
  {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": grafanatime,
              "fields": {
                  "southx_last_btc" : southx_last_btc,
                  "southx_volume_btc" : southx_volume_btc,
                  "southx_converted_last_btc_btc" : southx_converted_last_btc_btc,
                  "southx_converted_last_btc_eth" : southx_converted_last_btc_eth,
                  "southx_converted_last_btc_usd" : southx_converted_last_btc_usd,
                  "southx_converted_volume_btc_btc" : southx_converted_volume_btc_btc,
                  "southx_converted_volume_btc_eth" : southx_converted_volume_btc_eth,
                  "southx_converted_volume_btc_usd" : southx_converted_volume_btc_usd
              }
          }
        ]
        # Send the JSON data to InfluxDB
client.write_points(data)
        # Wait until it's time to query again...
