def join_fixed_to_varargs(argv):
   # from [var, var, var] and [fixed, fixed] build [fixed, var, var, fixed, var]
   # place fixed at their positions and fill the gaps with var
   length = len(fixed_params or []) + len(argv or [])
   if fixed_params and length < max(fixed_params):
      print(f"({clr('!')}) Insufficient params. Expecting {max(fixed_params) - length} more to join with fixed params.")
      return argv

   result = []
   curr_argv_index = 0
   for param in range(1, length+1):
      if param in fixed_params:
         result.append(fixed_params[param])
      else:
         result.append(argv[curr_argv_index])
         curr_argv_index += 1

   return result

def wrapper(func, args):
   if func and args:
      print(f"Function: {func}({args})")
      return func(*args)
   
   elif func:
      print(f"Function: {func}")
      return func()

def list_fixed_params():
   param_nums = list(fixed_params.keys())
   param_nums.sort()
   for param in param_nums:
      print(f"{param}: {fixed_params[param]}")

def set_param(argv):
   global fixed_params
   if len(argv) == 0:
      list_fixed_params()
      return
   elif len(argv) < 2:
      help.help("param", f"({clr('!')}) Both parameter number and value are required.")
      return

   if not argv[0].isnumeric():
      print(f"({clr('!')}) Invalid parameter number.")
      return

   param = int(argv[0])
   if param > 0 and param < 10:
      if isnumber(argv[1]):
         fixed_params[param] = int(argv[1]) if argv[1].isnumeric() else float(argv[1])
      else:
         fixed_params[param] = argv[1]

def rst_param(argv):
   global fixed_params
   if not argv:
      fixed_params.clear()
      return
   
   if not argv[0].isnumeric():
      print(f"({clr('!')}) Invalid parameter number.")
      return
   
   elif not int(argv[0]) in fixed_params:
      return
   
   fixed_params.pop(int(argv[0]), None)

def lock_call(argv):
   if len(argv) < 1:
      help.help("lock", f"({clr('!')}) Expected function name")
      return

   global global_call
   global_call = argv[0]

def unlock_call(_ = None):
   global global_call
   global_call = None

def set_split_input(status):
   global split_input
   split_input = status
   print(f"split => {split_input}")

def string_wrap(preppend : str = None, preppendall : str = None, append : str = None, appendall : str = None):
   global prefix, prefixall
   global suffix, suffixall
   
   prefix = preppend if preppend and preppend.strip() else None
   prefixall = preppendall if preppendall and preppendall.strip() else None
   suffix = append if append and append.strip() else None
   suffixall = appendall if appendall and appendall.strip() else None

fixed_params = {}
global_call = None
split_input = True
prefix, prefixall = None, None
suffix, suffixall = None, None

class CmdParams:
    def __init__(self):
        self.params = []

    def inrange(self, pos: int):
        return pos != None and pos > 1 and pos <= len(self.params)
            
    @inrange
    def add(self, pos: int, name: str, val: str):
        if self.inrange(pos): self.params[pos or len(self.params) - 1] = {name: val}

    def remove(self, pos: int):
        if self.inrange(pos): self.params.remove(self.params[pos or len(self.params) - 1])

class CmdParser:
    config = {
       "prefix": "",
       "lock": "",
       "base":"",
       "params": {},
       "suffix": "",
       "split": False
    }

    # Method for subsystem commands (ie. lock, set-param)
    def reset(spec: dict):
        for elem in spec: 
            CmdParser.config[elem] = spec[elem]

    # from [var, var, var] and [fixed, fixed] build [fixed, var, var, fixed, var]
    def joinp(vparams: list[str]):
        fparams = CmdParser.config['params']
        fmaxpos, vlength = max(fparams), len(vparams)

        length = fmaxpos if fmaxpos > vlength else vlength 
        result = []
        for elem in range(1, length + 1):
            if elem in fparams:
                result.append(fparams[elem - 1])

            elif elem <= vlength:
                result.append(vparams[elem - 1])
            else: 
                result.append("")                
        return result

    # Method for RPC commands; result is (cmd, [params]) fit for cmd(*params) call
    def parse(self, cmdin: list[str]):
        config = CmdParser.config
        config['base'] = cmdin[0]

        command = f"{config['prefix']}{config['lock']}"
        command += config['base']

        params = self.joinp(cmdin[1:] if config['split'] else [' '.join(cmdin[1:])])
        params += config['suffix']
        return command, params