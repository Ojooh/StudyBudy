import time, json, os
from .utils.sentence_processing import SentenceProcessing
from .utils.question_categories import  QuestionCategories
from .utils.summary import Summarizey
from studybudy.settings import BASE_DIR



class Application:
    def ques_application(self, rawtext, filename):
        sf = SentenceProcessing()
        qc = QuestionCategories()

        processed_text = sf.prepare_sentences(rawtext)

        if processed_text is not  None:
            questions_answers, info = qc._categorize_sentences_(processed_text)
            output = os.path.join(BASE_DIR+'/templates/', 'notes/Questions/' + filename + "-" + "evaluation_questions.json")

            # output = "questions/" + filename + "-" + "evaluation_questions.json"

            with open(output, 'w+') as output_file:
                json.dump(questions_answers, output_file, sort_keys=True, indent=4)
                

            print("Questions generated: \n")
            print("saved in json file, path is: " + output)

            return questions_answers, info, len(questions_answers)
    
    def summary_application(self, rawtext, number):
        sm         = Summarizey()
        sumText    = sm.generate_summary(rawtext, number)

        return sumText
