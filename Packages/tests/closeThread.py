
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
# SuperFastPython.com
# example of a thread executing a custom function
from time import sleep
from threading import Thread
 
# custom task function
def task():
    # execute a task in a loop
    for i in range(5):
        # block for a moment
        sleep(1)
        # report a message
        print('Worker thread running...')
    print('Worker closing down')
 
# create and configure a new thread
thread = Thread(target=task)
# start the new thread
thread.start()
# wait for the new thread to finish
thread.join()