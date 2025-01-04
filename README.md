# XRPC - XML Remote Procedure Call
A wrapper script for the xmlrpc.client python module providing command-line like interaction with xml rpc servers. Inclueds some sub-commands for ease of use and 
a lite bruteforcer for discovering rpc functions.

## Structure
- `libs`: The help module and discovery (bruteforcing) module.
- `wordlists`: Wordlists for use in discovery, initially includes `big.txt` a randomly picked off sample.

## Usage
To start xrpc run the following command:
```
python3 xrpc.py -host 127.0.0.1 -p 8000
```

> **Hint:**
> The `-host` option must be an IPv4 address, no names.


Procedure calls are made normally, that is the name of the procedure followed by it's parameters (space separated). But to run commands <br>
- `: `: Colon-space, precedes commands that difined within the script, like `help` and `join`.
- `! `: Exclamation-space, precedes system commands to (linux, windows, etc.).

## Examples
**list script commands**
```
: help
```
```
param    - Set a global parameter for procedure calls
paramrst - Clear all global parameter or a specific parameter
lock     - Useful if you don't want to specify the function to call, all the time
unlock   - Clear the locked call
join     - Treat input as one string (ignore spaces), usefule for locked calls that requre long strings as parameters
split    - Undo the effect of 'join'
disc     - Run the simple bruteforcer (error-based) to discover hidden function calls
```

**get help for specific command**
```
: help disc
```
```
Run the simple bruteforcer (error-based) to discover hidden function calls

Usage:
        disc <path/to/wordlist> <delay>
```

**run discovery module**
```
: disc wordlists/big.txt 1
```
```
< Discovering wordlists\big.txt delay by 1 >
g (6/58)
shell (24/58)
```

**run os command**
```
! python --version
```
```
Python 3.11.9
```

**make procudure call**
```
xrpc> g
```
```
Function: <xmlrpc.client._Method object at 0x0000020AE732D6D0>
Great day!
```
