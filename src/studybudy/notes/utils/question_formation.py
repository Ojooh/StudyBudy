import re, nltk, sys, json, random
from random import randint
from nltk.corpus import wordnet as wn
# from textblob import TextBlob
from nltk import RegexpParser
from nltk.tag import StanfordNERTagger
from nltk.stem import WordNetLemmatizer
STANFORD_NER_CLASSIFIER = '../models/stanford-models/english.all.3class.distsim.crf.ser.gz'
STANFORD_NER_CLASSPATH = '../models/stanford-models/stanford-ner.jar'

class QuestionFormation:

    def __init__(self):
        self.st             = StanfordNERTagger(STANFORD_NER_CLASSIFIER, STANFORD_NER_CLASSPATH, encoding='utf-8')
        self.sp             = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'who', 'Each', 'other', 'one another']
        self.ob             = ['me', 'him', 'her', 'it', 'us', 'you', 'them', 'whom']
        self.pp             = ['mine', 'yours', 'his', 'hers', 'ours', 'theirs']
        self.dp             = ['this', 'that', 'these', 'those']
        self.ip             = ['who', 'whom', 'which', 'what', 'whose', 'whoever', 'whatever', 'whichever', 'whomever']
        self.rp             = ['who', 'whom', 'whose', 'which', 'that', 'what', 'whatever', 'whoever', 'whomever', 'whichever']
        self.ref_p          = ['myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves']
        self.in_p           = ['myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves']
        self.ind_p          = ['Anything', 'everybody', 'another', 'each', 'few', 'many', 'none', 'some', 'all', 'any', 'anybody', 'anyone', 'everyone', 'everything', 'no one', 'nobody', 'nothing', 'none', 'other', 'others', 'several', 'somebody', 'someone', 'something', 'most', 'enough', 'little', 'more', 'both', 'either', 'neither', 'one', 'much', 'such']

    def concatenate_bin_list(self, bin, t, list_t):
        my_lst_str  = ""
        for x in list_t:
            if x != "not":
                if x == "but" or x == "and" or x == "." :
                    break
                else:
                    # my_lst_str = ' '.join(x)
                    my_lst_str += x + " "

        return my_lst_str + ' ?'


    def concatenate_list(self, list_t):
        my_lst_str  = ""
        for x in list_t:
            if x == "but" or x == "and" or x == "." :
                break
            else:
                my_lst_str += x + " "

        return my_lst_str + ' ?'


    def get_options(self, word):
        syn         = list()
        ant         = list()
        options     = []
        randy       = ['hallstattian', 'titillated', 'noncustomary', 'unencounterable', 'consubstantiated', 'doxographer', 'superglottic', 'schlesien', 'nonmicroscopical'
                        'redbone', 'sonorously', 'tetanically', 'izzard', 'impermissible', 'grassiness', 'sesquialtera', 'vaccinate', 'coak', 'oftenness', 'monotron']

        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                syn.append(lemma.name())
                if lemma.antonyms():
                    ant.append(lemma.antonyms()[0].name())

        
        tik     = 0
        while tik <= 5:
            rand_3  = random.choice(randy)
            if len(syn) != 0:
                rand_1 = random.choice(syn)
                if rand_1 not in options:
                    options.append(rand_1.lower()) 
                    tik += 1 
            if len(ant) != 0:
                rand_2 = random.choice(ant)
                if rand_2 not in options:
                    options.append(rand_2.lower())
                    tik += 1
            if rand_3 not in options:
                options.append(rand_3.lower())
                tik += 1
        if word not in options:
            value           = random.randint(0, 4)
            options[value]  = word

        return options


    def get_antonym(self, word):
        ant         = list()

        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                if lemma.antonyms():
                    ant.append(lemma.antonyms()[0].name())

        if len(ant) != 0:
            randh = random.choice(ant)
            if randh.lower != word.lower and not randh.startswith(word):
                return True, randh
        else:
            return False, word


    def genrate_mutiple_options(self, answer_list):
        options     = []
        new_options = [x for x in answer_list]
        tagged = nltk.pos_tag(answer_list)  

        while len(options) <= 5:
            
            if len(tagged) != 0:
                nit = 0
                dix = 0
                word= ""
                nn  = []
                for word, tag in tagged:
                    if tag.startswith("JJ") or tag.startswith("NN") and word not in nn:
                        word = word
                        nn.append(word)
                        nit  = dix
                        break
                    dix += 1
                new_words = self.get_options(word)

                for i in range(len(new_words)):

                    if word != "" :
                        new_options[nit]  = new_words[i]
                        opt               = self.concatenate_list(new_options)
                        if opt.lower() not in options and len(options) <= 5:
                            options.append(opt)
                        else:
                            break

            else:
                break

        ans = self.concatenate_list(answer_list)
        if ans not in options and len(options) > 0:
            value = random.randint(0, 4)
            options[value] = ans

        return options


    def determine_noun(self, noun_arr):
        for x in noun_arr:
            if len(x) <= 2:
                noun_arr.remove(x)
            else:
                if x in self.sp or x in self.ob or x in self.pp or x in self.dp or x in self.ip or x in self.rp or x in self.ref_p or x in self.in_p or x in self.ind_p:
                    noun_arr.remove(x)

        rand = random.choice(noun_arr)
        return rand


    def transform_binary_to_be(self, vb, indx, jj, wordArray):
        wa                 = [x for x in wordArray]
        print(wa)
        if jj is not None:
            lemmatizer  = WordNetLemmatizer()
            state, new_adj     = self.get_antonym(wa[jj])
            wa[jj]      = lemmatizer.lemmatize(new_adj)
        wa.pop(indx)
        wa.insert(0, vb)
        
        
        ques = self.concatenate_bin_list(vb,0, wa)
        return ques, wa


    def transform_binary_to_like(self, vb, indx, wordArray):
        lemmatizer  = WordNetLemmatizer()
        lemma       = lemmatizer.lemmatize(vb)
        wa          = wordArray
        wa[indx]    = lemma
        i           = indx - 1
        wa.insert(i, 'does')
        new_arr     = wa[i:]
        
        return self.concatenate_bin_list(vb, i, new_arr)


    def transform_fill(self, replace_nouns, wordArray):
        blanks_phrase = '__________ '.strip()
        chosen_noun = self.determine_noun(replace_nouns)
        for n in range(len(wordArray)):
            if wordArray[n] == chosen_noun:
                wordArray[n] = blanks_phrase

        ques    = self.concatenate_list(wordArray)
        options = self.get_options(chosen_noun)
        answer  = chosen_noun

        return ques, answer, options


    def transform_wh(self, wh_list):
        wa               = [x.title() for x in wh_list]
        classified_text  = self.st.tag(wa)
        idx              = 0
        cont             = len(classified_text)
        word_arr         = []
        answer           = []
        person = ''
        for word, tag in classified_text:
            person += word + " "
            if idx != cont - 1 and tag.startswith('PERSON') and (classified_text[(idx + 1)][0] == 'Is' or classified_text[(idx + 1)][0] == 'Was'):
                # person = word
                word_arr.append('Who')
                if classified_text[(idx + 1)][0] == 'Is':
                    word_arr.append('is')
                else:
                    word_arr.append('was')

                word_arr.append(person)
                tea = idx
                while tea != cont - 1:
                    if not classified_text[(tea + 1)][0] == 'Is':
                        if classified_text[(tea + 1)][0] == 'Was':
                            pass
                        else:
                            answer.append(classified_text[(tea + 1)][0].lower())
                    tea += 1

                person = ""
                break

            elif idx != cont - 1 and tag.startswith('LOCATION') and (classified_text[(idx + 1)][0] == 'Is' or classified_text[(idx + 1)][0] == 'Was'):
                # person = word
                word_arr.append('Where')
                if classified_text[(idx + 1)][0] == 'Is':
                    word_arr.append('is')
                else:
                    word_arr.append('was')

                word_arr.append(person)
                tea = idx
                while tea != cont - 1:
                    if not classified_text[(tea + 1)][0] == 'Is':
                        if classified_text[(tea + 1)][0] == 'Was':
                            pass
                        else:
                            answer.append(classified_text[(tea + 1)][0].lower())
                    tea += 1

                person = ""
                break

            elif idx != cont - 1 and tag.startswith('O') and (classified_text[(idx + 1)][0] == 'Is' or classified_text[(idx + 1)][0] == 'Was'):
                # person = word
                word_arr.append('What')
                if classified_text[(idx + 1)][0] == 'Is':
                    word_arr.append('is')
                else:
                    word_arr.append('was')

                word_arr.append(person)
                tea = idx
                while tea != cont - 1:
                    if not classified_text[(tea + 1)][0] == 'Is':
                        if classified_text[(tea + 1)][0] == 'Was':
                            pass
                        else:
                            answer.append(classified_text[(tea + 1)][0].lower())
                    tea += 1
                person = ""
                break
                
            idx += 1

        if len(word_arr) > 0:
            ques = self.concatenate_list(word_arr)
            ans  = self.concatenate_list(answer)
            opt  = self.genrate_mutiple_options(answer)
            return ques, ans, opt
        else:
            return None, None, None


