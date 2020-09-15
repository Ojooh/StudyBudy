from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words




class Summarizey:

    def __init__(self):
        self.LANGUAGE = "english"
        self.SENTENCES_COUNT = 10

    def concatenate_list(self, clean_list):
        my_lst_str = '. '.join([x for x in clean_list])
        print(my_lst_str)

        return my_lst_str



    def generate_summary(self, text, top_n):
        # url = "https://en.wikipedia.org/wiki/Automatic_summarization"
        # parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        # or for plain text files
        # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
        self.SENTENCES_COUNT        = top_n
        parser                      = PlaintextParser.from_string(text, Tokenizer(self.LANGUAGE))
        stemmer                     = Stemmer(self.LANGUAGE)
        summarizer                  = Summarizer(stemmer)
        summarizer.stop_words       = get_stop_words(self.LANGUAGE)
        summarize_text              = []

        for sentence in summarizer(parser.document, self.SENTENCES_COUNT):
            summarize_text.append(str(sentence))

        return self.concatenate_list(summarize_text)


   

    