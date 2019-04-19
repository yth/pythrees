from __future__ import print_function
from ThreesBoard import ThreesBoard
from ThreesBoard import _swipe_left, _swipe_right, _swipe_up, _swipe_down
from TileDeck import TileDeck
from random import randint, choice
from copy import copy

MOVES = {
    "left":0,
    "right":1,
    "up":2,
    "down":3,
    0:"left",
    1:"right",
    2:"up",
    3:"down"
}

a = ThreesBoard()

def draw_board(game_board):
    for row in game_board.board:
        for tile in row:
            print(str(tile).center(6), end=' ')
        print('')
    print('-'*24)



while not a.gameOver():
    next_move_scores = [0.0, 0.0, 0.0, 0.0]
    next_move_trials = [1.0, 1.0, 1.0, 1.0]
    test_move = None
    possible_moves = None
    for i in range(1000):
        b = ThreesBoard(board=a.board, deck=TileDeck(copy(a.deck.deck)), nextTile=a.nextTile, history=[])

        possible_moves = b.get_valid_moves()
        test_move = choice(possible_moves)
        b.swipe(test_move)
        while not b.gameOver():
            b.swipe(MOVES[randint(0, 3)])
        # next_move_scores[MOVES[test_move]] += sum([sum(row) for row in b.board])
        next_move_scores[MOVES[test_move]] += len(b.history) * 100
        # next_move_scores[MOVES[test_move]] += b.highestTile
        # next_move_scores[MOVES[test_move]] -= sum([1 if i == 1 or i == 2 else 0 for row in b.board for i in row]) * 100
        next_move_trials[MOVES[test_move]] += 1
        

    values = []
    for i in range(4):
        values.append(next_move_scores[i] / next_move_trials[i])

    if max(values) == 0:
        a.swipe(choice(a.get_valid_moves()))
    else:
        best = max(values)
        indexes = []
        for i in range(4):
            if values[i] == best:
                indexes.append(i)
        move = MOVES[choice(indexes)]
        print(move, best, a.nextTile)
        a.swipe(move)
 
    draw_board(a)


print(a)
print("\n  The next tile is :", a.nextTile, '\n')
for row in a.board:
    for tile in row:
        print(str(tile).center(6), end=' ')
    print('')

print("\n  This is the end board after using an expectimax strategy.")
print("\n  The highest tile obtained is " + str(a.highestTile) + \
	  ", after playing " + str(len(a.history)) + " moves.")
