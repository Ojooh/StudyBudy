import nltk
from .question_formation import QuestionFormation

class QuestionCategories:
    def __init__(self):
        self.qf             = QuestionFormation()
        self.checkwords = ['who', 'what', 'where', 'why', 'whose']
        self.binary_keys1   = ['is', 'was', 'am', 'are', 'does']
        self.binary_keys2  = ['like', 'likes']
        self.bin_count      = 0
        self.tobe_count     = 0
        self.fill_count     = 0
        self.wh_count       = 0
        self.QuestioAnswer  = []
        self.wa_2           = []

    def _tokenize_sentences_(self, sample):
        word_tokenizer      = nltk.word_tokenize
        tagged_sentences    = []
        wordArray           = []
        for lem in sample:
            wordArray.append(word_tokenizer(lem))
            tagged = nltk.pos_tag(word_tokenizer(lem))
            tagged_sentences.append(tagged)

        return wordArray, tagged_sentences 


    
    def _categorize_(self, word_tokens, pos_tokens):
        idx         = 0
        VBZ         = ""
        nn_state    = False    
        replace_nouns   = []
        for token in pos_tokens:
            wA = word_tokens[idx]
            inx         = 0 
            inx_limit   = len(token) 
            JJ          = None       
            for word, tag in token:
                if word in self.checkwords:
                    continue

                if tag.startswith('NN') and word not in replace_nouns:
                    replace_nouns.append(word)
                    
                if word in self.binary_keys1:

                    if tag.startswith('VBZ') or tag.startswith('VBP') or tag.startswith('VBD'):
                        VBZ           = word
                        if token[inx + 1][0]  == "not":
                            answer  = "False"
                        else:
                            answer  = "True"  
                        if inx + 1 < inx_limit and token[inx + 1][1].startswith('JJ'):
                            JJ  = inx + 1
                        elif inx + 2 < inx_limit and token[inx + 2][1].startswith('JJ'):
                            JJ  = inx + 2
                        elif inx + 3 < inx_limit and token[inx + 3][1].startswith('JJ'):
                            JJ  = inx + 3
                        elif inx + 4 < inx_limit and token[inx + 4][1].startswith('JJ'):
                            JJ  = inx + 4

                        question_1, ans_1, opt_1 = self.qf.transform_wh(wA) 
                        if question_1 is not None:
                            rict = {}
                            rict['Full_qus']    = question_1
                            rict['Answer']      = ans_1
                            rict['options']     = opt_1
                            self.wh_count       += 1

                            self.QuestioAnswer.append(rict)
                            self.wh_count += 1


                        
                        
                        question, wa_2 = self.qf.transform_binary_to_be(VBZ, inx, JJ, wA)
                        self.wa_2 = [x for x in wa_2]
                        # if state:
                        #     answer  = "False"
                        # else:
                        #     ans = True
                        rict = {}
                        rict['Full_qus']    = question
                        rict['Answer']      = answer
                        rict['options']     = ['True', 'False']

                        self.QuestioAnswer.append(rict)
                        self.bin_count += 1
                        break


                if word in self.binary_keys2:
                    wa  = word_tokens[idx]
                    if tag.startswith('VBZ') or tag.startswith('VBP') or tag.startswith('VBD') or tag == 'NNS':
                        VBZ         = word
                        if token[inx - 1][0]  == "not":
                            answer  = "False"
                        else:
                            answer  = "True"
                        
                        question = self.qf.transform_binary_to_like(VBZ, inx, wa)
                        rict = {}
                        rict['Full_qus']    = questions
                        rict['Answer']      = answer
                        rict['options']     = ['True', 'False']
                        self.QuestioAnswer.append(rict)
                        self.tobe_count += 1


                inx += 1

            
            if len(replace_nouns) <= 1:
                pass
            else:
                questions, ans, opt  = self.qf.transform_fill(replace_nouns, wA)
                rict = {}
                rict['Full_qus']    = questions
                rict['Answer']      = ans
                rict['options']     = opt
                self.QuestioAnswer.append(rict)
                self.fill_count += 1
                # if len(self.wa_2) > 0:
                #     questions, ans, opt  = self.qf.transform_fill(replace_nouns, self.wa_2)
                #     rict = {}
                #     rict['Full_qus']    = questions
                #     rict['Answer']      = ans
                #     rict['options']     = opt
                #     self.QuestioAnswer.append(rict)
                #     replace_nouns       = []
                #     self.fill_count += 1
                replace_nouns       = []
            idx += 1

        # print(self.QuestioAnswer)
        return self.QuestioAnswer
               



    def _categorize_sentences_(self, processed):
        word_tokens, pos_tokens         = self._tokenize_sentences_(processed)
        result                          = self._categorize_(word_tokens, pos_tokens)
        quiz_info                       = []
        quiz_info.append(self.bin_count) 
        quiz_info.append(self.tobe_count)
        quiz_info.append(self.fill_count) 
        quiz_info.append(self.wh_count) 
        return result, quiz_info    