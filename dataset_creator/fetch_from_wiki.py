import spacy, os, time, wikipedia
import pandas as pd
from string import punctuation
from spacy import displacy

#dataset = pd.read_excel("Chemistry.xlsx")
#dataset_x = dataset.iloc[:, 0].values
#dataset_x = []
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['TRANSFORMERS_CACHE'] = os.path.join(dir_path, 'model_cache')
dataset = open("new_dataset.txt", "a", encoding="utf-8")

#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
#
#tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-3")
#model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-3")

#def sum_text(text):
#    inputs = tokenizer(text, return_tensors='pt')
#    encoded = model.generate(inputs['input_ids'])
#    result = tokenizer.batch_decode(encoded, skip_special_tokens=True)[0]
#    return result

def extract_keywords(nlp, sequence, special_tags: list = None):
    """ Takes a Spacy core language model,
    text sequence of text and optional
    list of special tags as arguments.

    If any of the words in the text are
    in the list of special tags they are immediately
    added to the result.

    Arguments:
        sequence {str} -- text sequence to have keywords extracted from

    Keyword Arguments:
        tags {list} --  list of tags to be automatically added(words to be automatically added as a keyword) (default: {None})

    Returns:
        {set} -- set of the unique keywords extracted from a text
    """
    result = []

    # custom list of part of speech tags we are interested in
    # we are interested in proper nouns, nouns, and adjectives
    # edit this list of POS tags according to your needs.
    pos_tag = ['PROPN', 'NOUN']

    # create a spacy doc object by calling the nlp object on the input sequence
    doc = nlp(sequence)
    for ent in doc.ents:
        sequence = sequence.replace(ent.text, "")
    doc = nlp(sequence.lower())
    # if special tags are given and exist in the input sequence
    # add them to results by default

    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)

    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk = final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())

    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))


#def gen_keywords_excel():
#    # dataset = pd.read_excel("Chemistry.xlsx")
#    # dataset_x = dataset.iloc[:, 0].values
#    dataset_x = []
#    nlp = spacy.load("en_core_web_sm", exclude=['tagger', 'parser', 'attribute_ruler', 'lemmatizer'])
#    nlp.add_pipe('sentencizer')
#    keyword_nlp = spacy.load("en_core_web_sm", exclude=['lemmatizer', 'ner'])
#    i = 0
#
#    for article in dataset_x:
#        if i >= 4:
#            break
#        if type(article) != float:
#            if "Key concepts" in article:
#                continue
#            if len(article.replace(' ', '')) > 1024:
#                article_doc = nlp(article)
#                tempSents = []
#                for sent in article_doc.sents:
#                    tempSents.append(sent.text)
#                k = 0
#                while len(article) > 1024:
#                    article = article.replace(tempSents[k], '')
#                    k += 1
#            i += 1
#            keywords = extract_keywords(nlp=keyword_nlp, sequence=sum_text(article))
#            keyword_text = ' '.join(keywords)
#            keyword_doc = nlp(keyword_text)
#            for ent in keyword_doc.ents:
#                keyword_text = keyword_text.replace(ent.text, '')
#            #print(keywords)
#            print('{"text": "' + keyword_text + '", "label": "chemistry", "metadata": []}')


def gen_keywords_wiki(topic):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    titles = open("wikipedia_input.txt", encoding="utf-8")
    i = 0
    keyword_nlp = spacy.load("en_core_web_sm", exclude=['lemmatizer', 'ner'])
    for title in titles:
        print(title)
        if '\n' in title:
            title = title.replace('\n', '')
        i += 1
        if i % 100 != 0:
            time.sleep(5)
            keywords = extract_keywords(nlp=keyword_nlp, sequence=wikipedia.summary(title, auto_suggest=False, redirect=True))
        sub_lists = list(chunks(keywords, 12))
        for sub_list in sub_lists:
            if len(sub_list) < 12:
                continue
            else:
                result = '{"text": "' + " ".join(set(sub_list)) + '", "label": "' + topic + '", metadata": []}'
                print(result)
                dataset.write(result + '\n')
    dataset.close()

gen_keywords_wiki(input("input topic: "))