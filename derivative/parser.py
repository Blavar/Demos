from common import *

#parse the input string 
class Parser:
    def __init__(self, buf:str):
        self.buf = buf
        self.l   = len( buf )
        self.i   = 0

        self.res = []

        self.parse()

    def empty(self):
        return self.i == self.l

    def get(self):
        return self.buf[self.i]
    
    def next(self):
        self.i += 1
    
    def skip(self):
        while not self.empty() and self.get().isspace():
            self.next()

    #other option would be to write inside self.res inside read
    def read_num(self):
        c = self.get()
        
        res = ''
        while not self.empty() and (self.get().isnumeric() or self.get() == '.'):
            res += self.get()
            self.next()

        return res

    def read_name(self):
        c = self.get()
        
        res = ''
        while not self.empty() and (self.get().isalpha() or self.get().isnumeric() or self.get() == '_' ):
            res += self.get()
            self.next()

        return res        

    def parse(self):

        while not self.empty():
            c = self.get()
            
            if c.isspace():
                self.skip()
            elif c.isnumeric():
                self.res.append( self.read_num() )
            elif c.isalpha():
                self.res.append( self.read_name() )
            elif c in special_symbols:
                self.res.append( c )
                self.next()
            else:
                self.next()

    def tokens(self):
        return self.res

#entry function that returns tokens
def parse( buf ):
    return Parser( buf ).tokens()
