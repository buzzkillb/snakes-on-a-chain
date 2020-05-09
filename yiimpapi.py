from denariusrpc.authproxy import AuthServiceProxy, JSONRPCException

import time
import sys
import datetime
import urllib
import json
import requests
from influxdb import InfluxDBClient

# rpc_user and rpc_password are set in the denarius.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:32369"%("rpcuser", "rpcpassword"))

# Configure InfluxDB connection variables
host = "127.0.0.1" # My Ubuntu server
port = 8086 # default port
user = "admin" # the user/password created, with write access
password = "admin" 
dbname = "pools" # the database we created earlier
interval = 60 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# think of measurement as a SQL table, it's not...but...
measurement = "measurement"
# location will be used as a grouping tag later
blockchain = "denarius"

#iso = time.ctime()
blockcount = rpc_connection.getblockcount()
block = rpc_connection.getblockbynumber(blockcount)
grafanatime = block['time'] * 1000000000


#zergpool
#zergpool_url = requests.get('http://api.zergpool.com:8080/api/currencies')
#zergpool_data = json.loads(zergpool_url.text)
#zergpool_workers = zergpool_data['D']['workers']
#zergpool_hashrate = float(zergpool_data['D']['hashrate']) / 1000000000

#bsod
#bsod_url = requests.get('http://api.bsod.pw/api/currencies')
#bsod_data = json.loads(bsod_url.text)
#bsod_workers = bsod_data['D']['workers']
#bsod_hashrate = float(bsod_data['D']['hashrate']) / 1000000000

cafe_url = requests.get('http://mining.cafe/api/currencies')
cafe_data = json.loads(cafe_url.text)
cafe_workers = cafe_data['D']['workers']
cafe_hashrate = float(cafe_data['D']['hashrate']) / 1000000000
cafe_block = float(cafe_data['D']['height'])

data = [
  {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": grafanatime,
              "fields": {
                  "ycafeworkers" : cafe_workers,
                  "ycafehashrate" : cafe_hashrate,
                  "ycafeheight" : cafe_block
              }
          }
        ]
        # Send the JSON data to InfluxDB
client.write_points(data)
        # Wait until it's time to query again...
