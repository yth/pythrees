# Specifications of Threes History

"""
Structure: 
        
        history = [move, board, deck, bonus_deck/None]

Logic: 
        [previous history]
        [from above, applying MOVE, 
                    results in BOARD, DECK, BONUS_DECK CREATION or None)]
       
        Special moves: 'start', 'end'
       
            'start' = initialize game
            'end' = game over
        
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

# All Possible values for history in a game of Threes

"""

history = [

    move: ['start', 'left', 'right', 'up', 'down', 'end']
    
    board: [
    
            [  0,    0,    1,    2],
            [  3,    6,   12,   24],
            [ 48,   96,  192,  384],
            [768, 1536, 3072, 6144]
    ]
    
    deck: [1, 2, 3]
    bonus: [6, 12, 24, 48, 96, 192, 384, 768] or None

]

"""

if __name__ == "__main__":

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
        None,
        [6], 
        [6, 12]
        [6, 12, 24],
        [12, 24, 48],
        [24, 48, 96],
        [48, 96, 192], 
        [96, 192, 384],
        [192, 384, 768]
    ])
    
    ##############
    # Test Cases #
    ##############
        
    class ThreesHistoryTest(unittest.TestCase):
    
        def setUp(self):
            self.history = History()
        
        def test_valid_moves(self):
            for turn in self.history:
                assertIn(turn[0], ALL_MOVE_VALUES)
        
        '''
        More test to follow
        '''
    
    #############
    # Test Main #
    #############
        
    unittest.main()