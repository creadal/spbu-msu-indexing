import unittest
import os
from glob import glob
from retriever import JsonRetriever
from tokenizer import Tokenizer
from indexer import Indexer
from encoder import GammaEncodedIndex

class TestIndexers(unittest.TestCase):
    def setUp(self):
        # creating an instance of the tested class
        files = glob(os.path.join('data', 'data-spbu', '*.json'))
        files.remove(os.path.join('data', 'data-spbu', 'stats.json'))
        self.r = JsonRetriever(files[:100])
        self.t = Tokenizer()
        self.i = Indexer(self.t).create_index(self.r)
        self.ig = GammaEncodedIndex(self.i)

    def test_length_check(self):
        i_result = self.i.find('ректор спбгу')
        ig_result = self.ig.find('ректор спбгу')
        self.assertEqual(len(i_result), len(ig_result), "Result's length should be equal")

    def test_values(self):
        i_result = self.i.find('ректор спбгу')
        ig_result = self.ig.find('ректор спбгу')
        for key in i_result:
            self.assertEqual(i_result[key], ig_result[key], "Values should be equal")
