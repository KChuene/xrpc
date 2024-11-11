#!/bin/python3
import sys
import requests as req
import os
import shlex
import xmlrpc.client as xc
import discvr as dcv

fixed_params = {}
discoverer = None # Additional module to run bruteforcing
global_call = None
split_input = True
host = "127.0.0.1"
port = 8000

def bye(msg = "Terminating...", show_help = True):
  print(msg)
  
  if show_help:
    print()
    print("Usage: xmlrpc.py -host localhost -p 8000")
  
  sys.exit()

def safe_read(opt, argv):
  if not opt in argv:
    bye(f"{opt} expected but not found.")
    
  opt_indx = argv.index(opt)
  if opt_indx < len(argv):
    opt_value = argv[opt_indx + 1]
    
    return opt_value
  else:
    bye("Insufficient args.")
    
  return "0"

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
      print(f"Insufficient params. Expecting {max(fixed_params) - length} more to join with fixed params.")
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
   if argv==None:
      fixed_params = {}
      return
   elif len(argv) == 0:
      list_fixed_params()
      return
   elif len(argv) < 2:
      print("Both parameter number and value are required.")
      return

   if not argv[0].isnumeric():
      print("Invalid parameter number.")
      return

   param = int(argv[0])
   if param > 0 and param < 10:
      if isnumber(argv[1]):
         fixed_params[param] = int(argv[1]) if argv[1].isnumeric() else float(argv[1])
      else:
         fixed_params[param] = argv[1]

def lock_call(argv):
   if len(argv) < 1:
      print("Expected function name.")
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

def disc(args):
   global discoverer
   if not discoverer:
      discoverer = dcv.Discover(host, port)

   if not args:
      discoverer.shw_status()
      return
   elif len(args) < 2 or not args[1].isnumeric():
      print("Provide appropriate arguments.")
      return

   discoverer.run(*args)

def configure(cmd_str):
   args = shlex.split(cmd_str)
   config = {
      "param": set_param,
      "paramrst": lambda _=None: set_param(None),
      "lock": lock_call,
      "unlock": unlock_call,
      "join": lambda _=None: set_split_input(False),
      "split": lambda _=None: set_split_input(True),
      "disc": disc
   }

   if args[0] in config:
      config[args[0]](args[1:])
   else:
      print("Unrecognized subsystem command.")

def exec_shell(cmd_str):
   os.system(cmd_str)

if __name__=="__main__":
   host = "192.168.56.128" #safe_read("-host", sys.argv)
   port = 8000 #safe_read("-p", sys.argv)

   # TODO Test connection

   proxy = xc.ServerProxy(f"http://{host}:{port}/")
   print(f"Target: http://{host}:{port}/")

   while True:
      try:
        cmd_str = input(f"xrpc ({global_call})> " if global_call else "xrpc > ").strip()
      
        if cmd_str:
          if cmd_str.startswith("! "):
             exec_shell(cmd_str[2:])
          elif cmd_str.startswith(": "):
             configure(cmd_str[2:])
          else:
             cmd, args = parse_cmd(f"{global_call} {cmd_str}" if global_call else cmd_str) # Prefix global call
             args = join_fixed_to_varargs(args)

             run = getattr(proxy, cmd)
             print(wrapper(run, args))
      except xc.Fault as fault:
        print(f"Error: {fault}")
         
      except KeyboardInterrupt:
        bye("\nCtrl-C", False)

      except Exception as ex:
        raise ex
  
  #TODO Catch xmlrpc.client exceptions
  #TODO Test connection to host:port