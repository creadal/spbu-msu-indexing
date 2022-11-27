import os
from glob import glob
from retriever import JsonRetriever
from tokenizer import Tokenizer


if __name__ == '__main__':
    files = glob(os.path.join('data', 'data-spbu', '*.json'))
    files.remove(os.path.join('data', 'data-spbu', 'stats.json'))

    r = JsonRetriever(files)
    tokenizer = Tokenizer().create_dict(r)
    tokenizer.save_dict('dict.json')