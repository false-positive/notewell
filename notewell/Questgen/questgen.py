import os
import Questgen

dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['TRANSFORMERS_CACHE'] = os.path.join(dir_path, 'model_cache')


class Question:
    def __init__(self):
        self.nlp = Questgen.main
        self.boolQG = self.nlp.BoolQGen()
        self.MQG = self.nlp.QGen()

    def generate_question(self, input_text: str, type: str = "MCQ"):
        output = ""
        if type == 'MCQ':
            output = self.MQG.predict_mcq({'input_text': input_text})
            output = output['questions']
        elif type == 'Bool':
            output = self.boolQG.predict_boolq({'input_text': input_text})
            output['Questions'] = output['Boolean Questions']
        if len(output) == 0:
            return {
                'output': 'Something happened and the algorithm failed to return anything, most likely the text is too short'
            }
        return {
            'output': output
        }


