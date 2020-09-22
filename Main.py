import numpy as np
from random import shuffle, randint
from os import path
import pickle as pkl
import argparse
import Generate_Trie
from time import time, sleep

parser = argparse.ArgumentParser(description='Generate a Boggle boardstate and find all words present based on the ' +
                                 'provided dictionary')
parser.add_argument('-b', '--board', type=str, metavar='\b',
                    help='a boardstate file containing the boardstate to be used. If provided, the dice file is ignored'
                    , default=None, required=False)
parser.add_argument('-d', '--dice', type=str, metavar='\b',
                    help='a txt file containing the dice to be used',
                    default='english_dice.txt', required=False)
parser.add_argument('-o', '--output', type=str, metavar='\b',
                    help='the name of the file in which the result is printed.\
                     If left blank, the result will not be saved,',
                    default=None, required=False)
parser.add_argument('-w', '--words', type=str, metavar='\b',
                    help='a list of words to replace the default wordlist.txt. A trie will be generated',
                    default='wordlist.txt', required=False)
parser.add_argument('-t', '--time', type=int, metavar='\b',
                    help='the amount of time you get to fill in words',
                    default=120, required=False)


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
        all_words.add(s)

    for coord in adjacent_coords(x, y):
        if coord not in temp:
            x2, y2 = coord
            a = board[x2, y2]
            if is_prefix(s + a):
                search_from_dice(board, s + a, x2, y2, temp)


def points_for_word(word):
    if len(word) <= 4:
        return 1
    elif len(word) == 5:
        return 2
    elif len(word) == 6:
        return 3
    elif len(word) == 7:
        return 5
    else:
        return 7


if __name__ == '__main__':

    args = parser.parse_args()

    all_words = set()

    filename = path.splitext(args.words)[0] + "_trie.pkl"
    if not path.exists(filename):
        Generate_Trie.trie_from_word_list(args.words)

    infile = open(filename, 'rb')
    trie = pkl.load(infile)
    infile.close()

    d = read_dice_file(args.dice)
    if args.board:
        b = read_board_file(args.board)
        g = GameField(d, b)
    else:
        g = GameField(d)

    for x in range(4):
        for y in range(4):
            search_from_dice(g.board, g.board[x, y], x, y, [])

    all_words = list(all_words)

    timeout = args.time
    found_words = []

    print(g.show_board())

    start = time()

    while(time() < start + timeout):
        s = input("Type your words here, you have %f seconds!\n" % (start + timeout - time()))
        s = s.upper()
        if s in all_words:
            if s not in found_words:
                print("correct!")
                found_words.append(s)
            else:
                print('you found this word already!')
        else:
            print("This isn't a word")
        sleep(1)
        print(g.show_board())

    score = 0
    for word in found_words:
        score += points_for_word(word)

    total_score = 0
    for word in all_words:
        total_score += points_for_word(word)

    print("congratulations, you got %s out of %s possible points" % (score, total_score))

    print("you found the following words:")
    for word in sorted(found_words):
        print(word)

    print("These are the words you missed:")
    for word in sorted(all_words):
        if word not in found_words:
            print(word)

    if args.output:
        filename = args.output
        f = open(filename, 'w')
        f.write(g.show_board() + "\n")
        f.write("You got %s out of %s possible points in %s seconds\n\n" % (score, total_score, timeout))
        f.write("Found words:\n\n")
        for word in sorted(found_words):
            f.write(word + "\n")
        f.write("\nWords not found:\n\n")
        for word in sorted(all_words):
            if word not in found_words:
                f.write(word + "\n")
