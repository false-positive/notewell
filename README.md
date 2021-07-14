# notewell
The notewell `note app` project.

Here's how y'all can run the Django project (in `website/`). _(Works everywhere)_

    python -m pip install -U pipenv
    cd website/
    pipenv install && pipenv shell
    python manage.py migrate
    python manage.py runserver
