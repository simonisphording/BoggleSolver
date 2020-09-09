import numpy as np
from random import shuffle, randint
import pickle as pkl

found_words = set()

filename = "trie.pkl"
infile = open(filename, 'rb')
trie = pkl.load(infile)
infile.close()


class GameField:

    def __init__(self, d):
        self.board = np.array([["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]])
        self.dice = np.array(d)
        shuffle(self.dice)
        i = 0
        for x in range(4):
            for y in range(4):
                self.board[x, y] = self.dice[i][randint(0, 5)]
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
            dice.append(line)
    return dice


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


def search_from_dice(board, s, x, y, visited_coords):
    visited_coords.append([x, y])
    if is_word(s):
        found_words.add(s)

    for coord in adjacent_coords(x, y):
        if coord not in visited_coords:
            x2, y2 = coord
            a = board[x2, y2]
            if is_prefix(s + a):
                search_from_dice(board, s + a, x2, y2, visited_coords)


d = read_dice_file(r"C:\Users\ispho001\PycharmProjects\BoggleSolver\english_dice.txt")
g = GameField(d)
g.show_board()

for x in range(4):
    for y in range(4):
        search_from_dice(g.board, g.board[x, y], x, y, [])

found_words = list(found_words)

print(g.show_board())
for word in sorted(found_words):
    print(word)

#filename = "resultaat.txt"
#f = open(filename, 'wb')
#f.write(g.show_board())
#f.write("Gevonden woorden:")
#for word in sorted(found_words):
#    f.write(word)
