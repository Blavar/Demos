'''
Oh my...
It's a working project

Basic idea is pretty simple. I wanted the program to differentiate a given formula, and I wanted to write the differentiation
rules as strings for the program to interpret. So pretty much a goal tree.
The general idea for the goal tree I owe to this lecture:
https://www.youtube.com/watch?v=TjZBTDzGeGg&list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi&index=1

First things first, this required the program to parse the input (parser.py)
then from the tokens build a tree-structure of the formula (formulate.py). Nodes can be either functions, operators, constants or variables.
Operator and function nodes can have children - nodes representing arguments, which in turn can have their children, and so on, and so on *sniff*

After that, to differentiate a formula:
(1) for every differentiation (diff) rule of the form antedecent : consequent, check if the antedecent schema matches with the formula
(2) if there's a match, obtain a symbol table (symtab), which describes which formula nodes 
    correspond to which variable names in the rule antedecent schema
(3) using the symtab, substitute the nodes into the corresponding names in the consequent schema

So, the big components needed are:
(1) checking for matches between a formula and a schema
(2) getting a symtab
(3) substituting according to the symtab


In current form it works in specific cases.
Future versions ought to implement a formula class, which reperesents nodes in the formula, which in turn can be complex, or atomic.
Each fromula then will have a pointer to a 'content' node, which can be a concrete function symbol, operator, variable, or numerical value.

Right now the program doesn't make this crucial distictions, which caused be a bit of headache.
'''



from common import *
from formulate import formulate

#builder for the symbol table (usually for a schema)
#produces side-effects, but they're contained to build_symtab, so that's cool
def symtab_builder(schema, symtab):

    if schema.val in functions or schema.val in operators and schema.type != 'num':
        pass
    else:
        symtab[ schema.val ] = None
    
    for child in schema.children:
        symtab_builder( child, symtab )

#entry point for building symtabs
def build_symtab( schema ):
    symtab = {}
    symtab_builder( schema, symtab )
    return symtab



#compare if formulas are EXACTLY the same
def compare( a, b ):

    if a.type == b.type and a.val == b.val and len( a.children ) == len( b.children ):

        if len( a.children ) > 0:
            if a.val == '+' or a.val == '*':
                p = compare( a.children[0], b.children[0] ) and compare( a.children[1], b.children[1] ) 
                q = compare( a.children[0], b.children[1] ) and compare( a.children[1], b.children[0] )
                return p or q
            else:
                for i in range( len(a.children) ):
                    if not compare( a.children[i], b.children[i] ):
                        return False
    else:
        return False

    return True



#if symtabs are compatible merge them, if there's a conflict or some key in anacounted for, return None
def merge_symtabs( symtabs ):

    if len( symtabs ) == 1:
        return symtabs[0]

    for tab in symtabs:
        if not tab:
            return None

    res = {}
    for key in symtabs[0].keys():
        
        t = None
        for symtab in symtabs:
            if t == None and symtab[key]:
                t = symtab[key]
            elif t and symtab[key] and not compare(t, symtab[key]):
                return None

        res[key] = t

    return res



#try to build a mapping between a formula and a schema
#if something doesn't match, or if there's a conflict, return None
def mapping_builder( form, schema, symtab ):


    if not schema.children:

        if schema.type == 'var' or ( schema.type == form.type ):
            if not symtab[schema.val]:
                symtab[schema.val] = form
            else:
                if not compare( symtab[schema.val], form ):
                    symtab = None
        
    elif schema.children and len( schema.children ) == len( form.children ):

        if (schema.type == 'func' and not schema.val in functions and (form.type == 'func' or form.type == 'operator')):
            if not symtab[schema.val]:
                node = Node()
                node.type = 'func'
                node.val = form.val
                symtab[schema.val] = node
            else:
                if not compare( symtab[schema.val], form ):
                    return None    
        elif schema.val == form.val:
            pass
        else:
            return None

        if schema.val == '+' or schema.val == '*':
            tab1 = mapping_builder( form.children[0], schema.children[0], dict(symtab) )
            tab2 = mapping_builder( form.children[1], schema.children[1], dict(symtab) )

            tab3 = mapping_builder( form.children[0], schema.children[1], dict(symtab) )
            tab4 = mapping_builder( form.children[1], schema.children[0], dict(symtab) )
            
            merged1 = merge_symtabs( [symtab, tab1, tab2] )
            merged2 = merge_symtabs( [symtab, tab3, tab4] )

            if merged1:
                symtab = merged1
            elif merged2:
                symtab = merged2
            else:
                symtab = None
        else:

            tabs = [symtab]
            for i in range(len( schema.children )):
                tabs.append( mapping_builder( form.children[i], schema.children[i], dict(symtab) ) )
            symtab = merge_symtabs( tabs )

        if (schema.type == 'func' and not schema.val in functions and (form.type == 'func' or form.type == 'operator')):

            if not type(symtab[schema.val]) is str:
                symtab[schema.val] = form
            else:
                if not compare( symtab[schema.val], form ):
                    return None    


    return symtab

