'''
We got pretty everything we want. The last things to do are:
(1) get the data
(2) feed it to the model
(3) see what he comes up with

Here, we'll run a couple models, trained on the generated data, and pick the one with the smallest loss to be processed next.
In order not to allow our models to fall victim to severe underfitting, we'll take every fifth
element from the input data.
'''

import json # JAASOOOON
import numpy as np
from math import log10

class Model:
    def __init__(self):

        self.params = {
            'a' : 1,#np.random.uniform(-1, 1),
            'b' : 0,
            'c' : 0#np.random.uniform(-1, 1)
        }
        self.derivatives = dict( self.params )

        for val in self.params.values():
            val = np.random.uniform( -10, 10 )

    def loss( self, Y, Yhat ):
        return np.mean( (Y - Yhat)**2 )

    def forward(self, X):

        a = self.params['a']
        b = self.params['b']
        c = self.params['c']

        Yhat = a*((X+b)**(-1)) + c
        return Yhat
        

    def backward(self, X, Y, Yhat):
        a = self.params['a']
        b = self.params['b']
        c = self.params['c']

        df = Y - Yhat

        derivatives = {}
        derivatives['a'] = -2*np.mean( np.multiply( df, (X + b)**(-1) ) )
        #derivatives['b'] = -2*np.mean( np.multiply( df, -a*(X+b)**(-2)) ) 
        derivatives['c'] = -2*np.mean( df )

        return derivatives
    
    def update_params(self, derivatives, lr):


        self.params['a'] = self.params['a'] - lr * derivatives['a']
        #self.params['b'] = self.params['b'] - lr * derivatives['b']
        self.params['c'] = self.params['c'] - lr * derivatives['c']

    def train( self, X, Y, lr, epochs):

        for i in range( epochs ):

            Yhat = self.forward( X )
            derivatives = self.backward( X, Y, Yhat )
            self.update_params( derivatives, lr )

        return ( self.loss( Y, self.forward(X) ), self.params )
    
#read data
file = open( 'DB.json', 'r' )
data = json.load( file )

X = np.array(data['X']).astype( float )[0::5]
Y = np.array(data['Y']).astype( float )[0::5]

LR = 0.01
EPOCHS = 10000
MODELS = 100


results = []

for i in range( MODELS ):
    results.append( Model().train( X, Y, LR, EPOCHS ) )

best = min( results, key=lambda res: res[0] )


print( best )
#save the best
BEST = open( 'BEST.json', 'w' )
BEST.write( json.dumps( best ) )


