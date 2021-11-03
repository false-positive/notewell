import os, requests
from spacy.lang.en import English
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['TRANSFORMERS_CACHE'] = os.path.join(dir_path, 'model_cache')
#os.environ['TRANSFORMERS_CACHE'] = 'D:\huggingface\cache'


nlp = English()
nlp.add_pipe("sentencizer")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-3")
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-3")


def preprocess_text(input_text):
    input_text = input_text.replace("'", '')
    temp_text = input_text.split('\n')
    output_text = {}
    for id, text in enumerate(temp_text):
        output_text['Title' + str(id)] = []
        if len(text) > 1000:
            doc = nlp(text)
            new_text = ""
            sent_len = 800
            if len(text) < 1600:
                sent_len = int(len(text)/2)
            for sent in doc.sents:
                if len(new_text) < sent_len:
                    new_text += sent.text
                else:
                    output_text['Title' + str(id)].append(new_text)
                    new_text = ""
            output_text['Title' + str(id)].append(new_text)
        elif len(text) > 10:
            output_text['Title' + str(id)].append(text)
    return output_text


def sum_text(input_text):
    payload = preprocess_text(input_text)
    result = {}
    for txt_id, text_dict in enumerate(payload):
        for text in payload[text_dict]:
            inputs = tokenizer(text, return_tensors='pt')
            encoded = model.generate(inputs['input_ids'])
            result['Title' + str(txt_id)] = []
            result['Title' + str(txt_id)].append(tokenizer.batch_decode(encoded, skip_special_tokens=True)[0])
    return {'result': result}


def gen_quest(input_text):
    r = requests.post('http://localhost:5000/generate_question', json={'input_text': input_text})
    return {'result': r.json()}
