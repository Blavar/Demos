'''
Having a token list, build a formula tree made of nodes, which can be either:
    a function with children( its arguemnts )
    an operator  -|-
    a variable
    a number
    an argument node, specially marked, which contains argument to pass to the function

Firstly divide the token list into nested lists according to parentheses
Recursively invoke 'build' function which:
    if the tokens include ':', the list is an type declaration, do it
    if they include ',', formulate the arguemnts, return the args node with arguments as children

then:
    checks if any token in the list is a list, if so, formulate it first
    otherwise, make a node from given token

Now, the algorhitm works a bit like union find. By which i mean, similarity is marginal
Every node start with no parent, which indicates it's not included in any subtree
for every function symbol and operator which don't have children (are unchecked), get the roots of neighbooring node/s
Getting the root is equivalent to finding the node which is the root of the already formulated tree to which the node belongs
Attach the roots as children to currently considered node

At the end, check which node doesn't have a parent, which mean that this node is the main function symbol/operator
in the formula, i.e. it's the root

Return the root

'''
from common import functions, operators
from parser import parse


class Node:
    def __init__(self):
        self.type     = None
        self.val      = None
        self.parent   = None
        self.children = []

    def add_child( self, node ):
        self.children.append( node )
        node.parent = self

    def __repr__(self):
        res = ''

        if self.type == 'func':

            res += self.val
            if self.children:
                res += '('
                for child in self.children:
                    res += str(child) + ','
                res = res[:-1] + ')'

        elif self.type == 'operator':
            if self.children:
                res += '(' + str(self.children[0]) + ' ' + str(self.val) + ' ' + str(self.children[1]) + ')'
            else:
                res += str(self.val)

        else:
            res += str(self.val)


        return res


#group token to nested lists according to parentheses
def capsule( tokens:list ):

    stack = []
    caps = []

    for token in tokens:
        if token == '(' or token == '[':
            stack.append( caps[:] )
            caps = []
        elif token == ')' or token == ']':
            ubercaps = stack.pop()
            ubercaps.append(caps)
            caps = ubercaps
        else:
            caps.append(token)

    return caps


def token_node( token:str ):

    node = Node()
    node.val = token

    if token.isnumeric():
        node.val = float(token)
        node.type = 'num'
    elif token in functions:
        node.type = 'func'
    elif token in operators:
        node.type = 'operator'
    else:
        node.type = 'var'

    return node

def typed_node( tokens:list ):

    node = Node()
    node.val = tokens[0]
    node.type = tokens[2]

    return node

def args_node( tokens:list ):

    root = Node()
    root.type = 'args'
    root.val  = 'args'

    arg = []
    for token in tokens:

        if token == ',':
            root.add_child( build( arg ) )
            arg = []
        else:
            arg.append( token )

    root.add_child( build( arg ) )

    return root



def root_of(node):
    res = node
    while res.parent:
        res = res.parent
    return res

#build the formula tree
def build( tokens:list ):

    if len( tokens ) == 1:
        if type( tokens[0] ) is list:
            return build( tokens[0] )
        else:
            return token_node( tokens[0] )

    for token in tokens:
        if token == ':':
            return typed_node( tokens )
        elif token == ',':
            return args_node( tokens )

    nodes = []

    for i, token in enumerate( tokens ):
        if type(token) is list:
            if i > 0 and nodes[i-1].type == 'func':

                nodes.append( args_node( token ) )

            else:
                nodes.append( build(token) )
        else:
            nodes.append( token_node(token) )


    for func in functions:
        for i, node in enumerate(nodes):

            if node.type == 'func' and i+1 < len( nodes ) and nodes[i+1].type == 'args' and not nodes[i+1].parent:
                args = nodes[i+1]

                for child in args.children:
                    node.add_child( child )

                args.parent = node

    
    for opp in operators:
        for i, node in enumerate( nodes ):
            if node.val == opp and not node.parent and not node.children:

                left_root = root_of( nodes[i-1] )
                right_root = root_of( nodes[i+1] )

                node.add_child( left_root )
                node.add_child( right_root )

    for node in nodes:
        if not node.parent:

            return node


#entry point for buulding a formula tree from input
def formulate( buf:str ):
    return build( capsule( parse(buf) ) )

