from distutils.core import setup

setup(name='notewell',
      version='0.1.0',
      description='Notewell ai stuff',
      author='Notewell contributors',
      packages=['notewell', 'notewell.Moderation_models', 'notewell.Questgen', 'notewell.Summarization'],
      url="https://github.com/false-positive/notewell.git",
      install_requires=[
          'scibert @ git+https://github.com/CodenameSource/scibert.git',
          'spacy==2.2.4',
          'Questgen @ git+https://github.com/ramsrigouthamg/Questgen.ai.git',
          'pke @ git+https://github.com/boudinfl/pke.git',
          'overrides==3.1.0'

      ],
      package_data={'Notewell': ['questgen.py', 'summarization.py', 'load_moderation.py']}
      )