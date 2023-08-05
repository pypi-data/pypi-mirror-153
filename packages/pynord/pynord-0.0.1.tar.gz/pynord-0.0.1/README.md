# pynord
A Python library for NordVPN.
# Installation
```
pip install pynord
```
# Usage
```
from pynord import PyNord

nordvpn = PyNord(verbose=True)

# get VPN connection status (returns True/False)
nordvpn.status()

# connecting to a random server
nordvpn.connect()

# connecting to a specific server
nordvpn.connect(server='us8538')

# disconnecting from NordVPN
nordvpn.disconnect()

# toggling NordVPN killswitch feature (prevents unprotected internet access)
nordvpn.killswitch(toggle=True)
```







