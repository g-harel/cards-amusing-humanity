# Cards Amusing Humanity

> Single-player "Cards Against Humanity" game.

Round starts and player sees a black card and a number of white cards. They pick which white card is the funniest match with the black one. The "winning" state is determined by historical results of what other people have answered to a similar question.

## Development

Each service's directory contains a `Dockerfile` which describes how the source code is packaged. Each directory also contains a kubernetes manifest (`manifest.yaml`) to configure how the image is deployed and what external services it needs (ex. database).

### Environment Setup

Tool     | Version      | Reason                         | Install
-------- | ------------ | ------------------------------ | ------------------------------------------------------------------------------
minikube | `>= v0.34.1` | Run kubernetes cluster locally | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/install-minikube/)
kubectl  | `>= v1.13.5` | Interact with the kube api     | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
skaffold | `>= v0.25.0` | Live build/deploy to cluster   | [skaffold.dev](https://skaffold.dev/docs/getting-started/#installing-skaffold)

### Running

**Create local cluster**

> `minikube start`

_This step can be skipped if your `kubeconfig` is already configured to access the desired cluster._

**Deploy application**

> `skaffold dev`

**Open website** _(Optional)_

> `minikube service website`

## Services

Service APIs are described using the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification).

[Gateway](./gateway/openapi.yaml) | [Analytics](./analytics/openapi.yaml) | [Cards](./cards/openapi.yaml) | [Signing](./signing/openapi.yaml)
--------------------------------- | ------------------------------------- | ----------------------------- | ---------------------------------

_These documents can be visualized using the [Swagger Editor](https://editor.swagger.io)._

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

## Students

Name          | Email                    | Student ID | Username
------------- | ------------------------ | ---------- | ----------------------------------
Charles Hardy | m.user.work@gmail.com    | 27417888   | [Winterhart](https://github.com/Winterhart)
Gabriel Harel | gabrielj.harel@gmail.com | 40006459   | [g-harel](https://github.com/g-harel)
