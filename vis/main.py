'''
I was playing around with a small framework (if you can call it that) for visualizing tree-like structures,
as apparently they tend to come up a lot in problems I tackle, and, You won't believe this,
but actually seeing if the structure behaves properly is a game changer. Must be why data visualization is a thing.

The main idea is pretty simple: given a tree structure consisting of node-like objects,
wrap each one in an Elem object (name borrowed from JS) - a graphical representation of the graph.
Elems can compute their position and siz recursively by parasiting on the node's properties

You'll also notice that the above paragraph is demonstrably lying, because in this implementation:
(1) a tree generating class is generating Elems from the get go, not Nodes,
(2) because of (1), Elems inherit from Node and invoke its' constructor

'''

import pygame
from random import random

class Node:
    def __init__(self, key=None):
        self.key = key
        self.val = None

        self.parent = None
        self.children = []

    def append(self, node):
        self.children.append(node)
        node.parent = self

    def depth(self, d=0):
        return max([d] + [ child.depth(d+1) for child in self.children ])

    def __repr__(self, d=0):
        res =  '   '*d + f'{self.key}:\n'
        for child in self.children:
            res += child.__repr__(d+1)
        return res
    

class Elem(Node):
    def __init__(self, key=None):
        self.rect = pygame.Rect(0, 0, 0, 0)
        super().__init__(key)
    
    def update(self, x, y, w, h):
        self.rect.update( x, y, w, h )

    def resize(self):
        if self.children:
            x, y, w, h = self.rect

            kw = w // len( self.children )
            for i, child in enumerate( self.children ):
                child.rect.update( x + kw*i, y + h, kw, h )
                child.resize()


class Tree:
    def __init__(self):
        self.root = None
        self.d    = None

    def depth(self, d = 0):
        self.d = self.root.depth()
        return self.d


#class generating a tree
class GenTree:
    def __init__(self, MAX_V = 30, MAX_D = 6, MAX_B = 3):

        self.MAX_V = MAX_V
        self.MAX_D = MAX_D
        self.MAX_B = MAX_B

        self.p = 0.7

        self.key = 0
    
    def gen( self, node:Elem, d=0):

        if d < self.MAX_D-1:
            for i in range( self.MAX_B ):
                if self.key < self.MAX_V-1 and random() < self.p:

                    child = Elem(self.key)
                    self.key += 1
                    
                    node.append(child)
                    self.gen( child, d+1 )


    def generate(self):
        root = Elem(self.key)
        self.key += 1
        self.gen(root)

        return root

#a display manager affectionately named after late Tony Sirico's character
#Is it an informative, verbose and intuitive? No
#But I don't know any know code reviewer who wouldn't want Paulie Walnuts to draw graph for them
#It cartainly helps my case that I don't know any code reviewers
class Paulie:
    def __init__(self, WIN_SZ, CELLH):
        self.surface = pygame.Surface( WIN_SZ )
        self.font = pygame.font.Font( 'Helvetica.ttf', CELLH//2 )

    
    def draw( self, node ):
        
        pygame.draw.rect( self.surface, '#666666', node.rect, 1 )
        
        text = self.font.render( str(node.key), False,  '#ffffff' )
        text_rect = text.get_rect( center = node.rect.center )
        self.surface.blit( text, text_rect )


        for child in node.children:
            self.draw( child )

# # # # # # # # # # # # # # # # # # # # # # # #

pygame.init()

WIN_SZ = (1500, 850)
CELL_H = 20

display = pygame.display.set_mode( WIN_SZ )


#number of vertices, maximal depth, maximal number of branches of the tree
#feel free to tweak them and presumably break the already non-flexible visualization
vertices = 30
depth = 6
branching = 3

#the following line is an abomination
root = GenTree( vertices, depth, branching ).generate()
print(root)

d = root.depth()
print(d)

CELL_H = WIN_SZ[1]//(d+1)

root.update( 0, 0, WIN_SZ[0], CELL_H )
root.resize()

paulie = Paulie( WIN_SZ, CELL_H )

run = True
while run:
    #run = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.QUIT()

    paulie.draw(root)
    display.blit( paulie.surface, (0,0) )
    pygame.display.update()

