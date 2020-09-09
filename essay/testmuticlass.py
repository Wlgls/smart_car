class A:
    def __init__(self):
        self.v = 1
    def printvv(self):
        print('a')

class B:
    def __init__(self):
        self.v = 2
    def printvv(self):
        print('b')

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
    
    def printa(self):
        # print(A.v, B.v)
        print(self.v)
    def pp(self):
        self.printvv()
        A.printvv(self)
        B.printvv(self)


c = C()
c.printa()
c.pp()
c.printvv()