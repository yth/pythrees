# Specifications of Threes History

"""
Structure: 
        
        history = [move, board, deck, bonus_deck/None]

Logic: 
        [previous history]
        [from above, applying MOVE, 
                    results in BOARD, DECK, BONUS_DECK CREATION or None)]
        
        Special Notes:
            
            If there is a bonus deck, the next tile is draw from the
            bonus deck instead. The bonus deck is reset to none after
            each draw.
            
            A bonus deck is created every 24 moves.
        
Sample Game History:

0   ['start', [[...][...][...][...]], [...], None]
1   ['left', [[...][...][...][...]]', [...]', None]
    ...
    # Cause bonus deck creation
23  ['up', [[...][...][...][...]]'', [...]'', BONUS_DECK] 
    # Uses bonus deck instead of normal deck
24  ['right', [[...][...][...][...]]''', [...]'', None] 
    ...
    #No possible moves from this position
n-1 ['down', [[...],[...],[...],[...]]''', [...]''', BONUS_Deck/None'''] 
n   ['end',  [[...],[...],[...],[...]]''', [...]''', BONUS_Deck/None''']

or

n   ['end']
"""

###########
# Imports #
###########

import unittest

#######################
# Important Constants #
#######################

ALL_MOVE_VALUES = set([
    'start', 'left', 'right', 'up', 'down', 'end'
])

ALL_BOARD_CELL_VALUES = set([
    0, 1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144
])

ALL_DECK_TILE_VALUES = set([1, 2, 3])

ALL_BONUS_DECK_VALUES = set([
    (0),
    (6),
    (6, 12),
    (6, 12, 24),
    (12, 24, 48),
    (24, 48, 96),
    (48, 96, 192),
    (96, 192, 384),
    (192, 384, 768)
])

##############
# Test Cases #
##############
    
class ThreesHistoryTest(unittest.TestCase):

    def setUp(self, history):
        self.history = history
        self.moves = []
        self.board_positions = []
        self.deck_states = []
        self.bonus_deck_states = []
        for turn in history:
            move, board, deck, bonus_deck = turn
            moves.append(move)
            board_positions.append(board)
            deck_states.append(deck)
            bonus_deck_states.append(bonus_deck)
    
    def test_valid_moves(self):
        moves = set(self.moves)
        for move in moves:
            assertIn(move, ALL_MOVE_VALUES)
    
    def test_valid_board_values(self):
        tiles = []
        for board in self.board_positions:
            tiles += [tile for sublist in board for tile in sublist]
        tiles = set(tiles)
        for tile in tiles:
            assertIn(tile, ALL_BOARD_CELL_VALUES)
            
    def test_valid_deck(self):
        tiles = [tile for sublst in self.deck_states for tile in sublst]
        for tile in tiles:
            assertIn(tile, ALL_DECK_TILE_VALUES)
            
    def test_valid_bonus_deck(self):
        for bonus_deck in self.bonus_deck_states:
            assertIn(bonus_deck, ALL_BONUS_DECK_VALUES)

if __name__ == "__main__":
        
    unittest.main()
