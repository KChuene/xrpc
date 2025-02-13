import sys
from libs.colors import Color, Colors as _

clr = Color.color

def bye(endmsg = f"({clr('i')}) Terminating...", showusg=True):
	print(endmsg)
	if showusg:
		print("\nUsage:\n\t xrpc.py -s http://server.com")
          
	sys.exit()

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

def isnumber(n_str):
    for c in n_str:
        # Allowed chars are '-' and '.' in specific positions
        indx_of = n_str.index(c)
        if c=="-" and indx_of!=0:
            return False

        elif c=="." and (indx_of==0 or indx_of==len(n_str)-1):
            return False

        elif c=="." or c==".":
            continue # Is exceptional char and in right pos

        # Other char
        if not c.isnumeric():
            return False

    return True