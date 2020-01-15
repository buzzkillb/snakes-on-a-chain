from denariusrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the denarius.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:32369"%("RPCUSER", "RPCPASS"))
import time
import sys
import datetime
import urllib
import json
import requests
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "127.0.0.1" # My Ubuntu NUC
port = 8086 # default port
user = "adminusername" # the user/password created for the pi, with write access
password = "adminpassword" 
dbname = "powend" # the database we created earlier
interval = 60 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# Enter the sensor details
#sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = "measurement"
# location will be used as a grouping tag later
blockchain = "denarius"

import time
denariuswinurl = "https://pos.watch/win.json"
response = urllib.urlopen(denariuswinurl)
windata = json.loads(response.read())
averageblocktime = float(windata['blocktime'])
print (averageblocktime)

powend = 3000000
# get latest block count
block = rpc_connection.getblockcount()
blocksleft = powend - block
timeleftsec = blocksleft * averageblocktime
timeleftminutes = timeleftsec / 60
timelefthours = timeleftminutes / 60
timeleftdays = timelefthours / 24

# put blockhash from latest block and get extra info
getblockhash = rpc_connection.getblockchaininfo()
bestblockhash = str(getblockhash['bestblockhash'])
getblockhashinfo = rpc_connection.getblock(bestblockhash)
blockhashinfowork = str(getblockhashinfo['flags'])
blockhashinfotime = int(getblockhashinfo['time']) * 1000000000


print (powend)
print (block)
print (blocksleft)
print (timeleftsec)
print (timeleftminutes)
print (timelefthours)
print (timeleftdays)

from datetime import datetime, timedelta
pewpew = datetime.now()
pewpew += timedelta(seconds=timeleftsec)
powend = str(pewpew)
print (powend)

data = [
  {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": blockhashinfotime,
              "fields": {
                  "block" : block,
                  "timestamp" : blockhashinfotime,
                  "powend" : powend,
                  "averageblocktime" : averageblocktime
              }
          }
        ]
        # Send the JSON data to InfluxDB
client.write_points(data)
        # Wait until it's time to query again...
