import re
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._inside_script = False
        self._inside_style = False
        self._inside_head = False
        self._inside_title = True
        self._words = []
        self._word_regex = re.compile('\w+')

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self._inside_script = True
        elif tag == 'style':
            self._inside_style = True
        elif tag == 'head':
            self._inside_head = True
        elif tag == 'title':
            self._inside_title = True

    def handle_endtag(self, tag):
        self._inside_script = False
        self._inside_style = False

    def handle_data(self, data):
        if self._inside_script or self._inside_style:
            return
        words = self._word_regex.findall(data)
        if 0 < len(words) <= 2:
            self._words.append(' '.join(words))
        else:
            for word in words:
                self._words.append(word)

    @staticmethod
    def get_all_words(text: str) -> list:
        extractor = TextExtractor()
        extractor.feed(text)
        return extractor._words
