import xmlrpc.client as xc
import time
from pathlib import Path


class Discover:
    def __init__(self, url):
        self.url = url
        self.exec_status = {}

    def status_rst(self, wlist, delay):
        return {
            "Delay": delay,
            "Wordlist": wlist,
            "Tested": 0,
            "Succeeded": 0,
            "HitList": [],
        }

    def log_success(self, rpc_method):
        self.exec_status["HitList"].append(rpc_method)
        self.exec_status["Succeeded"] += 1


    def try_call(self, proxy, method, delay):
        if delay:
            time.sleep(delay)

        success = True
        try:
            getattr(proxy, method)()
            self.log_success(method) # Save for shw_status later

        except xc.Fault as fault:
            if "TypeError" in str(fault): # TypeError, method exist but incorrect args
                self.log_success(method)
            else:
                success = False

        except Exception:
            success = False

        self.exec_status["Tested"] += 1
        return success

    def shw_status(self):
        if not self.exec_status:
            return
        
        status = self.exec_status
        print(f"(i) {status['Wordlist']}, delay by {status['Delay']}s")
        print(f"(i) {status['Succeeded']} hit(s) of {status['Tested']} test(s)")

        print("", end="\n" if status["HitList"] else "")
        for method in status["HitList"]:
            print(method)

    def discover(self, proxy, path, delay):
        with open(path, "r") as wlist:
            lcount = 0
            for line in wlist:
                lcount += 1

            wlist.seek(0)
            priv_line_len = currline = 0
            for line in wlist:
                currline += 1
                line = line.strip() 

                progress_str = f"{line} ({currline}/{lcount})"
                print(f"\r{' '*priv_line_len}\r{progress_str}", end="") # Fancy-ish output

                if self.try_call(proxy, line, float(delay)):
                    print() # Leaves line on display

                priv_line_len = len(progress_str) # Fancy-ish output
            
            print(f"\r{' '*priv_line_len}")
        print()

    def run(self, wordlist, delay):
        proxy = xc.ServerProxy(self.url)
        #TODO Connection to url
        wpath = Path(wordlist)

        if not wpath.exists():
            print("Wordlist file not found.")
            return

        print(f"< Discovering {wpath} delay by {delay} >")
        self.exec_status = self.status_rst(wpath, delay)
        self.discover(proxy, wpath, delay)

