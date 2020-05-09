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


atom_miner_url = requests.get('https://api.atomminer.com/pool/pools')
atom_miner_data = json.loads(atom_miner_url.text)
for element in atom_miner_data['result']:
    if element['name'] == 'Denarius':
        atom_miner_workers = element['miners']
        atom_miner_hashrate = float(element['hashrate_raw']) / 1000000000
        atom_miner_block = float(element['height'])
        break


data = [
  {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": grafanatime,
              "fields": {
                  "atomworkers" : atom_miner_workers,
                  "atomhashrate" : atom_miner_hashrate,
                  "atomheight" : atom_miner_block
              }
          }
        ]
        # Send the JSON data to InfluxDB
client.write_points(data)
        # Wait until it's time to query again...
