from pytrie import StringTrie
import pickle as pkl

dictionary = []

trie = StringTrie()

f = open(r"C:\Users\ispho001\PycharmProjects\BoggleSolver\wordlist.txt", "r")
for line in f:
    if " " not in line.rstrip():
        key = line.rstrip().upper()
        trie[key] = key

filename = "trie.pkl"
outfile = open(filename, 'wb')
pkl.dump(trie, outfile)
outfile.close()
