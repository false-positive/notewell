import os
from flask import Flask, request
from Questgen import main as nlp

app = Flask(__name__)
bool_qgen = nlp.BoolQGen()
multi_qgen = nlp.QGen()


@app.route('/generate_question', methods=('POST',))
def generate_question():
    # input_ = request.json
    question_type = request.json.get('type').lower()
    input_text = request.json.get('input_text').lower()

    output = None

    if question_type == 'mcq':
        output = multi_qgen.predict_mcq({'input_text': input_text})
        output = output['questions']
    elif question_type == 'bool':
        output = bool_qgen.predict_boolq({'input_text': input_text})
        output['questions'] = output['Boolean Questions']

    if not output:
        return {
            'output': 'Something happened and the algorithm failed to return anything, most likely the text is too short'
        }, 500
    return {
        'output': output
    }


if __name__ == '__main__':
    app.run(debug=True)
