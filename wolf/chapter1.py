'''
Here's a problem: 2.53 from "Introduction to Probability" by Blitzstein, Hwang:

"There are 100 equally spaced points around a circle, at 99 of the points, there are sheep, and at 1 point, there is a wolf.
At each time step, the wolf randomly moves wither clockwise or counterclockwise by 1 point. If there is a sheep at that point, he eats it.
The sheep don't move. What is the probability that the sheep who is initially opposite of the wolf is the last one remaining."

This is an example of a "Gambler's ruin" problem. Issue is, during devouring the contents of the book, this class of problems proved to be
especially problematic to me. Even worse - the pdf with solutions didn't include the answer to this one.

So, I don't even have a concrete answer which would guide the reasoning process. 
If I could only get a rough estimate for the answer, by putting a ridicolous amount of work into this 3 line problem...

In fact, to make it even more fun, let's solve a slightly more general problem: finding the probability in question
for all even number of points = N.
Here's the strategy:
    (1) write a function generating test cases for given N
    (2) for given N, generate M test cases, count number S of succesful cases
    (3) S/M will be an approximation of the probability in question for N by naive definition of probability
    (4) do this for all even N less than some MAX_N
    (5) plot the data, formulate a guess as to what type of a fairly straightforward function (ln x, 1/x, x^2, etc.)
        describes plot's shape the best
    (6) functions parameters are still unclear, as in the general shape may be described by ln x, but is it 2*ln(x)? Is it 5*ln(x) + 1023?
        Hence, fit the function to the data using regression
    (7) ???
    (8) profit
    

This file visualizes step (1). I wanted to actually see if the generator does what it's supposed to.

If the wolf eats the opposite sheep (index N/2) last, the test is succesful, returning True. Otherwise, it is False.
Result of each case is logged in the terminal.

Also, feel free to tweak to the N right below. I know it'll take You no time to break the whole thing.
Might as well just accept it.
'''
N = 100
#tweak the parameters to accomodate different N



import math
import pygame
pygame.init()

RADIUS = 10
FONT_SZ = RADIUS

WIN_SZ = pygame.Vector2( 1500, 850 )
display = pygame.display.set_mode( WIN_SZ )
font = pygame.font.Font("Helvetica.ttf", FONT_SZ)
clock = pygame.time.Clock()

color = {
    'black' : '#000000',
    'white' : '#FFFFFF',
    'red'   : '#DD0000'
}

def rand( a ):
    from random import randint
    return randint( 0, a-1 )

def gen( n ):

    wolf = 0
    opposite = n//2

    eaten = [False for i in range( n )]
    eaten[wolf] = True

    eaten_num = 1

    
    center = WIN_SZ//2
    R = min( WIN_SZ.x - RADIUS*2, WIN_SZ.y-RADIUS*2 ) // 2

    while True:

        #visualization
        display.fill( color['black'] )
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.QUIT()

        for i in range( n ):
            angle = (2*math.pi / n) * i

            x = R * math.cos( angle ) + center.x
            y = R * math.sin( angle ) + center.y

            if i == wolf:
                pygame.draw.circle( display, color['red'], (x,y), RADIUS)
            else:
                col = color['black']
                if eaten[i]:
                    pygame.draw.circle( display, color['white'], (x,y), RADIUS, 2)
                    col = color['white']
                else:
                    pygame.draw.circle( display, color['white'], (x,y), RADIUS)
                
                text = font.render( f'{i}', True, col )
                text_w, text_h = font.size( f'{i}' )
                display.blit( text, (x - text_w//2, y - text_h//2) )

        pygame.display.update()
        clock.tick(10)

        #case logic
        
        #roll for a move
        if rand(2) == 0:
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


while True:
    print(gen( N ))


