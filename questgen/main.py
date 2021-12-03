import os
from flask import Flask, request
from Questgen import main as nlp

app = Flask(__name__)
bool_qgen = nlp.BoolQGen()
multi_qgen = nlp.QGen()


@app.route('/generate_question', methods=('POST',))
def generate_question():
    input_ = request.json
    output = None

    if input_['type'] == 'MCQ':
        output = multi_qgen.predict_mcq({'input_text': input_['input_text']})
        output = output['questions']
    elif input_['type'] == 'Bool':
        output = bool_qgen.predict_boolq({'input_text': input_['input_text']})
        output['Questions'] = output['Boolean Questions']

    if not output:
        return {
            'output': 'Something happened and the algorithm failed to return anything, most likely the text is too short'
        }, 500
    return {
        'output': output
    }


if __name__ == '__main__':
    app.run(debug=True)
