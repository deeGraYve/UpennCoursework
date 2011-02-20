def FibonacciGen():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b #calculate the next vals
            
def GetFibonacci(num):
        f = FibonacciGen()
        for x in range(num):
            print f.next()
            
GetFibonacci(20) #20 numbers