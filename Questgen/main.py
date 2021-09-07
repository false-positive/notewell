from flask import Flask, request
import Questgen

from answer_processing.clean_answer import clean_answer

app = Flask(__name__)
nlp = Questgen.main.QGen()

@app.route('/generate_question', methods=('POST',))
def generate_question():
    input = request.json
    print(input)
    output = nlp.predict_mcq(input)
    print(output)
    print(clean_answer(output['questions'][0]))
    return {
        'output': output
    }


if __name__ == '__main__':
    app.run(debug=True)