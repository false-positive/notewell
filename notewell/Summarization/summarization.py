import os
from spacy.pipeline import Sentencizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['TRANSFORMERS_CACHE'] = os.path.join(dir_path, 'model_cache')
#os.environ['TRANSFORMERS_CACHE'] = 'D:\huggingface\cache'


class Summarizer:
    def __init__(self):
        self.nlp = Sentencizer()
        self.tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-3")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-3") # TODO: Change to right method

    def _preprocess_text(self, input_text):
        input_text = input_text.replace("'", '')
        temp_text = input_text.split('\n')
        output_text = {}
        for id, text in enumerate(temp_text):
            output_text['Title' + str(id)] = []
            if len(text) > 1000:
                doc = self.nlp(text)
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


    def sum_text(self, input_text):
        payload = self._preprocess_text(input_text)
        result = {}
        for txt_id, text_dict in enumerate(payload):
            for text in payload[text_dict]:
                inputs = self.tokenizer(text, return_tensors='pt')
                encoded = self.model.generate(inputs['input_ids'])
                result['Title' + str(txt_id)] = []
                result['Title' + str(txt_id)].append(self.tokenizer.batch_decode(encoded, skip_special_tokens=True)[0])
        return {'result': result}


