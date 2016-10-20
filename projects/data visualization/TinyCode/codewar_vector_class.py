class MyError(Exception):
    def __init__(self, args):
        self.value = args
    def __str__(self):
        return self.value

class Vector():
  # TODO: Finish the Vector class.
    def __init__(self, foo=[]):
        self.numbers =foo
    def __str__(self):
        string = "("
        for num in self.numbers:
            string = string+str(num)+","
        string = string[:-1]+")"
        return string
    
    def add(self, foo):
        try:
            if len(self.numbers)!=len(foo.numbers):
                raise MyError("diffrent length")
            sum = Vector([0]*len(self.numbers))
            for i in range(0,len(self.numbers)):
                sum.numbers[i] = self.numbers[i] + foo.numbers[i]
            return sum
        except MyError as e:
            print e.value
        

    def subtract(self, foo):
        try:
            if len(self.numbers)!=len(foo.numbers):
                raise MyError("diffrent length")
            sub = Vector([0]*len(self.numbers))
            for i in range(0,len(self.numbers)):
                sub.numbers[i] = sub.numbers[i] - foo.numbers[i]
            return sub
        except MyError as e:
            print e.value

    def dot(self, foo):
        try:
            if len(self.numbers)!=len(foo.numbers):
                raise MyError("diffrent length")
            dot = 0
            for i in range(0,len(self.numbers)):
                dot = self.numbers[i]*foo.numbers[i]
            return dot
        except MyError as e:
            print e.value

    def norm(self):
        normSum = 0
        for i in range(0,len(self.numbers)):
            normSum+=self.numbers[i]**2
        return normSum**0.5

a = Vector([1,2,3])
b = Vector([3,4,5])
c = Vector([5,6,7,8])

print a.add(b).numbers # should return Vector([4,6,8])
print a.subtract(b).numbers # should return Vector([-2,-2,-2])
print a.dot(b) # should return 1*3+2*4+3*5 = 26
print a.norm() # should return sqrt(1^2+2^2+3^2)=sqrt(14)
print str(a)