from libs.colors import Color

# cmd: [args, description, validator]
index = {
    "paramlst": [None, "List all fixed parameters set.", lambda args: len(args) == 0],

    "paramadd": ["<number> <name> <value>", 
            "Set a global parameter for procedure calls",
            lambda args: len(args) == 3 and args[0].isnumeric()],

    "paramdel": ["<number>", 
                 "Paremter to remove from set of fixed parameters.",
                lambda args: len(args) == 1 and args[0].isnumeric()],

    "paramrst": [None, "Clear all global parameter or a specific parameter",
                lambda args: len(args) == 0],

    "lock": ["<call name>", 
            "Useful if you don't want to specify the function to call, all the time",
            lambda args: len(args) == 1],

    "unlock": [None, "Clear the locked call",
            lambda args: len(args) == 0],

    "join": [None,
            "Treat input as one string (ignore spaces), usefule for locked calls that requre long strings as parameters",
            lambda args: len(args) == 0],
    
    "split": [None, "Undo the effect of 'join'",
            lambda args: len(args) == 0],

    "prefix": ["<prefix_str>", "String to add as a prefix to subsequent rpc calls. Useful for wordpress ('wp.') xml rpc calls.",
            lambda args: len(args) == 1],

    "suffix": ["<suffix_str>", "String to add as a suffix to subsequent rpc calls.",
            lambda args: len(args) == 1],

    "help": ["[<command>]", "Show help.", lambda args: len(args) <= 1]
} 

clr = Color.color

def sepfor(cmd : str):
    # Compute output separator by taking the length of the longest command as a base
    return f"{' '*(8 - len(cmd) + 1)}- "

# Format command help
def oformat(cmd : str, descr: str):
    # Compute output separator by taking the length of the longest command as a base
    return f"{cmd}{' '*(8 - len(cmd) + 1)} - {descr}"

# Return command validator
def vdator(cmd: str):
    return index[cmd][2] if cmd in index else lambda _ = None: False

# Show help for a specific command
def show(cmd : str = None, msg=None):
    if cmd and not cmd in index:
        print(f"({clr('!')}) Unrecognized subsystem command.")
        return

    info = index[cmd]
    outmsg = msg or info[1]

    print(f"{outmsg}\n")
    print("Usage:")
    print(f"\t{cmd}", info[0] or "\x00")

# Show help for all commands
def showall():
    print('\n'.join([
        oformat(key, index[key][1]) 
        for key in index
    ]))
    # for key in index:
    #     info = index[key]
    #     print(key, info[0] if len(info) < 2 else info[1], sep=sepfor(key))