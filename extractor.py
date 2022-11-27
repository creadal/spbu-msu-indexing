from bs4 import BeautifulSoup
import re

class Parser():
    def _process_text(self, text):
        text = re.sub(r"(?<=\s)\s| +$|^ +", "", text)
        text = re.sub(r"(?<=^)\n", "", text)
        return text

    def extract_from_html(self, input):
        soup = BeautifulSoup(input, "html.parser")
        blacklist = [
        "head",
        "header",
        "footer",
        "form",
        "textarea",
        "dialog",
        "select",
        "label",
        "button",
        "script",
        "table",
        "code",
        ]
        for tag in soup.find_all(blacklist):
            tag.decompose()
        for br in soup.find_all("br"):
            br.replace_with("\n")
        text = soup.get_text()
        text = self._process_text(text)
        return text

