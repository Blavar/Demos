'''
My first visualization of linear regression. Done based on following resorces: 
https://mlu-explain.github.io/linear-regression/
https://www.geeksforgeeks.org/ml-linear-regression/

MLU especially is a wonderful thing.

My implementation doesn't exactly differ fromt he abovementioned resources due to the straightforwardness of the thing.
Which is why my friend was really adamant in accusing me of copy/pasting. Yes I am still salty.

You can add points by clicking.
'''


import pygame
from random import randint as rand


class Model:
    def __init__( self, data ):

        import random

        self.data = data
        self.w    = [ random.uniform( -100, 100 ), random.uniform( -10, 10) ]

    def add_data( self, data ):
        self.data.append( data )

    def gradient_descent(self, lr):
        
        data = self.data
        n = len( data )
        
        w = self.w
        terms_dw0 = [ data[i][1] - ( w[0] + w[1] * data[i][0] ) for i in range( n ) ]
        terms_dw1 = [ terms_dw0[i] * data[i][0] for i in range(n) ]

        dw0 = -(2/n) * sum( terms_dw0 )
        dw1 = -(2/n) * sum( terms_dw1 )

        w[0] = w[0] - lr*dw0
        w[1] = w[1] - lr*dw1



WIN_SZ = ( 1500, 850 )
DATA_N = 20

data = [ ( rand(0, WIN_SZ[0]//2), rand(0, WIN_SZ[1]//2) ) for i in range(DATA_N) ]

model = Model(data)


pygame.init()

display = pygame.display.set_mode( WIN_SZ )
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(10)
    display.fill( '#000000' )

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            data.append( pygame.mouse.get_pos() )

    #draw a circle where every point is
    for point in data:
        pygame.draw.circle( display, '#AA0000', point, 5, 2 )

    model.gradient_descent( 0.000001 )

    #draw the line
    p = (0, model.w[0])
    q = (WIN_SZ[0], model.w[0] + model.w[1] * WIN_SZ[0]  )
    pygame.draw.line( display, '#AA0000', p, q, 2)

    pygame.display.update()