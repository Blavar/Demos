'''
Given a dataframe and a target column, Splitter produces the best attribute to split on
calculating the maximal entropy gain among splits on attributes.

Recursive function builder() takes a dataframe, and returns a root of the decision tree.

'''


import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype

from math import log2

from factory import Factory

QUANTILES = 20


# # # # # # # # # # # # # # # # # # # # # # # #


#object describing a split on given atrribute
class Split:
    def __init__(self, type, attr, partitions, gain, t=0):
        self.type = type
        self.attr = attr
        self.partitions = partitions
        self.gain = gain
        self.t = t

    def __repr__(self):
        return f'SPLIT {self.type} {self.attr} {self.gain} {self.t}'


Split.NULL = Split( None, None, None, 0, None )


#Given a dataframe, possible attributes to split on, target atribute,
#spit out the best split
@Factory
class Splitter:
    def __init__(self, df, attributes, target):
        
        self.df = df
        self.target = target

        self.attributes = attributes
        self.entropy = self.H( df )


    # build a list of probabilities of getting a specific value for target
    # return a series of probs
    def get_probs(self, partition):

        total = partition.shape[0]
        counts = partition[self.target].value_counts()
        probs = counts / total

        return probs
    
    #entropy function
    def H( self, partition ):
        entropy = 0

        probs = self.get_probs( partition )

        for p in probs:
            try:
                entropy += p * log2(p)
            except:
                continue

        return -entropy

    def entropy_gain(self, partitions):
        total = 0
        for partition in partitions.values():
            total += partition.shape[0]

        sum = 0
        for partition in partitions.values():
            sum += (partition.shape[0]/total) * self.H( partition )

        return self.entropy - sum


    # # # # # # # # # # # # # # # 

    def numeric_partition( self, attr, t ):
        lt = self.df[ self.df[ attr ] < t]
        gt = self.df[ self.df[ attr ] >= t ]
        return { '<': lt, '>': gt }

    #pick the best numeric split by considering split 'QUANTILES' amount
    #of equidistant split-points
    def numeric_split( self, attr ):

        min_val = self.df[ attr ].min()
        max_val = self.df[ attr ].max()

        delta = (max_val - min_val) / QUANTILES

        partitions = None
        gain       = 0
        t          = None

        for i in range( 1, QUANTILES ):
            _t = min_val + delta * i
            _partitions = self.numeric_partition( attr, _t )

            _gain = self.entropy_gain( _partitions )

            if _gain > gain:
                gain = _gain
                partitions = _partitions
                t = _t

        return Split( 'numeric', attr, partitions, gain, t )


    def categorical_split(self, attr):

        vals = self.df[attr].unique()
        partitions = {}

        for val in vals:
            partitions[ val ] = self.df[ self.df[attr] == val ]

        gain = self.entropy_gain( partitions )
        
        return Split( 'categorical', attr, partitions, gain )

    # # # # # # # # # # # # # # # # # #

    def splitter(self):
        # for every attribute different than the target create a split object according to it's type
        #for attr in self.df.columns
        splits = {}
        
        for attr in self.attributes:
            if is_numeric_dtype( self.df[attr] ):
                splits[attr] = self.numeric_split( attr )
            elif is_string_dtype( self.df[attr] ):
                splits[attr] = self.categorical_split( attr )
            else:
                raise Exception( 'SPLITTER: unhandled attr type' )

        #dummy variable so iteration is nice and clean
        split = Split.NULL
        for _split in splits.values():
            if _split.gain > split.gain:
                split = _split

        if split == Split.NULL:
            return None
        return split




# # # # # # # # # # # # # # # # # # # # 



#Nodes of the decision tree
class Node:
    def __init__(self, split:Split, parent=None):
        self.parent = parent

        self.attr = split.attr
        self.children = {}
    
    #given data, return the predicted classifier by recursive calls
    #to children with attribute value in the data
    def klassify(self, data):
        pass

    def add_child(self, key, child):
        self.children[key] = child

class NumericNode(Node):
    def __init__(self, split:Split):
        super().__init__(split)
        self.t = split.t

    def klassify(self, data):
        val = data[ self.attr ]
        if val >= self.t:
            return self.children[ '>' ].klassify(data)
        else:
            return self.children[ '<' ].klassify(data)

class CategoricalNode(Node):
    def __init__(self, split:Split):
        super().__init__(split)
    
    def klassify(self, data):
        val = data[ self.attr ]
        return self.children[ val ].klassify( data )


#in retrospect, this is a werid idea
class TerminalNode(Node):
    def __init__(self, klass):
        self.klass = klass
        self.children = {}
    
    def klassify(self, *args):
        return self.klass

    def add_child(self):
        pass


#recursive tree builder
#for given data, check termination conditions
#if satisfied, get the best split

def builder(df, attributes, target):
    
    #termination conditions
    if df.empty:
        return None
    elif df[target].unique == 1:
        klass = df[target].unique[0]
        return TerminalNode( klass )
    elif attributes.empty:
        klass = df[target].value_counts().idxmax()
        return TerminalNode( klass )


    split = Splitter( df, attributes, target )

    #if all splits are shite return None for the parent function call
    #to take care of it
    if not split:
        return None

    attrs = attributes.drop( split.attr )

    #build the actual node according to attr type
    node = None
    if split.type == 'numeric':
        node = NumericNode( split )
    elif split.type == 'categorical':
        node = CategoricalNode( split )

    #build node's children by recursive calls to builder
    #if the call returns None, build a termination node
    #returning a plurality value of corresponding partition
    for key, partition in split.partitions.items():

        child = builder( partition, attrs, target )
        if not child:
            klass = df[target].value_counts().idxmax()
            child = TerminalNode( klass )

        node.add_child( key, child )

    return node

