# ibus_proxy
Forward IBUS (not to be confused with some Linux IBUS technology, please) streaming data to multiple destinations.
This layer is needed because IBUS servers are not plug-n-play. This layer provides plug-n-play for downstream consumers.

## Installation
```
pip install git+https://github.com/TwistTRL/ibus-proxy
```
This will install the script, ibus-proxy.py in to your $PATH.

## Usage:
```
ibus-proxy.py <inHost> <inPort> <outHost> <outPort>
```
Only one client can connect to inHost:inPort. Multiple clients can connect to outHost:outPort, to consume the stream.
Usually, keep inHost nad outHost the same, unless you have multiple network interfaces and you know what you are doing. 

## Possible missing features
* ssl and encryption
* authentication
