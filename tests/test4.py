import unittest
import os
from glob import glob
from retriever import JsonRetriever
from tokenizer import Tokenizer
from indexer import Indexer
from encoder import GammaEncodedIndex

class TestGammaIndexer(unittest.TestCase):
    '''
        Test Gamma encoder and Gamma Indexer
    '''

    def setUp(self):
        # creating an instance of the tested class
        self.t = Tokenizer()
        self.i = Indexer(self.t)
        files = files = glob(os.path.join('samples', 'test4', '*.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        self.ig = GammaEncodedIndex(self.i)

    def test_compressor(self):
        ig = GammaEncodedIndex(self.i)
        dictionary = {
            "слово": [1,2,3,4],
            "рука": [1,1,1,1]
        }
        result = {
            "слово": "0b101001100100",
            "рука": "0b1111"
        } #values from table in https://en.wikipedia.org/wiki/Elias_gamma_coding
        self.assertEqual(ig.compress(dictionary), result, "right encoder")

    def test_same_reaults(self):
        self.assertEqual(self.i.index['морожен'], self.ig.decode(self.ig.index['морожен']), "right decoder")

    def test_search(self):
        self.assertEqual(self.ig.find('мороженое'), {2: 1, 4: 1}, "right ig searcher")
        self.assertEqual(self.i.find('мороженое'), {2: 1, 4: 1}, "right i searcher")

    def test_unexisted_word(self):
        with self.assertRaises(KeyError):
            self.ig.find("сибирь")

    def test_input_diff_symbols(self):
        self.assertEqual(self.ig.find("!ОвОщИ!!!9827346___"), {3: 1}, "handling a bad request")

    def test_two_words_in_query(self):
        self.assertEqual(self.ig.find("люблю овощи"), {2: 1, 3: 1}, "existed words but not together")
