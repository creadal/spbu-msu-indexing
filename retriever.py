from extractor import Parser
import json
import string


class Retriever:
    """Absctract class for retriever iterators"""

class JsonRetriever(Retriever):
    def __init__(self, files):
        self.files = files
        self.i = 0
        self.files_list = files

        self.parser = Parser()
        self.get_next_text()



    def __iter__(self):
        return self


    def get_next_text(self):
        try:
            self.current_filename = self.files[self.i]
            self.i += 1
            # print(self.i)
        except IndexError:
            return False

        with open(self.current_filename, encoding='utf-8') as f:
            json_file = json.load(f)
            text = json_file['content']

            self.current_text = iter(self.parser.extract_from_html(text).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).split())

        return True


    def __next__(self):
        while True:
            try:
                return next(self.current_text), self.current_filename
            except StopIteration:
                status = self.get_next_text()
                if not status:
                    raise StopIteration
                    