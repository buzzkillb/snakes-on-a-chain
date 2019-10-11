from denariusrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the denarius.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:32369"%("rpcusername", "rpcpassword"))
get_fortunastake_info = rpc_connection.fortunastake('list', 'full')
print(get_fortunastake_info)
import time
import sys
import datetime
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "127.0.0.1" # My Ubuntu NUC
port = 8086 # default port
user = "admin" # the user/password created for the pi, with write access
password = "admin" 
dbname = "chain" # the database we created earlier
interval = 60 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# think of measurement as a SQL table, it's not...but...
measurement = "measurement"
# location will be used as a grouping tag later
blockchain = "denarius"

# Run until you get a ctrl^c
def main():
  import time
  last_block = -1
  while True:
    block = rpc_connection.getblockcount()
    getblockhash = rpc_connection.getblockchaininfo()
    bestblockhash = str(getblockhash['bestblockhash'])
    moneysupply = int(getblockhash['moneysupply'])
# put blockhash from latest block and get extra info
    getblockhashinfo = rpc_connection.getblock(bestblockhash)
    blockhashinfowork = str(getblockhashinfo['flags'])
    blockhashinfotime = int(getblockhashinfo['time'])
# fortunastake info
    fortunastakeinfo = rpc_connection.fortunastake('count')
    fortunastakecount = fortunastakeinfo
    iso = time.ctime()
        # Print for debugging, uncomment the below line
        # print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity)) 
        # Create the JSON data structure
    if block != last_block:
      print "latest block:", (block)
      data = [
        {
          "measurement": measurement,
              "tags": {
                  "blockchain": blockchain,
              },
              "time": iso,
              "fields": {
                  "block" : block,
                  "timestamp" : blockhashinfotime,
                  "work" : blockhashinfowork,
                  "bestblockhash" : bestblockhash,
                  "moneysupply" : moneysupply,
                  "fortunastakes" : fortunastakecount
              }
          }
        ]
        # Send the JSON data to InfluxDB
      client.write_points(data)
        # Wait until it's time to query again...

      last_block = block
#        time.sleep(interval)
main()
