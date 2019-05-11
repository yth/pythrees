## Planning Stage

## State Representation

"""
What's visible to the human player is the board with tiles on them, and
the information of what's the next tile that will be added to the board.
To have a presentation at this level, I just need to flatten the board
information into a list and then add another element to the list to
represent the next tile.

However, this is not all the information available to a really clever
and dedicated human player. That player might track which tiles are has
already been seen. They could work out the frequencies of the tiles, and
reconstruct the TileDeck structure and play ahead even more.

To mirror this player, I would need to flatten the board, add a next
tile, a list to present all the tiles that are yet to be drawn from the
current deck, and a counter to warn again bonus decks.
"""

## NN Representation

"""
Assuming that I have M features in my state representation, a NN would
then have M nodes in the first layer. There are only four decisions to
make in the game: swipe left, right, up and down. The last layer need to
have 4 nodes. There could be any number of in between layers.
"""

## Marking Success

"""
The NN_AI player would need to know how to make valid moves. Through the
operations of the NN, it will only make valid moves.

The NN_AI player will also ideally be a good player of Threes! It will
need to make moves that make the game last as long as possible.
"""

## Implementation

"""
I think I should use numpy to implement my NN and training algorithms.

It feels unprofitable at this point to implement my own matrix library.
"""