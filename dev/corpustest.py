from conllu import parse
from io import open
from conllu import parse_incr, parse_tree_incr

data_file = open("dniev_09.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    print(tokenlist)
