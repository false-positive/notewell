import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['TRANSFORMERS_CACHE'] = os.path.join(dir_path, 'model_cache')

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-3")
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-3")

def sum_text(input_text):
    inputs = tokenizer(input_text, return_tensors='pt')
    encoded = model.generate(inputs['input_ids'])
    result = tokenizer.batch_decode(encoded, skip_special_tokens=True)[0]
    return {'result': result}
