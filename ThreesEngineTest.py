###########
# Imports #
###########

import unittest
from random import choice
from ThreesEngine import ThreesEngine

#######################
# Important Constants #
#######################

ALL_MOVE_VALUES = (
    'start', 'left', 'right', 'up', 'down', 'end'
)

ALL_BOARD_CELL_VALUES = (
    0, 1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144
)

ALL_DECK_TILE_VALUES = (1, 2, 3)

ALL_BONUS_DECK_VALUES = (
    [],
    [6],
    [6, 12],
    [6, 12, 24],
    [12, 24, 48],
    [24, 48, 96],
    [48, 96, 192],
    [96, 192, 384],
    [192, 384, 768]
)

ALL_NEXT_TILE_VALUES = (ALL_DECK_TILE_VALUES, ALL_BONUS_DECK_VALUES)

#############
# Test Case #
#############

class ThreesEngineTest(unittest.TestCase):

    def setUp(self):
        all_moves = ('left', 'right', 'up', 'down')
        test_game = ThreesEngine()

        while True:

            while not test_game.game_over():
                test_game.swipe(choice(all_moves))

            if test_game.highest_tile == 96:
                break

            else:
                test_game = ThreesEngine()

        self.history = test_game.history
        self.board = self.history[-1][1]
        self.deck = self.history[-1][2]
        self.next_tile = self.history[-1][3]

    def test_start_game(self):
        assert self.history[0][0] == 'start'

    def test_end_game(self):
        assert self.history[-1][0] == 'end'

    def test_board_valid_size(self):
        size = len(self.board)
        for row in self.board:
            assertEqual(len(row), size)

    def test_board_valid_tiles(self):
        all_tiles = [tile for sublist in self.board for tile in sublist]
        tiles = set(all_tiles)
        assert tiles.issubset(ALL_BOARD_CELL_VALUES)

    def test_deck_valid_tiles(self):
        tiles = set(self.deck)
        assert tiles.issubset(ALL_DECK_TILE_VALUES)

    def test_tiles_used(self):
        bonus_deck_used = []
        for turn in self.history:
            bonus_deck_used.append(turn[3])
        bonus_decks = set(bonus_deck_used)
        assert bonus_deck.issubset(ALL_BONUS_DECK_VALUES)

    def test_board_history():
        pass

if __name__ == "__main__":

    unittest.main()
