"""
Code illustration: 4.07

NO CHANGES FROM PREVIOUS ITERATION

Tkinter GUI Application Development Hotshot
"""

import sys

SHORT_NAME = {
    'Q': 'Queen',
}


def create_piece(piece, color='white'):
    ''' Takes a piece name or shortname and returns the corresponding piece instance '''
    if piece in (None, ' '): return
    if len(piece) == 1:
        if piece.isupper():
            color = 'white'
        else:
            color = 'black'
        piece = SHORT_NAME[piece.upper()]
    module = sys.modules[__name__]
    return module.__dict__[piece](color)


class Piece(object):
    def __init__(self, color):
        if color == 'black':
            self.shortname = self.shortname.lower()
        elif color == 'white':
            self.shortname = self.shortname.upper()
        self.color = color

    def place(self, board):
        ''' Keep a reference to the board '''
        self.board = board


class Queen(Piece):
    shortname = 'q'
