from datetime import datetime
from tabulate import tabulate
import os
import speedtest
import sys
import time
import threading

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()
            sys.stdout.write('\b')

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

headers = ["item", "Bandwidth (Mbps)"]
today = datetime.now().strftime("%m/%d/%Y, %H:%M")
print("Testing internet connection...")
print()
response = os.system("ping -c 1 google.com > /dev/null")

if response == 0:
    s = speedtest.Speedtest()
    print("\033[1;32mInternet connection OK!!\033[0;m")    
    print("Testing throughput...")
    print()
    with Spinner():
        table = [["Download","\033[1;32m" + str(round((s.download()/1000000),3)) + "\033[0;m"],
                ["Upload", "\033[1;32m" + str(round((s.upload()/1000000),3)) + "\033[0;m"]]
        print("Report date: " + str(today))
        print()
        print(tabulate(table, headers, tablefmt="github"))
        print()        
else:
    print("\033[1;31mNo internet connection\033[0;m")



