# This is the question generation module using the [Questgen Library](https://github.com/ramsrigouthamg/Questgen.ai)
### Due to the dependencies of this library it is necessary to run it as a different python environment(python 3.7)

## Dependencies 
Python 3.7 \
Flask \
Spacy 2.2.4 \
[Questgen](https://github.com/ramsrigouthamg/Questgen.ai)  

## Setup

### Multiple-choice questions
For the multiple choice questions to work you need to download and extract zip of [Sense2vec wordvectors](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz).

Extraction can be done under POSIX-compliant systems where `wget` and `tar` are available using:

```
wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
tar xvf s2v_reddit_2015_md.tar.gz 
rm ._s2v_old
```

### Starting the server
```
python -m pip install -U pipenv
pipenv install && pipenv shell
python main.py
```

## Usage
This is a flask mini web-application with a single endpoint - `/generate_question`, that runs on port 5000.
It accepts json input with key `input_text`. The mode of generation can be specified with `type` key.

### Example  usage
- One thing that is important to note is that for question generation to produce better results longer text is neccessary. 
#### Multiple choice questions
```
curl http://localhost:5000/generate_question -X POST -H "Content-Type: application/json" -d '{"input_text": "I have to save this coupon in case I come back to the store tomorrow.", "type": "MCQ"}'
```
##### Response
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
#### Question generation(Without answers)
```
curl http://localhost:5000/generate_question -X POST -H "Content-Type: application/json" -d '{"input_text": "Carbon is the 15th most abundant element in the Earth crust, and the fourth most abundant element in the universe by mass after hydrogen, helium, and oxygen. Carbon abundance, its unique diversity of organic compounds, and its unusual ability to form polymers at the temperatures commonly encountered on Earth enables this element to serve as a common element of all known life. It is the second most abundant element in the human body by mass after oxygen."}'
```
##### Response
```
{
  "output": [
    "Is carbon the most abundant element in the universe?",
    "Is carbon the second most abundant element in the universe?",
    "Is carbon the most abundant element in the human body?"
  ]
}
```
