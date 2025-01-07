'''
A very rudimentary implementation of ID3 algorithm (i think) for building decision trees.

Data was borrowed from here:
https://www.kaggle.com/datasets/pablomgomez21/drugs-a-b-c-x-y-for-decision-trees

To be completely honest, I don't know if I can use this data as part of the portfolio, but here we are.
Then again, I don't see any Data Science Police around, do you?

Anyway, build.py has the algorithm itself which is pretty standard.
This file uses 5-fold cross validation to estimate average success rate of the algorithm on the data.
It turns out to be ~0.85, which... well.. could be better

I conservatively consulted 'AI: A Mordern Approach' by Russel, Norvig, Section 18.3: Learning Decision Tree
while working on it.



[Flex] I'm pretty proud of the fact that, while reading about the algorithm, I stopped at the first concrete idea behind
it and tried to predict how it's gonna look. I came up with a guess as to what it does and how it does it, 
and that entropy will be probably be the measure used to evaluate how good a split is. Even had some general fromulas.
To my surprise, my guess was pretty good, and did entrop pop up in the discussion. My formulas were a bit off though.

'''
import pandas as pd
import numpy as np

from builder import builder

def row_to_dict(row):
    res = {}
    for key, val in row[1].items():
        res[key] = val
    return res

# # # # # # # # # # # # # # # # # 


K = 5

df = pd.read_csv( 'drug.csv' )
frags = np.array_split( df, K )



target = 'Drug'
attributes = df.columns.drop(target)

success_rates = []

for i in range( K ):
    train_data = pd.concat( [frags[j] for j in range(K) if j != i], ignore_index=True )
    test_data = frags[i]
    
    root = builder( train_data, attributes, target )

    positive = 0
    total    = test_data.shape[0]

    for row in test_data.iterrows():
        #row to dict
        test_case = row_to_dict( row )
        prediction = root.klassify( test_case )
        if test_case[target] == prediction:
            positive += 1

    success_rates.append( positive/total ) 
    print( f'SET {i}\nSUCCESS RATE: {success_rates[i]}\n' )



print( f'AVERAGE SUCCESS RATE: {sum( success_rates ) / len(success_rates )}' )








