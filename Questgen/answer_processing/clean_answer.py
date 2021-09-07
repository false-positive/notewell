import spacy
nlp = spacy.load("en_core_web_sm")

def clean_answer(question):
    context_doc = nlp(question['context'])

    full_answer = ""
    for ent in context_doc.ents:
        if question['answer'] in ent.text:
            if ent.text not in question['question_statement']:
                full_answer = ent.text
    return full_answer