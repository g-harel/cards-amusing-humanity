# Cards Amusing Humanity

> Single-player "Cards Against Humanity" game.

Round starts and player sees a black card and a number of white cards. They pick which white card is the funniest match with the black one. The "winning" state is determined by historical results of what other people have answered to a similar question.

## Services

### Gateway

- serves static files for frontend
- entrypoint for all request
- handles routing
- rate limiting (by IP)

### Analytics (internal)

- records results from played rounds
- enforces round signatures and only accepts them once
- provides analytics on historical data (ex. most popular)

### Card (internal)

- contains card data
- creates rounds (and fetches a signature)

### Signing (internal)

- sign arbitrary payloads (ex. JSON string)
- verify signatures

## API

Service APIs are described using the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification).

[Gateway](./gateway/openapi.yaml) | [Analytics](./analytics/openapi.yaml) | [Cards](./cards/openapi.yaml) | [Signing](./signing/openapi.yaml)
--------------------------------- | ------------------------------------- | ----------------------------- | ---------------------------------

_These documents can be visualized using the [Swagger Editor](https://editor.swagger.io)._

## Students

Name          | Email                    | Student ID | Username
------------- | ------------------------ | ---------- | ----------------------------------
Charles Hardy | m.user.work@gmail.com    | 27417888   | [Winterhart](https://github.com/Winterhart)
Gabriel Harel | gabrielj.harel@gmail.com | 40006459   | [g-harel](https://github.com/g-harel)
