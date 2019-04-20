FROM kennethreitz/pipenv

COPY . /app

CMD gunicorn app:app -b 0.0.0.0:5000
