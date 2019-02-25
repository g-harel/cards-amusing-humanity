# API 

Here are the services offered by the API.

## Cards

### Questions

Let you **insert/update/delete/read** questions from the questions table.

### Answers

Let you **read** answers from the answers table.

### Brewer

Let you obtain a random question or answer from the
tables.

### Cards Services


|    Cards       | HTTP  Method                  | Route                       |  Description                    |
|----------------|-------------------------------|-----------------------------|----------------------------------|
| Brewer         |`GET`                          |`api/brewer/answers` | Get a number of answer card in random order |
| Brewer         |`GET`                          |`api/brewer/questions` | Get a number of question card in random order |
| Answers         |`GET`                          |`api/answers/{id}` | Get a specific answer card        |
| Answers         |`GET`                          |`api/answers` | Get all answer cards        |
| Questions         |`GET`                          |`api/questions/{id}` | Get a specific question card        |
| Questions         |`GET`                          |`api/questions` | Get all question cards        |
| General         |`GET`                          |`/` | Get home page of service        |
