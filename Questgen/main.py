from flask import Flask, request
import Questgen

from answer_processing.clean_answer import clean_answer

app = Flask(__name__)
nlp = Questgen.main.QGen()

@app.route('/generate_question', methods=('POST',))
def generate_question():
    input = request.json
    output = nlp.predict_mcq(input)
    output_list = []
    if len(output) == 0:
        return {
        'output': "Something happened and the algorithm failed to return anything, most likely the text is too short"
    }
    return {
        'output': output['questions']
    }


if __name__ == '__main__':
    app.run(debug=True)