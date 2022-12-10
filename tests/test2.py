import unittest
from tokenizer import Tokenizer
from extractor import Parser

class TestTokenizerAndParser(unittest.TestCase):
    '''
        Tokenizer tests and parser simple test (the parser was tested in module 1)
    '''

    def setUp(self):
        # creating an instance of the tested class
        self.t = Tokenizer()
        self.p = Parser()

    def test_tokenizers_work(self):
        word = "ЛАБорАтОрия,"
        self.assertEqual("лаборатор", self.t.tokenize(word, add_to_dict=True), "stemming, remove punctuation, lower case")

    def test_empty_string(self):
        self.assertEqual(self.t.tokenize("", add_to_dict=True), "", "empty string is empty string")

    def test_not_space_separation(self):
        self.assertEqual(self.t.tokenize("СПБГУ/МГУ", add_to_dict=True), "спбгу мгу", "slash separation")

    def test_eng_big_word(self):
        self.assertEqual(self.t.tokenize("WORD", add_to_dict=True), "word", "to lower case")

    def test_parsers_work(self):
        file = open("samples/example.html", "r")
        self.assertEqual(self.p.extract_from_html(file), "Guest page\nHello, dear guest!\n")
