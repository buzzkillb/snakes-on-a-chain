#from denariusrpc.authproxy import AuthServiceProxy, JSONRPCException

import time
import sys
import datetime
import urllib
import json
import requests
from influxdb import InfluxDBClient

# rpc_user and rpc_password are set in the denarius.conf file
#rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:32369"%("rpcuser", "rpcpassword"))

# Configure InfluxDB connection variables
host = "127.0.0.1" # My Ubuntu NUC
port = 8086 # default port
user = "admin" # the user/password created
password = "admin" 
dbname = "chainz_stakes" # the database we created earlier
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

#chainz stakes
staking = json.loads(requests.get("https://chainz.cryptoid.info/explorer/index.stakes.dws?coin=d").text)
circulating = json.loads(requests.get("https://chainz.cryptoid.info/d/api.dws?q=circulating").text)

staking_remove_junk = json.dumps(staking).replace('null', '0')
staking_removed = json.loads(staking_remove_junk)
#print(staking_removed)

#print(response)
stakes = staking_removed['stakes']
#print(stakes)

#stakes = list(filter(None, stakes_list))
#print(stakes)
#print (stakes[0]['amount'])

sum=0
for x in stakes:

  #print(x['amount'])
  staking_amount= float(x['amount'])

  #print(staking_amount)
  sum = sum + staking_amount

print(sum)
print(circulating)
percent_staking = (sum / circulating) * 100
print(percent_staking)



data = [
  {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": grafanatime,
              "fields": {
                  "sum" : sum,
                  "circulating" : circulating,
                  "percent_staking" : percent_staking
              }
          }
        ]
        # Send the JSON data to InfluxDB
client.write_points(data)
        # Wait until it's time to query again...
