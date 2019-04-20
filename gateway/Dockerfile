FROM kennethreitz/pipenv

COPY . /app

CMD gunicorn --workers=2 app:app -b 0.0.0.0:5000
