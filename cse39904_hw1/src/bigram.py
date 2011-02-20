# Dmitry Golomidov CSE399 004 HW1
import copy
"""implementation of bigram"""
def myCompare(first,second):
    return cmp(first.lower(),second.lower())

def sortByFrst(a,b):
    xr = a.split("-")
    yr = b.split("-")
    x = xr[0].lower()
    y = yr[0].lower()
    #print x, y
    if(x > y):
        return 1
    elif (x < y):
        return -1
    else:
        return 0
    
def msort(a,b):
    x = a.lower()
    y = b.lower()
    if(x > y):
        return 1
    elif (x < y):
        return -1
    else:
        return 0

string = "I like Python and I like Java but like Fred I dislike BASIC";
def bigram(string):
    string = string.lower() # since everything should be lowercased
    lst = string.split(" ")
    unique = []
    for el in lst:
        if el not in unique:
            unique.append(el)
            
    
    
    unique.sort(myCompare)
    #print unique
    
    dict = {}
    #for el in unique:
    for el in unique:
        lstcp = copy.copy(lst)
        ln = len(lstcp)
        while True:
            try:
                ind = lstcp.index(el)
                next = ind + 1
                if next <= len(lstcp)-1:
                    val = lstcp[next]
                    nkey = el+"-"+val
                    if nkey not in dict.keys():
                        dict[nkey] = 1
                    else:
                        dict[nkey] += 1
                smval = len(lstcp)-1-next
                lstcp = lstcp[next+1:ln] #here we use same length because slicing keeps the length, just rewrites the start pointer
            except ValueError:
                break
    dict[lst[len(lst)-1]] = 0
    
    prev = ""
    out = ""
    acc = {}
    for keypair in sorted(dict.keys(),sortByFrst):
        kr = keypair.split("-")
        k = kr[0]
        if (len(kr) > 1):
            n = kr[1]
        else:
            n = ""
        r = dict[keypair]
        if k == prev:
            acc[n] = r
        else:
            if prev != "":
                out += prev.lower() + " "
                for sm in sorted(acc.keys(),msort): #also sort through keys in alphabetical order
                    if acc[sm] > 0:
                        out += sm + " " + acc[sm].__str__() + " "
                    else:
                        out += sm
                out += "\n"
            acc = {}
            acc[n] = r
            prev = k
    out += prev.lower() + " "
    for sm in sorted(acc.keys(),msort):
        out += sm + " " + acc[sm].__str__() + " "
    out += "\n"
    return out

#f = open('boswell.txt','r')
#input = f.read()
#f.close()
#res = bigram(input)
#nf = open('out','w')
#nf.write(res)
#nf.close()
q = bigram(string)
print q