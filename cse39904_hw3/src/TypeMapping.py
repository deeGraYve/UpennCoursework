import exceptions

class Error(Exception):
    pass

class NonStringKey(Error):
    """not a string key exception"""
    def __init__(self, value):
        self.value = "'" + value.__str__() + "' is not a string!"
        
    def __str__(self):
        return repr(self.value)

class ClassNameMismatch(Error):
    """class name mismatch exception"""
    def __init__(self, value, type, key):
        self.value = "Illegal mapping of '" + value.__str__() + "' to key '" + \
        key + "'. '" + value.__str__() +"' is not of '" + type + "' type."
        
    def __str__(self):
        return repr(self.value)
    
class ClassNameExclude(Error):
    """class name exclude exception"""
    def __init__(self, value, type, key):
        self.value = "Illegal mapping of '" + value.__str__() + "' to key '" + \
        key + "'. '" + value.__str__() +"' cannot be of '" + type + "' type."
        
    def __str__(self):
        return repr(self.value)

class TypeMapping:
    """main type mapping class"""
    def __init__(self, classObj, dataStub={}):
        self.data = {} #could have used copy here, since {} is mutable and would "inherit" previous classes dataStub reference, but initializing it to {} and then using __setitem__ does the trick 
        self.typeSet = classObj
        self.myVerify = self.verify #assign a method for verification of consistency
        self.myVerifyException = ClassNameExclude #assign an exception
        for i in dataStub.keys():
            self.__setitem__(i, dataStub[i])
            
        
    def __getitem__(self,key):
        return self.data[key]
    
    def __setitem__(self,key,item):
        if type(key) is not str: #check if key is a string
            raise NonStringKey(key)
        if not self.myVerify(item): #apply verification function
            raise self.myVerifyException(item,self.typeSet.__class__.__name__, key)
        self.data[key] = item
        
    def __repr__(self):
        return self.__class__.__name__ + "(" + self.typeSet.__repr__() + ", " + self.data.__repr__() + ")" #repr as I understand has to return a string on which we can call eval and get a copy of an object
        
    def __str__(self):
        return self.data.__str__()
    
    def verify(self,item):
        return True

class TypeConsistentMapping(TypeMapping):
    def __init__(self,classObj,dataStub={}):
        TypeMapping.__init__(self, classObj, dataStub) #init TypeMapping class
        self.myVerifyException = ClassNameMismatch #our own exception

    def verify(self,item): #our own verify
        if(self.typeSet.__class__.__name__ != item.__class__.__name__):
            return False
        return True
    
class TypeExclusionMapping(TypeMapping):
    def __init__(self,classObj,dataStub={}):
        TypeMapping.__init__(self, classObj, dataStub) #superclass contructor called only

    def verify(self,item):#own verify
        if(self.typeSet.__class__.__name__ == item.__class__.__name__):
            return False
        return True


#test cases

n = TypeMapping([])
print n.__class__.__name__
try:
    #n[2] = 5
    n["str"] = "strin"
    print n
except NonStringKey, e:
    print 'NonStringKey exception occured: ', e.value
except ClassNameMismatch, e:
    print 'ClassNameMismatch exception occured: ', e.value
n["str"] = "newstring"
#print n

k = {}
k['1'] = 'one'
k['2'] = 'two'
m = TypeMapping([])
print "m is ", m, m.data

z = TypeMapping("oi")
print "z is ", z, z.data


q = TypeConsistentMapping(1)
q['sm'] = 76
print q
#q['smt'] = 'df'
q['smtc'] = 998
print "q is ", q

d = TypeConsistentMapping(1)
print "d is ", d

v = TypeConsistentMapping("m",k)
print "v is ", v
print v.__repr__() #repr check
p = v.__repr__()
print p
kl = eval(p)
print kl
print v

fc= TypeConsistentMapping("m")
fc["meh"] = "sd"
#fc["meh2"] = 9
print "fc is ", fc

z = TypeExclusionMapping("m")
print z
z['1'] = 3
z['2'] = []
print z

z2 = TypeExclusionMapping([],k)
print z2
z2['dsf'] = {}
print z2
#z2['sdf'] = []

print z.__repr__() #repr check
p = z.__repr__()
print p
kl = eval(p)
print kl
print z