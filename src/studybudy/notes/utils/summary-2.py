import nltk
import string
import sys
import time
import codecs
import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity 
from nltk.cluster.util import cosine_distance


class Summarizer:
    def __init__(self):
        self.cleaned_sentences  =  []
        self.GLOVE   = r"C:\Users\david\OneDrive\Documents\Projects\Django\SB\src\studybudy\notes\models\glove\glove.6B.100d"



    def concatenate_list(self, clean_list):
        my_lst_str = '. '.join([x for x in clean_list])

        return my_lst_str

    
    def rankTOP(self, sentences, scores, number, summarize_text):
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        print("Indexes of top ranked_sentence order are ", ranked_sentences)

        for i in range(number):
            sent    = ranked_sentences[i][1]
            if sent:
                summarize_text.append(" ".join(ranked_sentences[i][1]))
        
        print("Summarize Text: \n", ". ".join(summarize_text))


        return summarize_text


    def pageTextRank(self, sim_mat):
        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank_numpy(nx_graph, alpha=0.9)

        return scores

    
    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []
    
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
 
        all_words = list(set(sent1 + sent2))
    
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
 
        # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1
 
        # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1
    
        return 1 - cosine_distance(vector1, vector2)


    def build_similarity_matrix(self, sentences, stop_words):
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue 
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix


    def clean_sentences(self, sentences):
        punc = set(string.punctuation)
        special_char = ['*', '#', '@', '$', '%', '^', '&', "(", ")", "-", "+"]
        alphab = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  '0', ' ', ',']
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


    def get_sentences(self, trans_text):
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        text = trans_text
        sentences = sentence_detector.tokenize(text.strip())

        return sentences


    def generate_summary(self, text, top_n):
        nltk.download("stopwords")
        stop_words = stopwords.words('english')
        summarize_text = [] 

        sentencesArray                  = self.get_sentences(text)

        cleanSentences                  = self.clean_sentences(sentencesArray)

        sentence_similarity_martix      = self.build_similarity_matrix(cleanSentences, stop_words)

        scores                          = self.pageTextRank(sentence_similarity_martix)

        rankedText                      = self.rankTOP(cleanSentences, scores, top_n, summarize_text)
     
        return rankedText
    

