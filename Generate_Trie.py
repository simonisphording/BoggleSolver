from pytrie import StringTrie
from os.path import splitext
import pickle as pkl


def trie_from_word_list(filename):

    trie = StringTrie()

    f = open(filename, "r")
    for line in f:
        if " " not in line.rstrip():
            key = line.rstrip().upper()
            trie[key] = key
    filename2 = splitext(filename)[0] + "_trie.pkl"
    outfile = open(filename2, 'wb')
    pkl.dump(trie, outfile)
    outfile.close()


if __name__ == '__main__':
    trie_from_word_list(r"C:\Users\ispho001\PycharmProjects\BoggleSolver\wordlist.txt")
    print("trie generated")