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

cmdparams = CmdParams()
cmdparser = CmdParser()

clr = Color.color

def wrapper(func, args):
   if func and args:
      print(f"Function: {func}({args})")
      return func(*args)
   
   elif func:
      print(f"Function: {func}")
      return func()

def configure(cmdstr: str):
    args = shlex.split(cmdstr)
    config = {
        "paramlst": lambda _ = None: cmdparams.list(),
        "paramadd": lambda p, n, v: cmdparams.add(p, n, v), 
        "paramdel": lambda p: cmdparams.remove(p),
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
       cmdlst = [ctype(elem) for elem in args]
       config[cmdlst[0]](*cmdlst[1:])
       
def shell(cmdstr):
   os.system(cmdstr)

def main():
    host = urlparse(url).netloc
    htag = f" @ {clr(host, fgcolor=_.MAGENTA)}" if host else ""
    conf = f"{cmdparser.config['prefix']}{cmdparser.config['lock']}{cmdparser.config['suffix']}"
    cmdstr = input(f"{clr('xrpc')}{htag} ({clr(conf, fgcolor=_.YELLOW)})~$ " if conf else f"{clr('xrpc')}{htag} ~$ ").strip()
    
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
sys.argv.append("http://localhost:8000")
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

