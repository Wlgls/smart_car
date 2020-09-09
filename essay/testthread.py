import threading
import time

num = 10

def aa():
    while(True):
        print(num)

av = threading.Thread(target=aa)
av.setDaemon(True)
av.start()


time.sleep(1)

num=20

time.sleep(1)