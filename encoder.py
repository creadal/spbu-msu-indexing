from indexer import Indexer
import numpy as np
from tokenizer import Tokenizer
from glob import glob
import os
from retriever import JsonRetriever
from tqdm import tqdm


class GammaEncodedIndex(Indexer):
    def __init__(self, i: Indexer):
        self.t = i.t
        self.sources = i.sources
        self.index = self.compress(i.index)

    def compress(self, index: dict):
        new_index = {}
        for word in tqdm(index):
            new_value = '0b'
            for pos in index[word]:
                if pos == 1:
                    new_value += '1'
                else:
                    N = int(np.log2(pos))
                    new_value += '0' * N
                    new_value += '1'
                    leftover = bin(pos - np.power(2, N))[2:]
                    new_value += (N - len(leftover)) * '0'
                    new_value += leftover

            new_index[word] = new_value
        return new_index


    def decode(self, s: str):
        pos_list = []
        ended = False
        i = 2
        while True:
            if ended:
                break
            N = 0
            while True:
                try:
                    c = s[i]
                except IndexError:
                    ended = True
                    break

                if c == '0':
                    N += 1
                else:
                    leftover = '0b' + s[i+1:i+N+1]
                    base = np.power(2, N) if leftover != '0b' else 0
                    leftover = int(leftover, base=2) if leftover != '0b' else 1
                    pos_list.append(base + leftover)
                    i += N + 1
                    break
                
                i += 1
        return pos_list

    def find(self, query):
        words = [self.t.tokenize(word, add_to_dict=False) for word in query.split()]
        results = {}

        for word in words:
            position = 0
            for result in self.decode(self.index[word]):
                position += result
                if position not in results:
                    results[position] = 1
                else:
                    results[position] += 1

        return results

if __name__ == '__main__':
    files = glob(os.path.join('data', 'data-spbu', '*.json'))
    files.remove(os.path.join('data', 'data-spbu', 'stats.json'))

    r = JsonRetriever(files[:100])

    t = Tokenizer()
    i = Indexer(t).create_index(r)
    ig = GammaEncodedIndex(i)

    print(i.index['д'])
    print(ig.decode(ig.index['д']))