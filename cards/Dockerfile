FROM python:3.6

MAINTAINER winterhart <m.user.work@gmail.com>

WORKDIR /home/cards
COPY . .

ENV HOST 0.0.0.0
ENV PORT 8000
ENV DEBUG true

RUN pip3 install -r requirements.txt
EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
