from denariusrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the denarius.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:32369"%("rpcuser", "rpcpassword"))

# test connection and get current block
get_block_count = rpc_connection.getblockcount()
print(get_block_count)

def main():
  last_block = -1
  while True:

    block = rpc_connection.getblockcount()

    if block != last_block:
      print('latest block ' ,block)
      last_block = block

main()
