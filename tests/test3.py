import unittest
import os
from glob import glob
from retriever import JsonRetriever
from tokenizer import Tokenizer
from indexer import Indexer

class TestIndexer(unittest.TestCase):
    def setUp(self):
        # creating an instance of the tested class
        self.t = Tokenizer()
        self.i = Indexer(self.t)

    def test_empty_collection(self):
        files = glob(os.path.join('samples', 'test3', 'two.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        dictionary = self.i.index
        self.assertEqual(dictionary, {}, "empty collection creates an empty dictionary")
        self.assertEqual(self.i.find(""), {})

    def test_not_space_separation(self):
        files = glob(os.path.join('samples', 'test3', 'one.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        try:
            self.assertEqual(self.i.find("ui"), {1: 1}, "not space separation")
        except:
            self.assertEqual(1,0, "error: word not found")

    def test_mispells(self):
        files = glob(os.path.join('samples', 'test3', 'three.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        try:
            self.i.find("телефон")
            self.assertEqual(1,0, "mispell excepted")
        except:
            self.assertEqual(1,1, "word not found")

    def test_numbers(self):
        files = glob(os.path.join('samples', 'test3', 'three.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        try:
            self.i.index['8']
            self.assertEqual(1,0, "error: a number became the key")
        except:
            self.assertEqual(1,1, "there is no such key")
        with self.assertRaises(KeyError):
            self.i.find("8")

    def test_search_non_existed_word(self):
        files = glob(os.path.join('samples', 'test3', 'three.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        with self.assertRaises(KeyError):
            self.i.find("коготь")

    def test_with_correct_word(self):
        files = glob(os.path.join('samples', 'test3', 'three.json'))
        r = JsonRetriever(files)
        self.i.create_index(r)
        self.assertEqual(self.i.find("номер"), {1: 1}, "existed word")        
