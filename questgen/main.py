from flask import Flask, request
import Questgen

app = Flask(__name__)
nlp = Questgen.main


@app.route('/generate_question', methods=('POST',))
def generate_question():
    input_ = request.json
    if input_['type'] == 'MCQ':
        qe = nlp.QGen()
        output = qe.predict_mcq({'input_text': input_['input_text']})
        output = output['questions']
    elif input_['type'] == 'Bool':
        qe =nlp.BoolQGen()
        output = qe.predict_boolq({'input_text': input_['input_text']})
        output = output['Boolean Questions']
    if len(output) == 0:
        return {
            'output': 'Something happened and the algorithm failed to return anything, most likely the text is too short'
        }, 500
    return {
        'output': output
    }


if __name__ == '__main__':
    app.run(debug=True)
