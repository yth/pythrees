#!/usr/bin/env python

########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################



""" Threes! on the command line

Graphically see how Threes! work through curses on the command line.

This is implemented as a functional test for ThreesBoard. It can also be
used to see how an AI player is playing Threes!
"""


###########
# Imports #
###########


import curses
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from ThreesBoard import ThreesBoard


##############
# Exceptions #
##############


class SmallScreenError:
    pass


#######################
# Important Constants #
#######################


GOAL = 6144  # Expected highest possible score in Threes
PADDING = 1


####################
# Important Values #
####################


""" How a cell should appear on the game board
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


####################
# Helper Functions #
####################


def _wipe_text(screen):

    screen.addstr(2, 1, "|                           |")
    screen.addstr(3, 1, "|                           |")
    screen.addstr(4, 1, "|                           |")


def _tell_user(screen, s, color_pair=0):

    _wipe_text(screen)
    screen.addstr(3, 2, '{:^27s}'.format(str(s)), curses.color_pair(color_pair))


def _draw_board(screen, board):
	# Consider define color pairings elsewhere

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

    # Consider capture draw cell in a function during refactoring
    for row in board:
        for cell in row:

            if cell == 0:
                cell = ' '

                screen.addstr(first_y + offset_y - 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(0))


                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              '{:^6s}'.format(str(cell)),
                              curses.color_pair(0))

                screen.addstr(first_y + offset_y + 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(0))


            elif cell == 1:

                screen.addstr(first_y + offset_y - 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(1))

                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              '{:^6s}'.format(str(cell)),
                              curses.color_pair(1))

                screen.addstr(first_y + offset_y + 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(1))

            elif cell == 2:

                screen.addstr(first_y + offset_y - 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(2))

                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              '{:^6s}'.format(str(cell)),
                              curses.color_pair(2))

                screen.addstr(first_y + offset_y + 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(2))

            else:

                screen.addstr(first_y + offset_y - 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(3))

                screen.addstr(first_y + offset_y,
                              first_x + offset_x,
                              '{:^6s}'.format(str(cell)),
                              curses.color_pair(3))

                screen.addstr(first_y + offset_y + 1,
                              first_x + offset_x,
                              '{:^6s}'.format(str('')),
                              curses.color_pair(3))

            offset_x += 7

        offset_x = 0
        offset_y += 4


#################
# Main Function #
#################


def main(screen):

# I could have organized this function so much better
# I could also have structured my code so much better

    # Set up environment:

    curses.curs_set(0)  # Hide Cursor, not needed in this game

    # Find out more about environment
    y, x = screen.getmaxyx()

    if y < GAME_HEIGHT or x < GAME_WIDTH:
        raise SmallScreenError

    # Calculate information for creating the new game window
    center = (y // 2, x // 2)
    start_y = center[0] - GAME_HEIGHT // 2
    start_x = center[1] - GAME_WIDTH // 2

    # Creating game
    screen = curses.newwin(GAME_HEIGHT, GAME_WIDTH, start_y, start_x)
    screen.border()

    # Static Game Board
    # This screen can also be used for debugging purposes
    # All the numbers will be covered over by game information
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
    good_keys = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN] # Only get these
    q_keys = [ord('q'), ord('Q')] # quit using 'q' or 'Q'
    game = ThreesBoard()  # Make a new board

    # Game Loop
    while not game.gameOver():

        _draw_board(screen, game.board)  # Draw the board
        next_tile = game.nextTile

        if next_tile == 1:
            color_pair = 1
        elif next_tile == 2:
            color_pair = 2
        else:
            color_pair = 3

        if next_tile >= 6:
            bonuses = []
            high = game.highestTile
            while high >= 48 and len(bonuses) < 4:
                bonuses.append(high/8)
                high /= 2
            s = str(bonuses[0])
            for tile in bonuses[1:]:
                s+= "  "
                s+= str(tile)
            _tell_user(screen, s, color_pair)

        else:
            _tell_user(screen, str(next_tile), color_pair)

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

            # Quit
            elif key in q_keys:
                break

        # Break out of the game loop
        if key in q_keys:
            break

    else:

        # Game Over
        _tell_user(screen, "Game Over!")
        _draw_board(screen, game.board)
        wait = screen.getch()

    _tell_user(screen, "Your highest tile was: " + str(game.highestTile))
    wait = screen.getch()
    # Consider adding an option to restart the game here


if __name__ == '__main__':

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
