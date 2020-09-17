import numpy as np
from random import shuffle, randint
import pickle as pkl
import argparse

#TODO: figure out why "NADEN" isn't found
#TODO: integrate generate_trie

parser = argparse.ArgumentParser(description='Generate a Boggle boardstate and find all words present based on the ' +
                                 'provided dictionary')
parser.add_argument('-b', '--board', type=str, metavar='\b',
                    help='a boardstate file containing the boardstate to be used. If provided, the dice file is ignored'
                    , default=None, required=False)
parser.add_argument('-d', '--dice', type=str, metavar='\b',
                    help='a txt file containing the dice to be used',
                    default='english_dice.txt', required=False)
parser.add_argument('-o', '--output', type=str, metavar='\b',
                    help='the name of the file in which the result is printed',
                    default='result.txt', required=False)

args = parser.parse_args()

found_words = set()

filename = "trie.pkl"
infile = open(filename, 'rb')
trie = pkl.load(infile)
infile.close()


class GameField:

    def __init__(self, d, b=None):
        if b:
            self.board = np.array(b)
        else:
            self.board = np.array([["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]],
                                  dtype='U100')

            self.dice = np.array(d)

            self.order = [i for i in range(16)]
            shuffle(self.order)

            i = 0
            for x in range(4):
                for y in range(4):
                    letter = self.dice[self.order[i]][randint(0, 5)]
                    self.board[x, y] = letter
                    i += 1

    def show_board(self):
        result = ""
        for x in range(4):
            for y in range(4):
                result += self.board[x, y]
                result += " "
            result += "\n"
        return result


def read_dice_file(filename):
    # reads dice file and adds found dice to a list. Ignores lines starting with "#"
    dice = []
    f = open(filename, "r")
    for line in f:
        if not line[0] is "#":
            dice.append(line.split())
    return dice


def read_board_file(filename):
    board = []
    f = open(filename, "r")
    for line in f:
        if not line[0] is "#":
            board.append(line.split())
    return board


def is_word(s):
    if len(s) >= 3:
        return s in trie.values(s)
    else:
        return False


def is_prefix(s):
    if not trie.values(s):
        return False
    else:
        return True


def adjacent_coords(x, y):
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            x2 = x + dx
            y2 = y + dy
            if -1 < x2 < 4 and -1 < y2 < 4:
                if x2 != x or y2 != y:
                    result.append([x2, y2])
    return result


def search_from_dice(board, s, x, y, visited_coords, debug=False):
    temp = visited_coords.copy()
    temp.append([x, y])

    if debug:
        print(temp, s)

    if is_word(s):
        found_words.add(s)

    for coord in adjacent_coords(x, y):
        if coord not in temp:
            x2, y2 = coord
            a = board[x2, y2]
            if is_prefix(s + a):
                search_from_dice(board, s + a, x2, y2, temp)


d = read_dice_file(args.dice)
if args.board:
    b = read_board_file(args.board)
    g = GameField(d, b)
else:
    g = GameField(d)

for x in range(4):
    for y in range(4):
        search_from_dice(g.board, g.board[x, y], x, y, [])

found_words = list(found_words)

filename = args.output
f = open(filename, 'w')
f.write(g.show_board() + "\n")
f.write("Found words:\n")
for word in sorted(found_words):
    f.write(word + "\n")
