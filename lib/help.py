index = {
    "param": ["<number> <value>", 
              "Set a global parameter for procedure calls"],

    "paramrst": ["[<number>]", "Clear all global parameter or a specific parameter"],

    "lock": ["<call name>", 
             "Useful if you don't want to specify the function to call, all the time"],

    "unlock": ["Clear the locked call"],

    "join": ["Treat input as one string (ignore spaces), usefule for locked calls that requre long strings as parameters"],
    
    "split": ["Undo the effect of 'join'"],

    "disc": ["<path/to/wordlist> <delay>", 
             "Run the simple bruteforcer (error-based) to discover hidden function calls"]
} 

def sepfor(cmd : str):
    # Compute output separator by taking the length of the longest command as a base
    return f"{' '*(8 - len(cmd) + 1)}- "

def help(cmd : str = None, msg=None):
    if cmd and not cmd in index:
        print("Unrecognized subsystem command.")
        return

    info = index[cmd]
    outmsg = msg

    if not outmsg:
        outmsg = info[0] if len(info) < 2 else info[1]

    print(f"{outmsg}\n")
    print("Usage:")
    print(f"\t{cmd}", info[0] if len(info) == 2 else "\x00")

def helpall():
    for key in index:
        info = index[key]
        print(key, info[0] if len(info) < 2 else info[1], sep=sepfor(key))