#!/usr/bin/env python

# Please feel free to donaate BTC: 3J5PCTwHEBWpT6VB7aTB75qPiWFzixd56o or ZCR: ZKy4JoAp7H8cuYbPcDsVYpgKZpg4unnJWe
# Fork based on:
# https://github.com/gkovacs/remove_miner_fees

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import nfqueue
from scapy.all import *
import os
import re

from os import path

# DO NOT CHANGE FOR LYRA2Z PORT --dport 20012. THIS IS PORT OF CryptoDredge MINING FEE POOL
os.system('iptables -A OUTPUT -p tcp --dport YOUR_MINING_POOL_PORT -j NFQUEUE --queue-num 0')

# Change my_address to YOUR_MINING_ADDRESS.WORKER_NAME and my_pws TO_YOUR_LYRA2Z_COIN_PASSWORD
my_address = 'ZVyFZghscHfmHnEjG2GBVNJBZRcQRam5XW.nini'
my_pws = 'c=ZCR'

addresses_to_redirect = [re.compile(re.escape(x.lower()), re.IGNORECASE) for x in [
  # DO NOT CHANGE THIS ADDRESS. THIS IS MINING FEE ADDRESS OF CryptoDredge 0.11.0 TO LYRA2Z GIN COIN
  #This is ex-address to stratum.gos.cx pool!    'GLwc1FaCzMewtSZCovXDCQgMVw1LhGQECS' 
  'GWA2V7FewZNb49CBDd9yDnZBp8Hddko7h9'
]]
pwss_to_redirect = [re.compile(re.escape(x.lower()), re.IGNORECASE) for x in [
  # DO NOT CHANGE THIS, THIS IS MINING FEE AUTHORIZATION FOR MINING FEE ADDRESS ON GOS.CX POOL
        'd=32,c=GIN'
]]
logfile = open('remove_mining_fees_log.txt', 'w', 0)

def callback(arg1, payload):
  data = payload.get_data()
  pkt = IP(data)

  payload_before = len(pkt[TCP].payload)

  payload_text = str(pkt[TCP].payload)
  for address_to_redirect in addresses_to_redirect:
    payload_text = address_to_redirect.sub(my_address, payload_text)

  for pws_to_redirect in pwss_to_redirect:
    payload_text = pws_to_redirect.sub(my_pws, payload_text)

  pkt[TCP].payload = payload_text

  payload_after = len(payload_text)

  payload_dif = payload_after - payload_before

  pkt[IP].len = pkt[IP].len + payload_dif

  pkt[IP].ttl = 40

  del pkt[IP].chksum
  del pkt[TCP].chksum
  payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(pkt), len(pkt))
  logfile.write(payload_text)
  logfile.write('\n')
  logfile.flush()
def main():
  q = nfqueue.queue()
  q.open()
  q.bind(socket.AF_INET)
  q.set_callback(callback)
  q.create_queue(0)
  try:
    q.try_run() # Main loop
  except KeyboardInterrupt:
    q.unbind(socket.AF_INET)
    q.close()
    if path.exists('./restart_iptables'):
      os.system('./restart_iptables')

main()
