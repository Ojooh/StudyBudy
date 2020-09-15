import nltk
import string
import sys
import time
import spacy
from .restart_line import restart_line
# from spacy.tokens import Token


nlp = spacy.load("en_coref_sm")
#nlp = spacy.load('en')
# neuralcoref.add_to_pipe(nlp)
# Token.set_extension('context', default=False, force=True)



class SentenceProcessing:
    def __init__(self):
        self.cleaned_sentences  =  []
        

    def clean_sentences(self, text):
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sentence_detector.tokenize(text[0].strip())
        punc = set(string.punctuation)
        punc.remove('.')
        punc.remove('?')
        punc.remove(',')
        special_char = ['*', '#', '@', '$', '%', '^', '&', "(", ")", "-", "+"]
        alphab = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  '0', ' ',]
        new_sentence = ""

        for sentence in sentences:
            for x in sentence:
                x = x.lower()
                if x in alphab and x not in punc and x not in special_char:
                    new_sentence += x
            self.cleaned_sentences.append(new_sentence)
            new_sentence = ""

        cleaned = self.concatenate_list(self.cleaned_sentences)
        return cleaned


    def concatenate_list(self, clean_list):
        my_lst_str = '. '.join([x for x in clean_list])

        return my_lst_str


    def pronoun_transformation(self, clean_text):
        clean_text.encode('utf-8')
        doc = nlp(clean_text)
        trey = doc._.coref_clusters
        resolved = doc._.coref_resolved
        
        if resolved == "":
            return clean_text
        else:
            return resolved


    def get_sentences(self, trans_text):
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        text = trans_text
        sentences = sentence_detector.tokenize(text.strip())
        print(sentences)

        return sentences


    def prepare_sentences(self, Arrrawtext):

        clean_text = self.clean_sentences(Arrrawtext)

        transformed_text = self.pronoun_transformation(clean_text)
        
        sanitized_sentences = self.get_sentences(transformed_text)

        return sanitized_sentences