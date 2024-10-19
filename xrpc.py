#!/bin/python3
import sys
import requests as req
import os
from xmlrpc.client import ServerProxy

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

      elif c=="." and (indx_of(c)==0 or indx_of==len(n_str)-1):
         return False

      elif c=="." or c==".":
         continue # Is exceptional char and in right pos

      # Other char
      if not c.isnumeric():
         return False

   return True

def parse_cmd(cmd_str):
   argv = cmd_str.split(' ')
   for indx in range(0, len(argv)):
      if isnumber(argv[indx]):
         argv[indx] = int(argv[indx]) if argv[indx].isnumeric() else float(argv[indx]) # int() if whole number else float()

   if not argv:
      return None, None
   elif len(argv)==1:
      return argv[0], None
   else:
      return argv[0], argv[1:]

def wrapper(func, args):
   if func and args:
      print(f"Function: {func}({args})")
      return func(*args)
   
   elif func:
      print(f"Function: {func}")
      return func()

def reqbody_to_xml():
   pass

def xml_to_reqbody():
   pass

def exec_shell(cmd_arr):
   os.system(cmd_str)

if __name__=="__main__":
  try:
    host = safe_read("-host", sys.argv)
    port = safe_read("-p", sys.argv)

    # TODO Test connection

    print(f"Target: http://{host}:{port}/")
    proxy = ServerProxy(f"http://{host}:{port}/")
    while True:
      cmd_str = input("cmd > ").strip()
      
      if cmd_str:
        if cmd_str.startswith("! "):
           exec_shell(cmd_str[2:])
           continue

        cmd, args = parse_cmd(cmd_str)
        run = getattr(proxy, cmd)
        print(wrapper(run, args))
        
  except KeyboardInterrupt:
    bye("\nCtrl-C", False)

  except Exception as ex:
    raise ex
  
  #TODO Catch xmlrpc.client exceptions
