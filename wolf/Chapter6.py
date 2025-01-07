'''
Turns out the model seems to be closer to 2/x than 1/x.
Let's adjust our guess to 2/x then.

We'll use R squared to measure how good of a fit we have.
Let's agree that R squared >= 0.95 contitutes a good fit.

First, we'll compare our model to our guess.
Then, just to be sure, the model to the data.
Lastly, and most crucially, we'll compare the guess and the data.

'''
import numpy as np
import json #JASOOON

def Rsq(Y, Yhat):
    y = np.mean(Y)
    SSres = np.sum((Y - Yhat)**2)
    SStot = np.sum( (Y - y)**2 )

    res = 1 - SSres/SStot
    return res


BEST = open( 'BEST.json', 'r' )
data = json.load( BEST )

loss = data[0]
params = data[1]


DATA = open( 'DB.json', 'r' )
data = json.load( DATA )

#data again made sparser due to underfitting
X = np.array( data['X'] ).astype( float )[0::5]
Y = np.array( data['Y'] ).astype( float )[0::5]

Ymodel = params['a'] * 1/X + params['c']
Yguess = 2/X

print( f'R^2 MODEL, GUESS: { Rsq( Ymodel, Yguess )} ')
print( f'R^2 DATA,  MODEL: { Rsq( Y, Ymodel ) }' )
print( f'R^2 DATA,  GUESS: { Rsq( Y, Yguess ) }')


'''
If You dared to run the script before changing any of the previous files,
You could see the values 
0.993
0.995
0.988

Which means that everything fits together nicely and 2/n is a pretty
good approximation to the problem posed in Chapter1, given variability
of the generated data.

'''