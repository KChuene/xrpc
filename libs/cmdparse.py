import shlex
from libs.auxiliary import ctype

class CmdParams:
    def __init__(self):
        self.params = {}

    # Range and Presence check of pos (parameter position)
    def inrange(self, pos: int, pcheck: bool=False):
        if pos == None or pos < 1:
            return False
        
        return pos in self.params if pcheck else True
            
    # Add a new fixed parameter
    def add(self, pos: int, name: str, val: str):
        if self.inrange(pos): 
            self.params[pos] = [name, val]

    # Remove an set fixed parameter
    def remove(self, pos: int):
        if self.inrange(pos, pcheck=True): 
            del self.params[pos]

    # Clear all fixed parameters
    def removeall(self):
        self.params.clear()

    # Show set fixed parameters
    def list(self):
        # 1: name = value
        keys = sorted(self.params.keys())
        print("\n".join(
            f"{kelem}: {' = '.join([str(pelem) for pelem in self.params[kelem]])}" 
            for kelem in keys
        ))

class CmdParser:
    config = {
       "prefix": "", "lock": "", "base":"",
       "suffix": "",
       "params": {},
       "split": True
    }

    # Method for subsystem commands (ie. lock, set-param)
    def reset(self, spec: dict):
        CmdParser.config.update({
            elem: spec[elem] for elem in spec if elem in CmdParser.config
        })

    # from [var, var, var] and [fixed, fixed] build [fixed, var, var, fixed, var]
    def joinp(self, vparams: list[str], fparams: dict[list]):
        fmaxpos, vlength = max(fparams or [0]), len(vparams)

        length = fmaxpos if fmaxpos > vlength else vlength 
        result = []
        for elem in range(1, length + 1):
            fflag, vflag = elem in fparams, elem <= vlength
            
            if fflag: result.append(fparams[elem][1])
            if vflag: result.append(vparams[elem - 1])
            
            if not (fflag or vflag): 
                result.append("")                
        return result

    # Read command and arguments from commandline input string
    # making appropriate type conversions
    def read(self, cmdstr: str):
        config = CmdParser.config
        if not config['split']:
            return [cmdstr] # all strings
        
        return [
            ctype(elem) 
            for elem in shlex.split(cmdstr)
        ]

    # Method for RPC commands; result is (cmd, [params]) fit for cmd(*params) call
    def parse(self, cmdin: list[str], fparams: dict[list]):
        config = CmdParser.config
        config['base'] = cmdin[0] if not config['lock'] else ""

        command = f"{config['prefix']}{config['lock']}"
        command = f"{command}{config['base']}"
        command = f"{command}{config['suffix']}"

        pstart = 1 if not config['lock'] else 0
        params = self.joinp(cmdin[pstart:] if config['split'] else [' '.join(cmdin[pstart:])], fparams)
        return command, params