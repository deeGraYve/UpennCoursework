class top:
    x=2
    y=8
    a=2

class middleA(top):
    x=4
    def __init__(self):
        pass
    

class middleB(top):
    x=8
    y=4
    def __init__(self):
        self.r=-2

class bottom(middleA, middleB):
    z=3
    def __init__(self):
        middleA.__init__(self)
        middleB.__init__(self)
        self.q=42

inst=bottom()
inst2=bottom()

print inst.q
"""returns 42 since it q is a variable that belongs to class bottom, self variable"""
print inst.r
"""returns -2 because it inherits variable from middleB class, since the inheritance happens bottom-up"""
print bottom.a
"""returns 2 since the variable gets inherited from top class without being redefined in middle and bottom classes """
print inst.x
"""returns 4. The value of x propagates through classes. But since the attribute is being looked up in 
the instance namespace(did not define x) then in the class namespace, which consists of initializing middleA
and middleB classes but since class A initilizes the top class with x=8 and then changes it in its namespace to 4,
this becomes the last namespace that changes it, since top class does not have init method and it's variables references,
are accessible within its scope(outermost scope with build-in names) and replaced by the ones that have the 
same names, therefore this value is inherited"""

inst.x = 16
print inst2.x
"""returns 4 as well, since all variables found outside of the innermost scope are read-only, so an attempt to write 
to such a variable will simply create a new local variable, leaving the identically named outer variable unchanged
And that is why we use global - all references and assignments go directly to the middle scope containing the 
module's global names"""

print inst.y
"""returns 8, goes to outermost scope (top), therefore class hierarchy is searched depth-first(left to right in
order of occurence)"""