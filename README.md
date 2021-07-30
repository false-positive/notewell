# notewell
The notewell project.

Here's how y'all can run the Django project (in `website/`). _(Works everywhere)_

    python -m pip install -U pipenv
    cd website/
    pipenv install && pipenv shell
    python manage.py migrate
    python manage.py runserver

Next you might want to `python manage.py createsuperuser` and use it to login to `/admin/` and create dummy data, such as users, notes, etc.
