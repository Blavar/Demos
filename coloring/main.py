'''
A visualized algorithm for a constraint satisfaction problem of coloring a map,
as presented and discussed by Patrick Winston:
https://www.youtube.com/watch?v=dARl_gGrS4o&list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi&index=8

Main idea is pretty simple:
The map is represented as a graph.
In order to relaiably generate different test case, a W x H grid is created,
N points are randomly chosen, marking the 'capitals' of a region.
The regions then expans from expand from every capital by means of BFS.

From that, a graph is generated by looking which regions neighboor each other.

For the solution itself: the nodes are sorted in decreasing order of number of constraints i.e. number of neighboors.
The main algorithm tracks how many colors each region can yet be colored with (keeps track of its' domain),
by means of dictionary of the form  {region : domain}.
At first domains are maximal, as in every color is possible for every node.
The main recursive function (strider) is invoked. It chooses the first non-determined (not left with one color in the domain) region,
and colors it with a random color from its' domain. Then it propagates the change, by means of BFS,
which for every neighboor of the considered region, deletes from the neighboor's domain a color which was
just used on the considered region. If the neighboor is left with just one color, do the same for it.
If it's left with no colors, or its' color conflicts with its' neighboors, 
we have a contradiction and gotta back up to the previous instance of strider.

Algorithm is a DFS, so the first solution it finds it will return immediately.
If not solution is found, it return None
'''
import pygame

pygame.init()

'''
Feel free to play around with these

Max number of colours is 8, because I only bothered to hard-code that many distinct ones
'''
NODES_NUM = 100
COLORS_NUM = 4
FPS = 60

'''
Also, animation can get pretty costly. Firstly, because the animation process here ain't exactly cheap or optimized.
Secondly... because it's Python, come on.
Anyway, set this to False if You just wanna see the result
'''
ANIMATE = True


#pick n random elements from a list
def pick( lis:list, n:int ):
    from random import randint as rand

    res = lis[:]
    l = len(res)

    for i in range(n):
        k = rand( i, l-1 )
        res[i], res[k] = res[k], res[i]

    return res[:n]

#return coordinates adjacent to the given
def adj_to(i, j):
    return [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]

#Build a 2D grid, generate n random points, propagate from them with BFS
class Grid:
    def __init__(self, n, w, h):
                
        self.n = n
        self.w = w
        self.h = h

        self.UNCLAIMED  = -1
        self.centers    = None
        self.grid       = [[self.UNCLAIMED for i in range(self.w)] for j in range(self.h)]

        self.pick_centers()
        self.gen()

    def __getitem__(self, i):
        return self.grid[i]

    def inbounds(self, i, j):
        return i >= 0 and i < self.w and j >= 0 and j < self.h

    def pick_centers(self):

        pool = []
        for i in range( self.w ):
            for j in range( self.h ):
                pool.append( (i,j) )

        self.centers = pick( pool, self.n )

    def gen(self):

        for k in range( self.n ):
            i, j = self.centers[k]
            self[j][i] = k

        q = self.centers[:]
        while q:
            
            i, j = q.pop(0)
            for k, l in adj_to(i,j):

                if self.inbounds(k, l) and self[l][k] == self.UNCLAIMED:
                    self[l][k] = self[j][i]
                    q.append((k,l))        

    def __repr__(self):

        res = ''
        for j in range( self.h ):
            for i in range( self.w ):
                t = self[j][i]
                if t == self.UNCLAIMED:
                    res += '.'
                else:
                    res += str( t )
            res += '\n'

        return res


#Class of a node, also containing information about its' graphical representation for simplicity
class Elem:
    def __init__(self, key):
        self.key = key

        self.center = None
        self.cells = []
        self.border = None

class Graph:
    def __init__(self, n, nodes, adj ):
        
        self.n = n
        self.nodes = nodes
        self.adj = adj

# # # # # # # # # # # # # # # # # # # # # # # # # # 

#Given a grid generate a graph
class Generator:

    def __init__(self, n, w, h, WIN_SZ, CELL_SZ):
        
        self.grid = Grid( n, w, h )
        self.WIN_SZ  = WIN_SZ
        self.CELL_SZ = CELL_SZ

        self.n = n
        self.adj = [[False for i in range(self.n)] for j in range(self.n)]
        self.nodes = [Elem(i) for i in range(self.n)]

        self.build_adj()
        self.build_vis()

    def build(self):
        return Graph( self.n, self.nodes, self.adj )

    #build the adjacency matrix fot th graph
    def build_adj(self):

        grid = self.grid

        for j in range( grid.h ):
            for i in range( grid.w ):

                for k, l in adj_to( i, j ):
                    if grid.inbounds( k, l ): 
                        
                        key = grid[j][i]
                        adj_key = grid[l][k]

                        if key != adj_key:
                            self.adj[key][adj_key] = True
                            self.adj[adj_key][key] = True

        for i in range( self.n ):
            self.adj[i] = [ j for j in range( self.n ) if self.adj[i][j] == True ]


    #build the visualization objects for the graph
    def build_vis(self):
        
        def pos(i, j):
            return ( i * self.CELL_SZ, j * self.CELL_SZ )

        grid = self.grid
        #build node border objects
        for i in range( self.n ):
            cx, cy = grid.centers[i]
            self.nodes[i].center = pygame.Rect(pos( cx, cy ), (self.CELL_SZ, self.CELL_SZ ))
            self.nodes[i].border = pygame.Surface( self.WIN_SZ, pygame.SRCALPHA )

        #iterate over every cell, check every adj
        for j in range(grid.h):
            for i in range(grid.w):

                #add rect, check borders
                key = grid[j][i]
                self.nodes[ key ].cells.append( pygame.Rect( pos(i,j), (self.CELL_SZ, self.CELL_SZ) ) )

                lines = []

                if not grid.inbounds( i-1, j ) or (self.grid[j][i] != self.grid[j][i-1]):
                    lines.append( (pos(i, j), pos(i, j+1)) )

                if not grid.inbounds( i+1, j ) or self.grid[j][i] != self.grid[j][i+1]:
                    lines.append( (pos(i+1, j), pos(i+1, j+1)) )

                if not grid.inbounds( i, j-1 ) or self.grid[j][i] != self.grid[j-1][i]:
                    lines.append( (pos(i, j), pos(i+1, j)) )

                if not grid.inbounds( i, j+1 ) or self.grid[j][i] != self.grid[j+1][i]:
                    lines.append( (pos(i, j+1), pos(i+1, j+1)) )

                for p, q in lines:
                    pygame.draw.line( self.nodes[key].border, '#ffffff', p, q, 3)

