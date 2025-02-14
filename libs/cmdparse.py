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

fixed_params = {}
global_call = None
split_input = True
prefix, prefixall = None, None
suffix, suffixall = None, None

class CmdParams:
    def __init__(self):
        self.params = {}

    def inrange(self, pos: int):
        return pos != None and 1 < pos <= len(self.params)
            
    def add(self, pos: int, name: str, val: str):
        if self.inrange(pos): self.params[pos or len(self.params) - 1] = [name, val]

    def remove(self, pos: int):
        if self.inrange(pos): del self.params[pos or len(self.params) - 1]

    def removeall(self):
        self.params.clear()

    def list(self):
        # 1: name = value
        keys = sorted(self.params.keys())
        print("\n".join(
            f"{elem}: {' = '.join(self.params[elem])}" 
            for elem in keys
        ))

class CmdParser:
    config = {
       "prefix": "", "lock": "", "base":"",
       "suffix": "",
       "params": {},
       "split": False
    }

    # Method for subsystem commands (ie. lock, set-param)
    def reset(spec: dict):
        CmdParser.config.update({
            elem: spec[elem] for elem in spec if elem in CmdParser.config
        })

    # from [var, var, var] and [fixed, fixed] build [fixed, var, var, fixed, var]
    def joinp(vparams: list[str], fparams: dict[list]):
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
    def parse(self, cmdin: list[str], fparams: dict[list]):
        config = CmdParser.config
        config['base'] = cmdin[0]

        command = f"{config['prefix']}{config['lock']}"
        command += config['base']
        command += config['suffix']

        params = self.joinp(cmdin[1:] if config['split'] else [' '.join(cmdin[1:])], fparams)
        return command, params