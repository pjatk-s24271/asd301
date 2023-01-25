from queue import Queue
from algs.arraysort import *
from algs.heapsort import *
from algs.quicksort import *
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
import threading
import psutil

def isSorted(arr: list[int]):
    for i in range(1, len(arr)):
        if arr[i-1] > arr[i]:
            return False
    return True

def isReversedSorted(arr: list[int]):
    for i in range(1, len(arr)):
        if arr[i-1] < arr[i]:
            return False
    return True

def plot(graphs):
    with open('output/frames.txt', 'r') as f:
        set_name = None
        values = []
        fig, axs = plt.subplots(int(graphs), sharey=True)
        cur_plot = 0

        for line in f:
            if line.startswith('#'):
                # Extract the set name
                set_name = line[1:].strip()
                values = []
            elif line.startswith("^"):
                # Split the line
                _, nanoseconds, miliseconds = line.split(" - ")
                nanoseconds = int(nanoseconds)
                miliseconds = int(miliseconds[:-1])

                # Add graph
                axs[cur_plot].plot(values)
                axs[cur_plot].set_title(f'{set_name} - {nanoseconds} nanoseconds - {miliseconds} miliseconds - {round(np.mean(values) / 1000000)} MB (AVG) - {round(max(values) / 1000000)} MB (MAX)')
                axs[cur_plot].set_xticks([])
                cur_plot += 1
            else:
                # Split the line by whitespace and convert the values to floats
                values.append(float(line.strip()))

        fig.suptitle("RAM USAGE IN BYTES", size=16)
        #plt.get_current_fig_manager().full_screen_toggle()
        plt.xticks([])
        plt.subplots_adjust(left=0.03, right=0.98, top=0.91, bottom=0.03, hspace=0.65)
        plt.show()

def mem(): return psutil.Process().memory_info().rss

def tracking(q: Queue):
    frames = open("output/frames.txt", "w")

    cmd = ""
    timestamps = {}

    while True:
        try:
            cmd = q.get_nowait()
        except Exception:
            cmd = ""
            
        if cmd == "done": break #end tracking when main is done
        elif cmd != '':
            if cmd in timestamps.keys(): #close block when repeated tag is posted
                frames.write('^' + cmd + " - " + 
                    str(time.perf_counter_ns() - timestamps[cmd]) +
                    " - " + 
                    str(round((time.perf_counter_ns() - timestamps[cmd]) / 1000000)) +
                    '\n'
                )
            else: #open block when new tag is posted
                timestamps[cmd] = time.perf_counter_ns()
                frames.write('#' + cmd + '\n')
        else: #append block when cmd is empty | ignore values before first tag
            frames.write(str(mem()) + '\n')
        
    frames.close()

def main(q, max, size):
    unsorted = np.array(np.random.randint(0, max, size)).tolist()
    ascending = unsorted.copy()
    ascending.sort()
    descending = ascending[::-1]

    print("Start!")

    q.put("quick-un")
    quicksort(unsorted.copy())
    q.put("quick-un")

    q.put("quick-as")
    quicksort(ascending.copy())
    q.put("quick-as")

    q.put("quick-de")
    quicksort(descending.copy())
    q.put("quick-de")

    q.put("heap-un")
    heapsort(unsorted.copy())
    q.put("heap-un")

    q.put("heap-as")
    heapsort(ascending.copy())
    q.put("heap-as")

    q.put("heap-de")
    heapsort(descending.copy())
    q.put("heap-de")

    q.put("array-un")
    arraysort(unsorted.copy())
    q.put("array-un")

    q.put("array-as")
    arraysort(ascending.copy())
    q.put("array-as")

    q.put("array-de")
    arraysort(descending.copy())
    q.put("array-de")

    q.put("done")

#Create queue and threads
queue = Queue()
trackingThread = threading.Thread(target = tracking, args = (queue,))
mainThread = threading.Thread(target = main, args = (queue, 10000, 1000000,))

#Disable limitations
sys.setrecursionlimit(400000000)
threading.stack_size(67108864)

#Start threads
trackingThread.start()
mainThread.start()

#Wait for threads to end
trackingThread.join()

#Plot results
plot(9)