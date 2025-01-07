'''
Axis-aligned rectangle collision detection and resolution algorithm visualization.
[Flex] I NEARLY got it right myself, but ultimately had to resolve to getting help from here:
https://www.youtube.com/watch?v=8JJ-4JgR7Dg

Keep in mind this code is relatively old and hence gruesome. I decided to put it up here nonetheless.
'''


import pygame.freetype
from vector import Vector

class Line:
    def __init__(self, p, q):
        self.p = p
        self.q = q

class Rect:
    def __init__(self, x=0, y=0, w=0, h=0, v=Vector(0,0)):
        self.set( x, y, w, h )
        self.v = v

    def set(self, x, y, w, h):
        self.pos = Vector(x, y)
        self.size = Vector(w, h)

    def to_tuple(self):
        return (self.pos.x, self.pos.y, self.size.x, self.size.y)
    
    def __str__(self):
        return f'x:{self.pos.x} y:{self.pos.y}\nw:{self.size.x} h:{self.size.y}\nv: {self.v}'

    def center(self):
        return Vector( self.pos.x + self.size.x//2, self.pos.y + self.size.y//2 )

##########################

class Collision:
    def __init__(self, norm, t):
        self.norm = norm
        self.t    = t

##########################


def DrawV(rect: Rect):
    DrawLine( display, '#0000FF', rect.center(), rect.center() + rect.v*4 )

#######################################



def DrawLine(display, color, p: Vector, q: Vector):
    pygame.draw.line( display, color, p.to_pair(), q.to_pair() )

#in a class DrawRect(rect, col="smth")
def DrawRect(display, color, rect:Rect):
    pygame.draw.rect( display, color, rect.to_tuple(), 2 )


import pygame
pygame.init()

win_sz = Vector(1000, 500)
display = pygame.display.set_mode( win_sz.to_pair() )




def ray_rect(p, v, rect: Rect):
    
    if v.x == 0 and v.y == 0:
        return None



    near = Vector()
    far  = Vector()
    if v.x != 0:
        near.x = (rect.pos.x - p.x) / v.x
        far.x  = (rect.pos.x + rect.size.x - p.x) / v.x

    if v.y != 0:
        near.y = (rect.pos.y - p.y) / v.y
        far.y  = (rect.pos.y + rect.size.y - p.y) / v.y

    if near.x > far.x:
        near.x, far.x = far.x, near.x
    if near.y > far.y:
        near.y, far.y = far.y, near.y


    norm = None
    t = None

    if v.x == 0:

        if p.x > rect.pos.x and p.x < rect.pos.x + rect.size.x:
            if p.y < rect.pos.y:
                norm = Vector( 0,-1 )
            else:
                norm = Vector( 0,+1)
            t = min( near.y, far.y )
            if 0 <= t and t <= 1:
                return Collision( norm, t )
            else:
                return None
        else:
            return None
    if v.y == 0:
 
        if p.y > rect.pos.y and p.y < rect.pos.y + rect.size.y:
            if p.x < rect.pos.x:
                norm = Vector( -1,0)
            else:
                norm = Vector( +1,0)
            t = min( near.x, far.x )
            if 0 <= t and t <= 1:
                return Collision( norm, t )
            else:
                return None
        else:
            return None




    if not( near.x <= far.y and near.y <= far.x):
        return None

    if near.x >= near.y:
        t = near.x
        if p.x <= rect.pos.x:
            norm = Vector(-1,0)
        elif p.x >= rect.pos.x + rect.size.x:
            norm = Vector(+1,0)
    elif near.x <= near.y:
        t = near.y
        if p.y <= rect.pos.y:
            norm = Vector( 0,-1)
        elif p.y >= rect.pos.y + rect.size.y:
            norm = Vector( 0,+1)


    if 0 <= t and t <= 1:
        return Collision( norm, t )
    else:
        return None




def rect_rect(A: Rect, B: Rect):

    rect_dummy = Rect( B.pos.x - A.size.x/2, B.pos.y - A.size.y/2, B.size.x + A.size.x, B.size.y + A.size.y)

    DrawRect(display, '#222222', rect_dummy)
    DrawLine(display, "#00FF00", A.pos, A.pos+A.v*10)

    return ray_rect( A.center(), A.v-B.v, rect_dummy )

    
###########################



font = pygame.font.Font("Helvetica.ttf", 20)

clock = pygame.time.Clock()

black = "#000000"
white = "#FFFFFF"
red   = "#FF0000"
gray  = "#666666"

###########################



def gen_rect():
    from random import randint as rand

    margin_x = 100
    margin_y = 100

    dim = 50

    x = rand(0, win_sz.x - margin_x)
    y = rand(0, win_sz.y - margin_y)

    v = Vector( rand(0,2), rand(0,2) )

    return Rect( x, y, dim, dim, v )



walls = [Rect(0, 0, win_sz.x, 0), Rect(0,0,win_sz.y,0), Rect(win_sz.x,0,0,win_sz.y), Rect(0,win_sz.y,win_sz.x,0)]

Jigs = [gen_rect() for i in range(30)]

###########################

run = True
pause = False
while run:


    dt = clock.tick(120)
    dt /= 120
    #dt /= 240

    colors = [white for i in range(len(Jigs))]

    keys = pygame.key.get_pressed()

    #events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                pause = not pause
    

    if not pause:

        display.fill(black)

        for i in range( len(Jigs) ):
            jig = Jigs[i]

            dtdt = dt

            for j in range( i+1, len(Jigs)):

                jig2 = Jigs[j]

                collision = rect_rect( jig, jig2 )
                if collision:

                    colors[i] = red
                    colors[j] = red

                    jig.pos += jig.v * collision.t * (dt*0.99)
                    jig2.pos += jig2.v * collision.t * (dt*0.99)
                    
                    norm = collision.norm

                    if norm.x != 0:
                        jig.v.x, jig2.v.x = jig2.v.x, jig.v.x
                    elif norm.y != 0:
                        jig.v.y, jig2.v.y = jig2.v.y, jig.v.y

                    jig.pos += -jig.v*(1-collision.t)
                    jig2.pos += -jig2.v*(1-collision.t)

            #bounds
            if jig.pos.x < 0:
                jig.v.x *= -1
                jig.pos.x = 0 
            elif jig.pos.x + jig.size.x > win_sz.x:
                jig.v.x *= -1
                jig.pos.x = win_sz.x - jig.size.x
            elif jig.pos.y < 0:
                jig.v.y *= -1
                jig.pos.y = 0
            elif jig.pos.y + jig.size.y > win_sz.y:
                jig.v.y *= -1
                jig.pos.y = win_sz.y - jig.size.y

            jig.pos += jig.v
            

        for i, jig in enumerate(Jigs):

            DrawRect( display, colors[i], jig )
            text = font.render(f'{i}', True, black, white)
            display.blit( text, jig.pos.to_pair() )


        pygame.display.update()

