import os
import Questgen
from flask import Flask, request


#os.environ['TRANSFORMERS_CACHE'] = 'D:\huggingface\cache' made this so huggingface transformers model in questgen could work on my pc with limited C: space left
app = Flask(__name__)
nlp = Questgen.main
boolQG = nlp.BoolQGen()
MQG = nlp.QGen()

@app.route('/generate_question', methods=('POST',))
def generate_question():
    input_ = request.json
    print(input_)
    output = ""
    if input_['type'] == 'MCQ':
        output = MQG.predict_mcq({'input_text': input_['input_text']})
        output = output['questions']
    elif input_['type'] == 'Bool':
        output = boolQG.predict_boolq({'input_text': input_['input_text']})
        output['Questions'] = output['Boolean Questions']
    if len(output) == 0:
        return {
            'output': 'Something happened and the algorithm failed to return anything, most likely the text is too short'
        }, 500
    return {
        'output': output
    }


if __name__ == '__main__':
    app.run(debug=True)
