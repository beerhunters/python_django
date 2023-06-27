FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

#COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip "poetry==1.5.1"
RUN poetry config virtualenvs.create false --local
#RUN pip3 install -r requirements.txt
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .

CMD [ "gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8080" ]