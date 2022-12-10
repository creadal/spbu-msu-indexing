from tokenizer import Tokenizer
from retriever import JsonRetriever, Retriever
from tqdm import tqdm
from glob import glob
import os
from itertools import tee


class Indexer:
    def __init__(self, t: Tokenizer):
        self.t = t
        self.index = {key: [] for key in t.dictionary}


    def add_to_index(self, word: str, source: str):
        if word not in self.index.keys():
            self.index[word] = [source]
        else:
            if source not in self.index[word]:
                self.index[word].append(source)


    def create_index(self, r: Retriever):
        self.sources = [None] + sorted(r.files_list)
        
        print('started indexing')
        for word, file in tqdm(r):
        # for word, file in r:
            token = self.t.tokenize(word, add_to_dict=True)
            self.add_to_index(token, file)

        print('index created')

        if None in self.index.keys():
            del self.index[None]
        self.indexize()

        return self

    def indexize(self):
        for word in tqdm(self.index.keys()):
            self.index[word] = sorted(self.index[word])

            new_values = [self.sources.index(self.index[word][i]) \
                          for i in range(len(self.index[word]))]

            for i in range(len(new_values) - 1, 0, -1):
                new_values[i] = new_values[i] - new_values[i-1]

            self.index[word] = new_values

    def find(self, query):
        words = [self.t.tokenize(word, add_to_dict=False) for word in query.split()]
        results = {}

        for word in words:
            position = 0
            try:
                for result in self.index[word]:
                    position += result
                    if position not in results:
                        results[position] = 1
                    else:
                        results[position] += 1
            except KeyError:
                pass

        return results


if __name__ == '__main__':
    files = glob(os.path.join('data', 'data-spbu', '*.json'))
    files.remove(os.path.join('data', 'data-spbu', 'stats.json'))

    r = JsonRetriever(files[:100])

    t = Tokenizer()
    i = Indexer(t).create_index(r)

    print(i.index)