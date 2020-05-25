# snakes-on-a-chain
![Imgur Image](https://i.imgur.com/7pgCRBV.png)

Denarius Python RPC Daemon scripts  
For python denarius RPC use https://github.com/buzzkillb/python-denariusrpc  
sample site using grafana and influxdb https://denarius.pro  
guide to setting up Denarius Python RPC, influxdb, grafana and putting current block height in the dashboard.  
https://blockforums.org/topic/334-crypto-stats-using-grafana-influxdb-denarius-daemon/  
guide to setting up to read Coingecko API  
https://blockforums.org/topic/377-setting-up-grafana-and-influxdb-docker-containers-and-showing-some-apis-stats/

#### python blockcount.py  
```
2491056
('latest block ', 2491056)
('latest block ', 2491057)
('latest block ', 2491058)
```
#### python blockdata.py  
```
latest block: 2491411
epoch: 1570730014
converted time: 2019-10-10 10:53:34
bestblockhash: 0000000000069e7d25de16bd3c2b244e0edf66e4191820a3345f458577c65179
Type of Work: proof-of-work
circulating: 6415473.59282623
Fortunastakes: 357
last block delta: 1570730014  seconds
latest block: 2491412
epoch: 1570730090
converted time: 2019-10-10 10:54:50
bestblockhash: 99888746101dd3e798790fee574cc4d5dfa78496e76834328acc69730f349725
Type of Work: proof-of-stake
circulating: 6415473.60071664
Fortunastakes: 357
last block delta: 76  seconds
latest block: 2491413
epoch: 1570730108
converted time: 2019-10-10 10:55:08
bestblockhash: 86acf0fa67f798d32fb3706f317f47750f96b4dab01f3a1ec92608390baab16e
Type of Work: proof-of-stake
circulating: 6415473.60679883
Fortunastakes: 357
last block delta: 18  seconds
```  
#### python fswinner.py  
```
Winner of block 2524048 is DTaV7aXwUHNdACLTWmMJytu3ZsNqbB2VKV
Winner of block 2524049 is D9XwyKehex5mC6cqgpBSUngHoDna3EoUD6
Winner of block 2524050 is D5PaAPbNugjfHNnH6MbJKUWozBMRiL1N8q
Winner of block 2524051 is DFjpnJLXEBDDCucffShyoYUQpQ7FTypHpx
Winner of block 2524052 is DQ45tg4wnpRSJFWLnZecp5FfXXkQWUVtd4
Winner of block 2524053 is DRMbq6mZre8J4gdLA1xGetr3gpG2e6uyBo
Winner of block 2524054 is DAPGJ29kJYJyuXpE2ATGd6QPkwKUe9c9Eb
Winner of block 2524055 is DGGrUsauDK3j1W4cdYFPxAZMPo8gfyucNB
Winner of block 2524056 is D8jugMuwjk5ihzAyqfyrK7GuFS4sGeRu5x
Winner of block 2524057 is D5tuxvswmzHtoms2r76XaVSs3Kc58H4xiQ
```
#### Docker Setup 
Create a data directory and also a userid to use for the grafana Docker container  
```
mkdir data # creates a folder for your data
ID=$(id -u) # saves your user id in the ID variable
```
Docker run command with some environmental variables  
```
docker run -d \
-p 3000:3000 \
--name=grafana \
--user $ID \
--volume "$PWD/data:/var/lib/grafana" \
-e "GF_INSTALL_PLUGINS=grafana-worldmap-panel" \
-e "GF_USERS_VIEWERS_CAN_EDIT=false" \
-e "GF_USERS_EDITORS_CAN_ADMIN=false" \
-e "GF_USERS_ALLOW_SIGN_UP=false" \
-e "GF_USERS_ALLOW_ORG_CREATE=false" \
-e "GF_AUTH_DISABLE_LOGIN_FORM=false" \
-e "GF_AUTH_ANONYMOUS_ENABLED=true" \
-e "GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer" \
-e "GF_ANALYTICS_GOOGLE_ANALYTICS_UA_ID=UA-157676508-1" \
-e "GF_SERVER_DOMAIN=denarius.pro" \
grafana/grafana
```
Check this is up by going to your IP:3000  
Docker run command  
```
--name="influxdb" \
-p 8086:8086 \
-v /home/USERNAME/influxdb:/var/lib/influxdb \
influxdb -config /etc/influxdb/influxdb.conf
```
To get into influxdb Docker container
```
docker exec -it influxdb /bin/bash
```
To get into influx cli  
```
influx
```
then run commands like  
```
show databases
create database stats
drop database stats
```
Check its all working  
```
docker stop grafana
docker stop influxdb
docker start grafana
docker start influxdb
docker stop grafana
docker rm grafana
rerun the full grafana run command
```
