#!/bin/python3
import random
import subprocess
from xmlrpc.server import SimpleXMLRPCServer as SimpleRPC

passcode = random.randint(1000, 9999)

def h(n, s):
        return f"Hello, {n} {s}."

def g():
        return "Great day!"

def exec_cmd(cmd):
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.stdout.read() + process.stderr.read()
    return output

def shell(cmd, code):
    if code != passcode:
        return "Wrong passcode!"
    else:
        return exec_cmd(cmd)

if __name__=="__main__":
        s = SimpleRPC(("0.0.0.0", 8000))
        print("Handle: 0.0.0.0:8000")
        print(f"Shell Access-Code: {passcode}")

        s.register_function(h)
        s.register_function(g)
        s.register_function(shell)
        try:
                s.serve_forever()
        except KeyboardInterrupt:
                pass