class calculator:
    def add(self,x,y):
        return x+y
    def sub(self,x,y):
        return x-y
    def div(self,x,y):
        return x//y
    def mul(self,x,y):
        return x*y
    def sroot(self,x,y):
        return x**y



obj =calculator()


print(obj.add(1,2))
print(obj.sub(1,2))
print(obj.div(1,2))
print(obj.mul(1,2))
print(obj.sroot(1,2))