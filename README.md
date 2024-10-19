# xrpc
A wrapper script for the xmlrpc.client python module. Focus on making calls with a terminal like feel, treating functions as commands, and additionally 
allows issuing os commands to the local host directly.

## Options
1. `-host` - The remote host to issue RPC calls to.
2. `-p`    - The port to connect to on the remote host.

The target is then interpreted as 'http://{host}:{p}/'.

## Use example
```
./xrpc.py -host 127.0.0.1 -p 8000
```
```
cmd > g
Function: <xmlrpc.client._Method object at 0x7f96831b7890>
Great day!
cmd > h sam wilson
Function: <xmlrpc.client._Method object at 0x7f9682282dd0>(['sam', 'wilson'])
Hello, sam wilson.
cmd > ! head -n 5 ./xrpc.py
#!/bin/python3
import sys
import requests as req
import os
from xmlrpc.client import ServerProxy
cmd > 
```


