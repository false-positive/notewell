from allennlp.models import load_archive
from allennlp.predictors.predictor import Predictor
from scibert.dataset_readers import classification_dataset_reader
from spacy.pipeline import Sentencizer


class Moderation:
    def __init__(self):
        self.quality_moderation = Predictor.from_path("./quality_classification/model.tar.gz", predictor_name="sentence-tagger")
        self.subject_classification = Predictor.from_path("./subject_classification/model.tar.gz", predictor_name="sentence-tagger")
        self.nlp = Sentencizer

    def _preprocess_text(self, input_text):
        input_text = input_text.replace("'", '')
        temp_text = input_text.split('\n')
        output_text = []
        for text in temp_text:
            if len(text) > 1000:
                doc = self.nlp(text)
                new_text = ""
                sent_len = 1000
                if len(text) < 2000:
                    sent_len = int(len(text)/2)
                for sent in doc.sents:
                    if len(new_text) < sent_len:
                        new_text += sent.text
                    else:
                        output_text.append(new_text)
                        new_text = ""
                output_text.append(new_text)
            elif len(text) > 10:
                output_text.append(text)
        return output_text


    def asses_quality(self, input_text):
        text_chunks = self._preprocess_text(input_text)
        good_score = 0
        bad_score = 0
        for chunk in text_chunks:
            score = self.quality_moderation.predict_json({"sentence": chunk})['class_probs']
            good_score += round(score[0],0)
            bad_score += round(score[1], 0)
        return str(int(good_score > bad_score))


    def find_subject(self, input_text):
        subject_scores = {"Chemistry": 0, "Physics": 0, "Biology": 0, "Computer Science": 0}
        prediction = self.subject_classification.predict_json({"sentence": input_text})['class_probs']
        for id, subject_score in enumerate(subject_scores):
            subject_scores[subject_score] = round(prediction[id], 3)
        return subject_scores
