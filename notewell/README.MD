# The notewell library
This is a library that combines the different ai algorithms used to make creating notes easier.
## Caviats
Installing the library happens with the git+ prefix `git+https://github.com/false-positive/notewell.git`

The [moderation models](https://drive.google.com/drive/folders/1xSoSajUtSy8YyDWEXeiSh7CyaFLBcJaE?usp=sharing) are provided separately and must be installed in the Moderation_models folder.

Another thing to note is for question generation to function properly [sense2vec](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz) should be downloaded, unarchived and placed in the Questgen folder.
## Instalation steps
1. Install using pip
```
pip install git+https://github.com/false-positive/notewell.git
```
2. Download the [moderation models](https://drive.google.com/drive/folders/1xSoSajUtSy8YyDWEXeiSh7CyaFLBcJaE?usp=sharing) and place them within the Moderation_models folder
3. Download and unarchive [sense2vec](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz) into the Questgen folder

# Usage
The library currently has 3 classes(Summarizer, Moderation, Question)
### Summarizer class
The `Summarizer` class has 1 method used for summarization - `sum_text`, it expects string input and returns a dictionary with summarized paragraphs
### Question
The `Question` class has 1 method thats used for question generation - `generate_question`, it expects string input and type of question to be generated(MCQ for question with provided answers, Bool for question generation without answers), it returns a dictionary with questions and metadata related to them
### Moderation
The `Moderation` class has 2 methods used for determining the quality and the category of a given text.
The first method is `asses_quality` which expects a string and returns 1 for a text with good quality and 0 for text with bad quality
The second is `find_subject` which expects a string and returns a dictionary with the categories
