import sys

def dynamicFunc(moduleName):
     try:
        module = __import__(moduleName)
        for attr in module.__dict__.keys():
            if attr[0:2] != "__":
                if module.__dict__[attr].__str__()[0:9] == "<function":
                    print "running function '", attr, "' on input",
                    return module.__dict__[attr]
     except ImportError:
        return None
    

if (len(sys.argv)==1 or len(sys.argv)==2):
    print 'Usage: main.py ModuleName InputString'
    sys.exit(0)
else:
    modName = sys.argv[1]
    inStr = ""
    if len(sys.argv)>3:
        for i in sys.argv[2:]:
            inStr += i+" "
        inStr = inStr[0:len(inStr)-1]
    else:
        inStr = sys.argv[2]
    print "trying to run a function from module '", modName, "' on '", inStr, "'"
    myTryF = dynamicFunc(modName)
    print "'",inStr,"'"
    print "result: ", myTryF(inStr)
    
#===============================================================================
# print dynamicFunc("crcStr")
# print dynamicFunc("cypherStr")
# print dynamicFunc("binaryStr")
# print dynamicFunc("binaryStr23")
#===============================================================================