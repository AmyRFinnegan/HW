# Amy Finnegan
# This file gets times for HW3 sorting functions and plots them

import time 
import HW3
import random
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot


# Loop that gets a list of times for each type of sort
    
N = 10
trials = 4
merge_times = [0] * trials
bubble_times = [0] * trials
quick_times = [0] * trials
for i in range(0, trials):
  random_array = range(1, N)
  random.shuffle(random_array)
  
  start_time = time.clock()
  HW3.mergeSort(random_array)
  merge_times[i] = time.clock() - start_time
  
  random_array = range(1, N)
  random.shuffle(random_array)
  
  start_time = time.clock()
  HW3.bubblesort(random_array)
  bubble_times[i] = time.clock() - start_time
  
  random_array = range(1, N)
  random.shuffle(random_array)
  
  start_time = time.clock()
  random_array.sort()
  quick_times[i] = time.clock() - start_time
  
  N = N * 10
  
print merge_times
print bubble_times
print quick_times

#  Function that plots the results form above

def plotHW(times, times2, times3, name ="plot"):
    x = [10, 100, 1000, 10000]
    pyplot.plot(x, times, 'b-', label="BubbleSort")
    pyplot.plot(x, times2, 'r--', label="MergeSort")
    pyplot.plot(x, times3, 'g^--', label="QuickSort")
    #pyplot.axis(0, 10000, -0.1, 23)
    pyplot.xlabel( 'Array Size' )
    pyplot.ylabel( 'Time (seconds)' )
    pyplot.xticks([10, 100, 1000, 10000])
    pyplot.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
    pyplot.savefig(name + "%d.png" % len(times))
    pyplot.close()
    #pyplot.show()
    

plotHW(bubble_times, merge_times, quick_times, name ="Combo")


