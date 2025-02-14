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

def parse_cmd(cmd_str):
   argv = shlex.split(cmd_str)
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

def configure(cmd_str):
    args = shlex.split(cmd_str)
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

def configure(cmd_str):
    args = shlex.split(cmd_str)
    config = {
        "param": lambda params: cmdparams.add(*params), 
        "paramrst": lambda _: cmdparams.removeall(),
        "lock": lambda param: cmdparser.reset({"lock": param}), 
        "unlock": lambda _: cmdparser.reset({"lock": ""}),
        "join": lambda _=None: cmdparser.reset({"split": False}), 
        "split": lambda _=None: cmdparser.reset({"split": True}),
        "help": show_help,
        "prefix": lambda param: cmdparser.reset({"prefix": param}),
        "suffix": lambda param: cmdparser.reset({"suffix": param})
    }

    if args[0] in config:
        config[args[0]](args[1:])
    else:
        print(f"({clr('!')}) Unrecognized subsystem command.")

def exec_shell(cmd_str):
   os.system(cmd_str)

def main():
    hst_name = urlparse(url).netloc
    hst_tag = f" @ {clr(hst_name, fgcolor=_.MAGENTA)}" if hst_name else ""
    cmd_str = input(f"{clr('xrpc')}{hst_tag} ({global_call})> " if global_call else f"{clr('xrpc')}{hst_tag} > ").strip()
    
    if cmd_str.startswith("! "):
        exec_shell(cmd_str[2:])
    elif cmd_str.startswith(": "):
        configure(cmd_str[2:])
    elif cmd_str:
        cmd, args = parse_cmd(f"{global_call} {cmd_str}" if global_call else cmd_str) # Prefix global call
        args = join_fixed_to_varargs(args)

        run = getattr(proxy, cmd)
        print(wrapper(run, args))

if __name__=="__main__":
   Color.setdefault(_.MAGENTA)
   Color.mapfg(['!', 'Error', 'i', 'xrpc'], [_.RED, _.RED, _.BLUE, _.BLUE])
   url = readargs("-s", sys.argv)

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
            debug=False
        )

