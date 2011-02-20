def toBin(someString):
    if not someString or len(someString) == 0:
        return ""
    else:
        out = []
        for c in someString:
            i = ord(c)
            b = ''
            while i > 0:
                j = i & 1
                b = str(j) + b
                i >>= 1
            out.append(b)
    return "".join(out)
    
#print toBin("kozel koz")