from extractor import Parser
import json


class Retriever:
    """Absctract class for retriever iterators"""

class JsonRetriever(Retriever):
    def __init__(self, files):
        self.files = iter(files)

        self.parser = Parser()
        self.get_next_text()


    def __iter__(self):
        return self


    def get_next_text(self):
        try:
            self.current_filename = next(self.files)
        except StopIteration:
            return False

        with open(self.current_filename, encoding='utf-8') as f:
            json_file = json.load(f)
            text = json_file['content']

            self.current_text = iter(self.parser.extract_from_html(text).split())

        return True


    def __next__(self):
        try:
            return next(self.current_text)
        except StopIteration:
            status = self.get_next_text()
            if not status:
                raise StopIteration
            else:
                return next(self.current_text)