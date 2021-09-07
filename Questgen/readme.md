# This is the question generation module using the [Questgen Library](https://github.com/ramsrigouthamg/Questgen.ai)
### Due to the dependencies of this library it is necessary to run it as a different python environment(python 3.7)

## Dependencies 
Python 3.7 \
Flask \
Spacy 2.2.4 \
[Questgen](https://github.com/ramsrigouthamg/Questgen.ai)  

## Setup
For the multiple choice questions to work you need to download and extract zip of [Sense2vec wordvectors](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz).
Extraction can be done with tools for working with archives such as Winrar or 7zip.
```
python -m pip install -U pipenv
pipenv install && pipenv shell
python main.py
```
## Usage
This is a flask mini web-application with a single endpoint - `/generate_question`, that runs on port 5000.
It accepts json input with key `input_text`
### Example  usage
```
curl http://localhost:5000/generate_question -X POST -H "Content-Type: application/json" -d '{"input_text": "I have to save this coupon in case I come back to the store tomorrow."}'
```
#### Response
```json
{
  "output": [
    {
      "answer": "coupon",
      "context": "I have to save this coupon in case I come back to the store tomorrow.",
      "extra_options": [
        "Voucher",
        "Entire Purchase",
        "Free Shipping",
        "Regular Price"
      ],
      "id": 1,
      "options": [
        "Gift Card",
        "Discount",
        "Promo Code"
      ],
      "options_algorithm": "sense2vec",
      "question_statement": "What do I need to save in case I come back to the store tomorrow?",
      "question_type": "MCQ"
    }
  ]
}

```
