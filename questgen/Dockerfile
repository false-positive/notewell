FROM python:3.7

WORKDIR /app

# XXX: maybe we should mirror this
RUN wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
RUN tar -xvf  s2v_reddit_2015_md.tar.gz

# Dependenciess --
# Has to be done first, so we don't re-install when code changes
COPY requirements.txt /app
RUN pip install -r requirements.txt gunicorn
RUN python -m spacy download en
RUN python -m nltk.downloader brown popular stopwords universal_tagset

COPY main.py /app
ENV FLASK_ENV production

EXPOSE 5000
CMD ["gunicorn", "--bind", ":5000", "--workers", "1", "--timeout", "12000", "main:app"] # XXX: timeout too long, download = bad
