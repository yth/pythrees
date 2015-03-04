########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################


"""
Visualize the game of Threes in the command line with curses
"""


###########
# Imports #
###########

import curses
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
import string
from ThreesBoard import ThreesBoard

#######################
# Important Constants #
#######################

GOAL = 6144  # Expected highest possible score in Threes
PADDING = 1

####################
# Important Values #
####################

"""
--------
|      |
| 6144 |
|      |
--------
"""

CELL_WIDTH = len(str(GOAL)) + 2 * PADDING + 2
CELL_HEIGHT = 1 + 2 * PADDING + 2

BOARD_HEIGHT = CELL_HEIGHT * 4 - 3
BOARD_WIDTH = CELL_WIDTH * 4 - 3

TEXT_BOX_HEIGHT = 1 + 2 * PADDING + 2

GAME_HEIGHT = BOARD_HEIGHT + 2 + TEXT_BOX_HEIGHT - 1
GAME_WIDTH = BOARD_WIDTH + 2

##############
# Exceptions #
##############


class SmallScreenError:
    pass


####################
# Helper Functions #
####################


def _wipe_text(screen):

    screen.addstr(2, 1, "|                           |")
    screen.addstr(3, 1, "|                           |")
    screen.addstr(4, 1, "|                           |")


def _tell_user(screen, s):

    _wipe_text(screen)
    screen.addstr(3, 2, string.center(str(s), 27, ' '))


def _draw_board(screen, board):

    # Color for 1 tiles
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    # Color for 2 tiles
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

    # Color for all other tiles
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    first_y = 7
    first_x = 2
    offset_y = 0
    offset_x = 0

    for row in board:
        for cell in row:

            if cell == 0:
                cell = ' '
                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              string.center(str(cell), 6, ' '),
                              curses.color_pair(0))

            elif cell == 1:

                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              string.center(str(cell), 6, ' '),
                              curses.color_pair(1))

            elif cell == 2:

                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              string.center(str(cell), 6, ' '),
                              curses.color_pair(2))

            else:

                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              string.center(str(cell), 6, ' '),
                              curses.color_pair(3))

            offset_x += 7

        offset_x = 0
        offset_y += 4


#################
# Main Function #
#################


@curses.wrapper
def main(screen):

    # Set up environment:

    curses.curs_set(0)  # Hide Cursor, not needed in this game

    # Find out more about environment
    y, x = screen.getmaxyx()

    if y + x < GAME_WIDTH + GAME_HEIGHT:
        raise SmallScreenError

    center = (y / 2, x / 2)

    # Calculate information for creating the new game window
    start_y = center[0] - GAME_HEIGHT / 2
    start_x = center[1] - GAME_WIDTH / 2

    # Creating game
    screen = curses.newwin(GAME_HEIGHT, GAME_WIDTH, start_y, start_x)
    screen.border()

    # Static Game Board

    screen.addstr( 1, 1, "+---------------------------+")
    screen.addstr( 2, 1, "|                           |")
    screen.addstr( 3, 1, "|        1         2        |")
    screen.addstr( 4, 1, "|234567890123456789012345678|")
    screen.addstr( 5, 1, "+---------------------------+")
    screen.addstr( 6, 1, "|      |      |      |      |")
    screen.addstr( 7, 1, "| 6144 | 6144 | 6144 | 6144 |")
    screen.addstr( 8, 1, "|      |      |      |      |")
    screen.addstr( 9, 1, "+------+------+------+------+")
    screen.addstr(10, 1, "|      |      |      |      |")
    screen.addstr(11, 1, "| 6144 | 6144 | 6144 | 6144 |")
    screen.addstr(12, 1, "|      |      |      |      |")
    screen.addstr(13, 1, "+------+------+------+------+")
    screen.addstr(14, 1, "|      |      |      |      |")
    screen.addstr(15, 1, "| 6144 | 6144 | 6144 | 6144 |")
    screen.addstr(16, 1, "|      |      |      |      |")
    screen.addstr(17, 1, "+------+------+------+------+")
    screen.addstr(18, 1, "|      |      |      |      |")
    screen.addstr(19, 1, "| 6144 | 6144 | 6144 | 6144 |")
    screen.addstr(20, 1, "|      |      |      |      |")
    screen.addstr(21, 1, "+------+------+------+------+")

    # Initialize Game
    screen.keypad(1)  # Enable special keys
    good_keys = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]  # Only get these

    game = ThreesBoard()  # Make a new board

    # Game Loop
    while not game.gameOver():

        _draw_board(screen, game.board)  # Draw the board
        _tell_user(screen, "Your next tile is: " + str(game.nextTile))

        while 1:

            key = screen.getch()

            if key in good_keys:

                if key == KEY_LEFT:
                    game.swipe("left")

                elif key == KEY_RIGHT:
                    game.swipe("right")

                elif key == KEY_UP:
                    game.swipe("up")

                elif key == KEY_DOWN:
                    game.swipe("down")

                break

    # Game Over
    _tell_user(screen, "Game Over!")
    _draw_board(screen, game.board)
    wait = screen.getch()

    _tell_user(screen, "Your highest tile was: " + str(game.highestTile))
    wait = screen.getch()
