# notewell

The notewell project.

Here's how y'all can run the Django project (in `website/`). _(Works everywhere)_

    python -m pip install -U pipenv
    cd website/
    pipenv install && pipenv shell
    python manage.py migrate
    python manage.py loaddata fixtures/*.json
    python managepy changepassword admin
    python manage.py runserver

Then you can head on over to <http://localhost:8000/accounts/login/> and login as `admin` with the password you set above.