# # # # # # # # # # # # # # # # # #


#Class managing drawing of the graph nodes
#Affectionally named after Tony Sirico vel Paulie Walnuts for lack of a better idea
#or judgement for that matter
class Walnuts:
    def __init__(self, WIN_SZ, CELL_SZ):
        self.WIN_SZ = WIN_SZ

        self.display = pygame.display.set_mode( WIN_SZ )
        self.font_sz = CELL_SZ // 2
        self.font = pygame.font.Font( 'Helvetica.ttf', self.font_sz )
        
        #size of rectangle showing available colors
        self.sub_sz = 10

        self.clock = pygame.time.Clock()
        self.fps   = FPS



    def draw_node( self, node, domain):
        
        center = node.center

        if len( domain ) == 1:
            col = domain[0]
            for cell in node.cells:
                pygame.draw.rect( self.display, col, cell )
        else:
            for i, col in enumerate( domain ):
                rect = pygame.Rect( center.x + self.sub_sz * i, center.y + self.font_sz, self.sub_sz, self.sub_sz)
                pygame.draw.rect( self.display, col, rect )    
            

        self.display.blit( node.border, (0,0) )

        text = self.font.render( f'{node.key}', False, '#ffffff' )
        self.display.blit( text, center )



    def update(self, nodes, domains):
        self.display.fill( '#000000' )
        if ANIMATE:
            self.clock.tick( self.fps )
        for node in nodes:
            self.draw_node( node, domains[node.key] )

        pygame.display.update()


# # # # # # # # # # # # # # # # # #


#Generate a solution 
#Also includes a reference to Paulie in order to draw subsequent steps of the algorithm
class Solution:
    def __init__(self, graph, Paulie, domain):

        self.graph = graph
        self.Paulie = Paulie
        self.domain = domain

        #sort the nodes from most to least constrained
        self.nodes = sorted( self.graph.nodes, key = lambda node: len( self.graph.adj[node.key] ), reverse=True)
        self.nodes = [node.key for node in self.nodes]

        #construct the table of domains for the nodes
        self.domains = {}
        for node in self.nodes:
            self.domains[node] = self.domain[:]

        res = self.strider( self.domains )

        if res:
            Paulie.update( self.graph.nodes, res )
        else:
            domains = {}
            for node in self.nodes:
                domains[node] = []
            Paulie.update( self.graph.nodes, domains )

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
            
     

    
    #copy the 
    def copy(self, domains):
        res = {}
        for key, item in domains.items():
            res[key] = item[:]

        return res

    def check(self, node, domains):
        for adj in self.graph.adj[node]:
            if len( domains[adj] ) == 1 and domains[adj][0] == domains[node][0]:
                return False
        
        return True


    #check if constraints are satisfied
    #starting from the node, update every adj
    #if adj is left with no colors, return None
    #if adj is left with one color, propagate from it
    #draw every propagation step
    def propagate(self, _node, domains):


        q = [_node]

        while q:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()

            #node is guaranteed to have a single item in the domain by the loop invariant
            #node is guaranteed to have no conflicts in itself
            node = q.pop(0)
            node_dom = domains[node][0]

            for adj in self.graph.adj[node]:

                adj_dom = domains[adj]
                if node_dom in adj_dom:
                    adj_dom.remove( node_dom )

                    if len( adj_dom ) == 1:
                        if self.check( adj, domains ):
                            q.append( adj )
                        else:
                            return None
                    elif len( adj_dom ) == 0:
                        return None
                
                if (ANIMATE and adj_dom) or not adj_dom:
                    self.Paulie.update( self.graph.nodes, domains )

        return domains


    #main recursive function for the solution
    #strider, as in depth-strider, depth-first, get it?
    def strider(self, domains):

        node = None
        for _node in self.nodes:
            if len(domains[_node]) > 1:
                node = _node
                break
            
        if node == None:
            return domains

        res = []
        for col in domains[node]:
            
            subdomain = self.copy(domains)
            subdomain[node] = [col]
            subdomain = self.propagate( node, subdomain.copy() )

            if subdomain:
                subdomain = self.strider( self.copy(subdomain) )
            if subdomain:
                return subdomain


# # # # # # # # # # # # # # # # # #


colors = [ '#881d42', '#d7ae2e', '#36c873', '#2d62e7', '#a133b5', '#f4f152', '#15cb3c', "#48ebfa" ]

CELL_SZ = 10
win_sz = (1000, 850)


W = win_sz[0] // CELL_SZ
H = win_sz[1] // CELL_SZ


graph = Generator( NODES_NUM, W, H, win_sz, CELL_SZ ).build()
Paulie = Walnuts( win_sz, CELL_SZ )

s = Solution( graph, Paulie, colors[:COLORS_NUM] )