#entry point for building a mapping
def build_mapping( form, schema ):
    res =  mapping_builder( form, schema, build_symtab( schema ) )
    if res:
        for key, val in res.items():
            if val == None:
                return None

    return res


#substitution
#given a formula and a dictionary, substitute into it
#creates side effects mind you
def substitute( schema, symtab ):

    if not schema.children:
        return symtab[ schema.val ]
    elif schema.children:
        res = Node()
        res.val = schema.val
        res.type = schema.type

        if schema.type == 'func' and not schema.val in functions:
            res.val = symtab[schema.val].val
        for child in schema.children:
            res.children.append(substitute( child, symtab ))

        return res
        
        pass


rules_buf = {
    ' D( [x:var], [x:var] ) ' : '[c:const]',
    ' D( a + b, x) ' : 'D(a,x) + D(b,x)',
    ' D( a*x^b, x ) ' : ' (a*b)*x^(b-1) ',
    ' D( a*y^b, x ) ' : ' (a*b)*y^(b-1) ',
    ' D( [f:func](y)*g[func](y), x ) ' : ' D( [f:func](y), x ) * [g:func](y) + [f:func](y)*D( [g:func](y), x ) ',
    ' D( sin([x:var]), x )' : 'cos(x)',
    ' D( [f:func]( [g:func](x) ), x ) ' : ' D( [f:func]([g:func](x)), [g:func](x) ) * D( [g:func](x), x ) '
    # ' D( [x:func] + [y:func] ) ' : ' D(x) + D(y) ',
    # ' D( x - y)' : 'D(x) - D(y)',
    # ' D([c:const])' : '0',
    # ' D( [c:const] * x ) ' : ' [c:const] * D(x) ',
    # ' D( x * y )' : 'D(x)*y + x*D(y)',
    # ' D( [f:func]( [g:func] ) ) ' : ' (D([f:func]))([g:func]) ',
    # ' D(sin([x:var])) ' : 'cos(x)',
    # ' D([x:var]^[y])' : ' y*[x:var]^(y-1) '
}

#construct pairs of tree for every rule
rules = []
for key, val in rules_buf.items():
    rules.append( (formulate( key ), formulate( val )) )

#helper to construct a symtab for keys in both ante and cons
def rule_tab( ante, cons ):
    antetab = build_symtab( ante )
    constab = build_symtab( cons )
    res = {}
    for key in antetab.keys():
        res[key] = None
    for ket in constab.keys():
        res[ket] = None

    return res

#generate a random label for a constant
#not pretty, but was useful to see if the jist of it works
#before inevitable reimplementation
def rand_label(  ):
    from random import choice
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''.join(choice(chars) for i in range(3) )
    return res



def derivative( form ):

    res = form

    if form.val == 'D':
        for ante, cons in rules:

            symtab = build_mapping( res, ante )
            if symtab:

                antetab = build_symtab( cons )
                for key in antetab.keys():
                    if not key in symtab.keys():
                        symtab[key] = formulate( f'[{rand_label()}:const]' )


                res = substitute( cons, symtab )
                break
        

        if res and res.val != 'D' and res.children:
            form = res
            for i, child in enumerate(res.children):
                res.children[i] = derivative( child )


    return res
    


formstr = ' D(  sin(cos(x)), x) '

res = derivative( formulate( formstr ) )
print(res)

