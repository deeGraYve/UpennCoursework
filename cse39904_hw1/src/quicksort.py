#Dmitry Golomidov CSE 399 - 004 HW 1
import random

def split(list, start, end, compF):
    """function that finds a pivot by separating the values
    that are smaller and bigger than pivot to sides of the pivot
    in the list (bigger to the left)"""
    pivot = list[end]
    lo = start-1
    hi = end

    fin = False
    while not fin:
        while not fin:
            lo += 1
            if lo == hi:
                fin = True
                break
            if compF(pivot, list[lo]) < 0:
                list[hi] = list[lo]
                break
        while not fin:
            hi -= 1
            if lo == hi:
                fin = True
                break
            if compF(pivot, list[hi]) > 0:
                list[lo] = list[hi]
                break

    list[hi] = pivot
    return hi

def myquicksort(list, start, end,function):
    """function first checks if the chunk of the list is valid,
    i.e. the start is less than the end, and if it is the case 
    it calls split function on it to determine the pivot and
    calls itself recursively on both list partitions - one for 
    elements lower in list than the pivot, one for elements
    higher than the pivot, because pivot is already sorted and 
    it already appears at the right place"""
    if start < end:
        div = split(list, start, end, function)
        myquicksort(list, start, div-1,function)
        myquicksort(list, div+1, end,function)
    else:
        return

def quicksort(list, function):
    """This function takes list as an argument and then calls myquicksort function on it"""
    if len(list)>1:
        myquicksort(list,0,len(list)-1,function)
    else:
        return
    
def asc(a,b):
    if a>b:
        return 1
    elif a<b:
        return -1
    else:
        return 0
    
def desc(a,b):
    if a>b:
        return -1
    elif a<b:
        return 1
    else:
        return 0
    
test = [0, 7, 3, 9, 1, 10, 0]
test.insert(3, 2)
test.insert(6, 7)
random.shuffle(test)
print "original: ", test
quicksort(test,asc)
print "ascending order: ", test
quicksort(test,desc)
print "descending order: ", test
#quicksort(test,splitDesc)
#print test