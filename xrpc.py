#!/bin/python3
import sys
import os
import shlex
import xmlrpc.client as xc
import libs.help as help

from urllib.parse import urlparse
from libs.cmdparse import CmdParams, CmdParser
from libs.colors import Color, Colors as _
from libs.run import Run
from libs.auxiliary import *

fixed_params = {}
discoverer = None # Additional module to run bruteforcing
global_call = None
split_input = True
prefix, prefixall = None, None
suffix, suffixall = None, None
url = "http://127.0.0.1:8000"

cmdparams = CmdParams()
cmdparser = CmdParser()

clr = Color.color

def parse_cmd(cmdstr):
   argv = shlex.split(cmdstr)
   if not argv:
      return None, []

   elif len(argv)==1:
      return argv[0], []

   elif not split_input:
      return argv[0], [' '.join(argv[1:])]

   # Type conversion before returning
   for indx in range(0, len(argv)):
      if isnumber(argv[indx]):
         argv[indx] = int(argv[indx]) if argv[indx].isnumeric() else float(argv[indx]) # int() if whole number else float()

   return argv[0], argv[1:]

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

def apply_wrap(cmdstr : str):
   return f"{prefixall or ''}{prefix or ''}{cmdstr}{suffix or ''}{suffixall or ''}".strip()

def show_help(cmd):
   help.help(cmd[0]) if len(cmd)>0 and cmd[0].strip() else help.helpall()

def conf(cmdstr):
    args = shlex.split(cmdstr)
    config = {
        "param": set_param, "paramrst": rst_param,
        "lock": lock_call, "unlock": unlock_call,
        "join": lambda _=None: set_split_input(False), "split": lambda _=None: set_split_input(True),
        "help": show_help,
        "prefix-cmd": lambda value: string_wrap(preppend= value), "prefix": lambda value: string_wrap(preppendall= value),
        "suffix": lambda value: string_wrap(append= value), "suffix-cmd": lambda value: string_wrap(appendall= value)
    }

    if args[0] in config:
        config[args[0]](args[1:])
    else:
        print(f"({clr('!')}) Unrecognized subsystem command.")

def configure(cmdstr):
    args = shlex.split(cmdstr)
    config = {
        "paramlst": lambda _ = None: cmdparams.list(),
        "paramadd": lambda p, n, v: cmdparams.add(int(p), n, v), 
        "paramdel": lambda p: cmdparams.remove(int(p)),
        "paramrst": lambda _ = None: cmdparams.removeall(),
        "lock": lambda v: cmdparser.reset({"lock": v}), 
        "unlock": lambda _ = None: cmdparser.reset({"lock": ""}),
        "join": lambda _ = None: cmdparser.reset({"split": False}), 
        "split": lambda _ = None: cmdparser.reset({"split": True}),
        "help": lambda c = None: help.show(c) if c and c.strip() else help.showall(),
        "prefix": lambda v: cmdparser.reset({"prefix": v}),
        "suffix": lambda v: cmdparser.reset({"suffix": v})
    }

    isvalid = help.vdator(args[0])(args[1:])
    if not isvalid:
        print(f"({clr('!')}) Invalid command or arguments.")
    else:
       config[args[0]](*args[1:])
       
def shell(cmdstr):
   os.system(cmdstr)

def main():
    host = urlparse(url).netloc
    htag = f" @ {clr(host, fgcolor=_.MAGENTA)}" if host else ""
    cmdstr = input(f"{clr('xrpc')}{htag} ({global_call})~$ " if global_call else f"{clr('xrpc')}{htag} ~$ ").strip()
    
    if cmdstr.startswith("! "):
        shell(cmdstr[2:])

    elif cmdstr.startswith(": "):
        configure(cmdstr[2:])

    elif cmdstr:
        #cmd, args = parse_cmd(f"{global_call} {cmdstr}" if global_call else cmdstr) # Prefix global call
        cmdlst = cmdparser.read(cmdstr)
        cmd, args = cmdparser.parse(cmdlst, cmdparams.params)
        #args = join_fixed_to_varargs(args)

        run = getattr(proxy, cmd)
        print(wrapper(run, args))

sys.argv.append("-s")
sys.argv.append("https://digital.va.gov/xmlrpc.php")
sys.argv.append("-dbg")
arguments = sys.argv
if __name__=="__main__":
   Color.setdefault(_.MAGENTA)
   Color.mapfg(['!', 'Error', 'i', 'xrpc'], [_.RED, _.RED, _.BLUE, _.BLUE])
   url = readargs("-s", arguments)
   dbg = readargs("-dbg", arguments, required=False, isbool=True)

   proxy = xc.ServerProxy(url)
   print(f"Target: {url}")

   Run.reg([xc.Fault, OSError, Exception])
   while True:
        Run.run(main).onerror(
            KeyboardInterrupt,
            bye, ("\nCtrl-C", False)
        ).onerror(
            None,
            print, (f"Error: {Run.error}"),
            debug=bool(dbg)
        )

