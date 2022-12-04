import os
from glob import glob
from retriever import JsonRetriever
from tokenizer import Tokenizer
from indexer import Indexer
from encoder import GammaEncodedIndex


if __name__ == '__main__':
    files = glob(os.path.join('data', 'data-spbu', '*.json'))
    files.remove(os.path.join('data', 'data-spbu', 'stats.json'))

    r = JsonRetriever(files[:100])

    t = Tokenizer()
    i = Indexer(t).create_index(r)
    ig = GammaEncodedIndex(i)

    print(i.find('ректор спбгу'))
    print(ig.find('ректор спбгу'))