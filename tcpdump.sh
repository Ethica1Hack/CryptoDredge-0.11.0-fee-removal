# Start with SUDO permissions
# Find your network interface code with command in terminal: ifconfig
# This will dump traffic of mining fee to file mining_activiti_gos_cx.txt if you keep setting for mining GIN coin on gos.cx pool
# Only vaild for Lyra2z coins of CryptoDredge v0.11.0 miner
# If you are mining other Lyra2z coin ( ZCoin or simillar ), you need to preroute and forward tcp traffic with iptables, 
# otherwise CryptoDredge miner will continue witn mining fee connection to gos.cx pool !
tcpdump -i YOUR_NETWORK_INTERFACE -vv host stratum.gos.cx -X > mining_activity_gos_cx.txt
