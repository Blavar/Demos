'''
Step (2) is pretty straightforward
For N < MAX_N run CASES_NUM cases, count the number of positive ones, then write the probability
positives/CASES_NUM in a dictionary for N
The dictionary is then saved to a json, in order to be used further down the line
'''
CASES_NUM = 1000
MAX_N = 100

import random
def gen( n ):

    wolf = 0
    opposite = n//2

    eaten = [False for i in range( n )]
    eaten[wolf] = True

    eaten_num = 1

    while True:
        #roll for a move
        if random.randint(0, 1) == 0:
            wolf -= 1
        else:
            wolf += 1

        #check boundry conditions
        if wolf == -1:
            wolf = n-1
        elif wolf == n:
            wolf = 0

        if not eaten[wolf]:
            eaten_num += 1
            eaten[wolf] = True

        #check termination condition
        if wolf == opposite:
            if eaten_num == n:
                return True
            else:
                return False
            
CASES_NUM = 10000
MAX_N = 100

#calculate times

dataX = []
dataY = []
for n in range( 2, MAX_N + 2, 2 ):
    positive = 0
    print(n)
    for i in range( CASES_NUM ):
        if gen( n ):
            positive += 1
    dataX.append( n )
    dataY.append( positive/CASES_NUM )


#print(res)
import json
res = {
    'X' : dataX,
    'Y' : dataY
}
DB = open( 'DB.json', 'w' )
DB.write( json.dumps( res ) )

