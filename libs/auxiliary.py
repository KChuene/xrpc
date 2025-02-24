import sys
from libs.colors import Color, Colors as _

clr = Color.color

# Program termination function
def bye(endmsg = f"({clr('i')}) Terminating...", showusg=True):
	print(endmsg)
	if showusg:
		print("\nUsage:\n\t xrpc.py -s http://server.com [-dbg]")
          
	sys.exit()

# Command line arguments parsing
def readargs(opt : str, args : list[str], required=True, isbool : bool = False, isnum : bool = False):
    if not opt in args:
        if required:
            bye(f"({clr('!')}) Option {opt} is required.")
        else:
            return None

    elif isbool:
        return True
    
    indexof = args.index(opt)
    if indexof >= len(args)-1:
        bye(f"({clr('!')}) Value expected for option {opt}.")
    
    valueof = args[indexof + 1]
    if isnum and valueof.isnumeric():
        return int(valueof)
    
    elif isnum:
        bye(f"({clr('!')}) Number expected for option {opt}.")

    return valueof

# Numerical string (int, float, negative) check
def isnumber(n_str:str, allow_negative=True, intonly: bool = False):
    if not (n_str or n_str.strip()): 
        return False 

    if intonly: return n_str.removeprefix("-").isnumeric()

    dotcount = indexof = 0
    for c in n_str:
        # Allowed chars are '-' and '.' in specific positions
        if c=="-":
            if indexof!=0 or not allow_negative:
                return False
        elif c==".":
            if indexof in (0, len(n_str)-1) or dotcount > 0:
                return False
            dotcount += 1

        elif not c.isnumeric():
            return False
        indexof += 1
    return True

# Type converter
def ctype(svalue: str):
    if svalue.isnumeric(): return int(svalue)
    elif isnumber(svalue, allow_negative=True, intonly=True): return int(svalue)
    elif isnumber(svalue): return float(svalue)
    elif svalue.lower() in ("true", "false"): return svalue.lower() == "true"
    return svalue