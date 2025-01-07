'''
An implmentation of a minimax algorithm applied to tictactoe, as inspired by:
https://www.youtube.com/watch?v=5NgNicANyqM (1:14:34)

The only twist here is a function calculating score for each player,
which takes the line which are still valid (as in, only one player has marks there),
takes the difference of valid lines with n marks for the player and valid line with n marks for the opponent,
with n = 3,2,1
v = ( 3-lines, 2-lines, 1-lines )

'''

N     = None
lines = None

X = 'X'
O = 'O'
EMPTY = '.'

def gen():
    from random import randint as rand

    res = [[EMPTY for j in range(N)] for i in range(N) ]
    cells = []

    for i in range( N ):
        for j in range( N ):
            cells.append( (i, j) )

    count = rand( 0, 8 )

    for k in range( count ):
        if len(cells) > 1:
            t = rand(0, len(cells)-1)
        else:
            t = 0
        i, j = cells.pop(t)

        if k % 2 == 0:
            res[i][j] = X
        else:
            res[i][j] = O

    return res

def do_lines():
    res = []

    for i in range(N):
        
        line = []
        for j in range(N):
            line.append( (i, j) )
        
        res.append( line )

    for j in range(N):

        line = []
        for i in range(N):
            line.append( (i, j) )

        res.append( line )
    
    line = []
    for i in range(N):
        line.append( (i, i) )
    res.append( line )

    line = []
    for i in range(N):
        line.append( (i, (N-1)-i) )
    res.append( line )

    return res

def print_state(state):
    for i in range(N):
        print('> ', end='')
        for j in range(N):
            print(state[i][j], end='')
        print()

def to_state(s):
    res = [[None for j in range(N)] for i in range(N)]

    for i in range(N):
        for j in range(N):
            res[i][j] = s[N*i + j]
    
    return res

#++++++++++++++++++++++++


def get_score(state):
    
    res = [0 for i in range(N)]

    for line in lines:
        cnt_x = 0
        cnt_o = 0

        for i, j in line:
            if state[i][j] == X:
                cnt_x += 1
            elif state[i][j] == O:
                cnt_o += 1
        
        if cnt_x == 0 and cnt_o > 0:
            res[cnt_o-1] -= 1
        elif cnt_o == 0 and cnt_x > 0:
            res[cnt_x-1] += 1
    res.reverse()
    return res

def get_player(state):
    cnt_x = 0
    cnt_o = 0

    for i in range(N):
        for j in range(N):
            if state[i][j] == X:
                cnt_x += 1
            elif state[i][j] == O:
                cnt_o += 1
    
    if cnt_x == cnt_o:
        return X
    else:
        return O

def get_actions(state):

    res = []

    for i in range(N):
        for j in range(N):
            if state[i][j] == EMPTY:
                res.append( (i,j) )
    
    return res


def apply_action(state, action):
    res = [state[i][:] for i in range(N)]
    i,j = action
    res[i][j] = get_player(state)

    return res

def terminal(state):

    score = get_score(state)[0]
    if score != 0:
        return True
    
    for i in range(N):
        for j in range(N):
            if state[i][j] == EMPTY:
                return False
    
    return True 


def minimax(state):

    actions = get_actions(state)
    
    if actions:
        player = get_player(state)
        for action in actions:
            
            
            pass
        
        pass
    else:
        pass

    #return action + odds (X, Y)

def eq(a, b):
    for i in range(N):
        if not a[i] == b[i]:
            return False
    
    return True

def gt(a, b):
    for i in range(N):
        if a[i] > b[i]:
            return True
        elif a[i] < b[i]:
            return False
    
    return False

def fathom_min(state, d):

    if terminal(state):
        return (get_score(state), d)
        
    best = [20, 20, 20]
    res_d = d

    for action in get_actions(state):
        expected, _d = fathom_max( apply_action( state, action ), d+1 )
        if gt(best, expected):
            best = expected
            res_d = _d

    return (best, _d)

def fathom_max(state, d):

    if terminal(state):
        return (get_score(state), d)
        
    best = [-20, -20, -20]
    res_d = d

    for action in get_actions(state):
        expected, _d = fathom_min( apply_action( state, action ), d+1 )
        if gt(expected, best):
            best = expected
            res_d = _d


    return (best, res_d)


def predict(state):
    player = get_player(state)

    if player == X:
        best = [-20, -20, -20]
    elif player == O:
        best = [20, 20, 20]

    best_d = 20
    res = None

    for action in get_actions(state):

        expected = None

        if player == X:
            expected, d = fathom_min( apply_action( state, action ), 1 )
            if gt(expected, best):
                best = expected
                res = action
            elif eq(expected, best):
                if best_d > d:
                    best = expected
                    res = action
                    best_d = d


        elif player == O:
            expected, d = fathom_max( apply_action( state, action ), 1 )
            if gt(best, expected):
                best = expected
                res = action
            elif eq(expected, best):
                if best_d > d:
                    best = expected
                    res = action
                    best_d = d
    
    print(f'PREDICTED: {best}')
    return res


N = 3
lines = do_lines()

print( gt( [-1, 3, 0], [2, 0, 0] ) )

state = to_state('.........')

#state = gen()

run = True
if run:
    print_state( state )
    input()

    while not terminal(state):
        player = get_player(state)
        action = predict(state)



        print( f'PLAYER: {player} | ACTION: {action}' )
        state = apply_action( state, action )
        print( get_score(state) )
        print_state(state)

        input()
        



