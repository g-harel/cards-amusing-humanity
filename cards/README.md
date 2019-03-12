# SOEN 487 - A1

Microservice application providing basic services to play
*card against humanity*....

# Install all dependencies

> `cd a1`

>`pip install -r requirements.txt`


# Recreate Database

Simply enter:

`python -c 'from manage import recreate_db; recreate_db()'`

## Manually Initializing Database
First enter your credential as
`.env.example` following all variable.

I am currently using Postgres database.

You can run the `init_db` function which will create
the tables in your `postgres` database.

**Script:**

```
> cd .../a1
> python
>>> from datasource.init_database.py import init_db
>>> init_db()
```

## Manually Filling Database with Data

In resources you shall find a `cards.json` file
which contains all data for the `answers` and `questions`
tables.

To fill the tables from `cards.json` we need to run `fill_db`
from `fill_database.py`


**Script:**

```
> cd .../a1
> python
>>> from datasource.fill_database import fill_db
>>> fill_db()
```
You should wait 30 seconds for the database to be filled.

The default number of answers is 1000. 

The default number of questions is 100.

## Services

Here are the services and route offered by the API

### Questions

Let you **insert/update/delete/read** questions from the questions table.
The views **views/questions.py** contains CRUD operation.

##### Route:
- `GET`, `/api/questions` returns all questions stored in table
- `GET`, `/api/questions/<question_id>` return a specific question
- `POST`, `/api/questions` creates a question
- `PUT`, `/api/questions/<question_id>` updates specific question
- `DELETE`, `/api/questions/<question_id>` remove a question


### Answers

Let you **insert/update/delete/read** answers from the questions table.
The views **views/answers.py** contains CRUD operation.

##### Route:
- `GET`, `/api/answers` returns all answers stored in table
- `GET`, `/api/answers/<answer_id>` return a specific answer
- `POST`, `/api/answer` creates an answer
- `PUT`, `/api/answers/<answer_id>` updates specific answer
- `DELETE`, `/api/answers/<answer_id>` remove a specific answer

### Brewer

Let you obtain a random question or answer from the
tables.

##### Route:
- `GET`, `/api/brewer/answers/<number_of_item>` returns X number of random answers
- `GET`, `/api/brewer/questions/<number_of_item>` return X number of random questions

### Main

Basic server route configuration

#### Route:
- `/` obtain a JSON with student id and name
- `404` obtain custom error page

## Running Tests

All tests are written inside `tests` folder.

## Starting the Application

Simply run `flask run` after having the database setup.

## Deploy with Docker
