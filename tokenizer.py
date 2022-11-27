import os
import json

from retriever import Retriever

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from tqdm import tqdm


punctuation = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»0123456789'


class Tokenizer:
    def __init__(self):
        self.dictionary = set()

        self.russian_stopwords = stopwords.words("russian")

        self.stemmer = SnowballStemmer("russian")


    def read_dict(self, json_dict: os.PathLike):
        """
        Reads dictionary from JSON file.

        returns a Tokenizer object with read dictionary

        Args:
        1. json_dict: os.PathLike - path with a dictionary to read from.
        """
        with open(json_dict) as file:
            self.dictionary = set(json.load(file))

        return self


    def create_dict(self, r: Retriever, write_immedeately=False, 
                    write_location=None):
        """Tokenize text from r, create set of tokenized words. 

        returns a Tokenizer object with created dictionary

        Args:
        1. r: Retriever - an object to retireve the text from.
        2. write_immedeately=False - if True, \
            dictionary will be written to write_location.
        3. write_location=None
        """
        file = None
        if write_immedeately:
            file = open(write_location, 'w+')
            file.write('{\n')

        for word in tqdm(r):
            token = self.tokenize(word, add_to_dict=True)

            if not token is None:
                if write_immedeately:
                    if token not in self.dictionary:
                        file.write(f'\t\'{token}\',\n')

        if write_immedeately:
            file.write('}')
            file.close()

        return self


    def save_dict(self, destination):
        """Saves dict to a file

        Args:
            destination (os.PathLike): destionation path for a file
        """
        with open(destination, 'w+', encoding='utf-8') as file:
            s = json.dumps(list(self.dictionary), ensure_ascii=False).encode('utf8')
            file.write(s.decode()) 

    
    def tokenize(self, word: str, add_to_dict=False):
        """Tokenizes a word.

            Args:
                1. word: str
                2. add_to_dict=False - if True, writes new token to dict, \
                    otherwise raise exception for new tokens
        """
        word = word.translate(str.maketrans('', '', punctuation))
        token = self.stemmer.stem(word)
        
        if token in self.russian_stopwords:
            return None
        else:
            if not token in self.dictionary:
                if add_to_dict:
                    self.dictionary.add(token)
                else:
                    raise KeyError(token)
            return token