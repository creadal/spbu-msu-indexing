import os
from glob import glob
from retriever import JsonRetriever
from tokenizer import Tokenizer
from indexer import Indexer
from encoder import GammaEncodedIndex, DeltaEncodedIndex

from time import time


def measure_index_size(index: dict, bin: bool):
    size = 0
    for word in index.keys():
        if bin:
            size += len(index[word]) - 2
        else:
            size += len(index[word]) * 32

    return size


if __name__ == '__main__':
    spbu_files = glob(os.path.join('data', 'data-spbu', '*.json'))
    spbu_files.remove(os.path.join('data', 'data-spbu', 'stats.json'))

    msu_files = glob(os.path.join('data', 'data-msu', '*.json'))
    msu_files.remove(os.path.join('data', 'data-msu', 'stats.json'))

    r1 = JsonRetriever(spbu_files)

    print("== SPBU ==\n")

    t = Tokenizer()
    i1 = Indexer(t).create_index(r1)
    ig1 = GammaEncodedIndex(i1)
    id1 = DeltaEncodedIndex(i1)

    begin = time()
    for i in range(1000):
        ig1.find('ректор спбгу')
    end = time() - begin
    print(f"average time per search: {end / 1e6} ms")

    print(f"index size: %.2f kb" % (measure_index_size(i1.index, bin=False) / 8 / 1000))
    print(f"gamma encoded index size: %.2f kb" % (measure_index_size(ig1.index, bin=True) / 8 / 1000))
    print(f"delta encoded index size: %.2f kb" % (measure_index_size(id1.index, bin=True) / 8 / 1000))

    r1 = JsonRetriever(spbu_files)

    print("== SPBU ==\n")

    t = Tokenizer()
    i1 = Indexer(t).create_index(r1)
    ig1 = GammaEncodedIndex(i1)
    id1 = DeltaEncodedIndex(i1)

    begin = time()
    for i in range(1000):
        ig1.find('ректор спбгу')
    end = time() - begin
    print(f"average time per search: {end / 1e6} ms")

    print(f"index size: %.2f kb" % (measure_index_size(i1.index, bin=False) / 8 / 1000))
    print(f"gamma encoded index size: %.2f kb" % (measure_index_size(ig1.index, bin=True) / 8 / 1000))
    print(f"delta encoded index size: %.2f kb" % (measure_index_size(id1.index, bin=True) / 8 / 1000))