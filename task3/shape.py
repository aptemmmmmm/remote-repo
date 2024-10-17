import math
class shape:
    def area(self):
        raise NotImplemented("subclass must implement this function")
    def perimeter(self):
        raise NotImplemented("subclass must implement this function")
    def compare_area(self,other):
        if self.area()>other.area():
            print(self.name +' is bigger than '+other.name+' in area')
        else:
            print(self.name +' is smaller than '+other.name+' in area')
    def compare_perimeter(self,other):
        if self.perimeter()>other.perimeter():
            print(self.name+' is bigger than '+other.name+' in perimeter')
        else:
            print(self.name+' is bigger than '+other.name+' in perimeter')


def check_postive_number(x):
    assert isinstance(x, (int, float)), f"x should be a number, got {type(x).__name__} instead"
    assert x > 0, "it should be a postive number"
    pass
def check_is_triangle(a,b,c):
    check_postive_number(a)
    check_postive_number(b)
    check_postive_number(c)
    assert a+b>c and a+c>b and b+c>a,'it cannot be a triangle'
    pass

class circle(shape):
    def __init__(self,r):
        check_postive_number(r)
        self.name = "circle"
        self.r = r
        check_postive_number(self.r)
    def area(self):
        return math.pi *self.r*self.r
    def perimeter(self):
        return 2*pi*self.r
class rectangle(shape):
    def __init__(self,w=1,h=2):
        check_postive_number(w)
        check_postive_number(h)
        self.name = "rectangle"
        self.w = w
        self.h = h
    def area(self):
        return self.w*self.h
    def perimeter(self):
        return 2*self.h*self.w
class Triangle(shape):
    def __init__(self,a,b,c):
        check_is_triangle(a,b,c)
        self.name = "triangle"
        self.a=a
        self.b=b
        self.c=c
    def perimeter(self):
        return self.c+self.b+self.a
    def area(self):
        s = self.perimeter()/2
        return math.sqrt(s*(s-self.a)*(s-self.b)*(s-self.c))
