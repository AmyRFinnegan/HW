# Amy Finnegan
# This file contains two sorting algorithms of different complexity classes: mergeSort and bubblesort

import random
import sys, time


def mergeSort(array):
  """Sorts by splitting, sorting and merging"""
  if len(array) <= 1:
      return array
      
  middle = len(array)/2
  left = (array[:middle])
  right =(array[middle:])
  
  left_sorted = []
  while len(left) > 0:
    left_sorted.append(min(left))
    left.remove(min(left))
    
  right_sorted = []
  while len(right) > 0:
    right_sorted.append(min(right))
    right.remove(min(right))
    
  result = []
  while len(left_sorted) > 0 and len(right_sorted) > 0:
    if left_sorted[0] > right_sorted[0]:
        result.append(right_sorted.pop(0))
    else:
        result.append(left_sorted.pop(0))
        
  if len(left_sorted) > 0:
     result.extend(left_sorted)
  else:
     result.extend(right_sorted)   

  return result


## bubble sort

def bubblesort(array_to_sort):
     """Sorts list by comparing first element through."""
     for leftStart in range(len(array_to_sort)-1, 0, -1):
         for i in range(leftStart):
             if array_to_sort[i] > array_to_sort[i + 1]:
                array_to_sort[i], array_to_sort[i + 1] = array_to_sort[i + 1], array_to_sort[i]
     return array_to_sort
     
"""
# tests


n = 1000
trials = 10
merge_times = [0] * trials
bubble_times = [0] * trials
quick_times = [0] * trials

for i in range(0, trials):
  random_array = range(1, n)
  random.shuffle(random_array)

  start_time = time.time()
  mergeSort(random_array)
  merge_times[i] = time.time() - start_time

  random_array = range(1, n)
  random.shuffle(random_array)

  start_time = time.time()
  bubblesort(random_array)
  bubble_times[i] = time.time() - start_time
  
  random_array = range(1, n)
  random.shuffle(random_array)
  
  start_time = time.time()
  random_array.sort()
  quick_times[i] = time.time() - start_time


print "Merge"
print "======================"
print "Max:   {0}".format(max(merge_times))
print "Min:   {0}".format(min(merge_times))
print "Mean:  {0}".format(sum(merge_times) / len(merge_times))
print "Total: {0}".format(sum(merge_times))

print "\nBubble"
print "======================"
print "Max:  {0}".format(max(bubble_times))
print "Min:  {0}".format(min(bubble_times))
print "Mean: {0}".format(sum(bubble_times) / len(quick_times))
print "Total: {0}".format(sum(bubble_times))

print "\nQuick"
print "======================"
print "Max:  {0}".format(max(quick_times))
print "Min:  {0}".format(min(quick_times))
print "Mean: {0}".format(sum(quick_times) / len(quick_times))
print "Total: {0}".format(sum(quick_times))
"""