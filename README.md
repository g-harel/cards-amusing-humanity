# Cards Amusing Humanity ([Presentation](https://docs.google.com/presentation/d/e/2PACX-1vRnI3FzGfQP7HAtfErth3BHutfQhZUeoYBmgR2AI5FYu5TpVeT1nwxIfhhrkhEpDCQlClt80lbGrp52/pub?start=false&loop=false&delayms=2000))

> Single-player "Cards Against Humanity" game.

Player is presented with a board containing a question card (black) and a number of answer cards (white). They pick which answer card is the funniest match with the question. After making a pick, the player is shown a similarity score which is determined by historical results from what other players have answered to a similar board of cards.

## Development

All top level directories contain the source code for an individual, independent service. Each service directory contains a `Dockerfile` which describes how the source code is packaged. Each directory also contains a kubernetes manifest (`manifest.yaml`) to configure how the image is deployed and what external services it needs (ex. databases).

### Running

**Requirements**

Tool       | Version      | Reason                         | Install
---------- | ------------ | ------------------------------ | ------------------------------------------------------------------------------
`docker`   | `>= v18.3.1` | Build container images         | [docker.com](https://docs.docker.com/install/#supported-platforms)
`kubectl`  | `>= v1.13.5` | Interact with the kube api     | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
`minikube` | `>= v0.34.1` | Run kubernetes cluster locally | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/install-minikube/)
`skaffold` | `>= v0.25.0` | Live build/deploy to cluster   | [skaffold.dev](https://skaffold.dev/docs/getting-started/#installing-skaffold)

**Create local cluster**

```sh
minikube start
```

_This step can be skipped if your `kubeconfig` is already configured to access the desired cluster._

**Deploy application**

```sh
skaffold dev
```

_Note that this command might take some time to start showing application logs because it needs to pull container images._

_Some features will not work until all pods are ready. This can be checked using `kubectl get pods` or when there are no more error logs from the regular health checks._

**Open website (Optional)**

```sh
minikube service website
```

_This will open the website in your default browser._

### Testing

**Requirements**

Tool       | Version          | Reason                           | Install
---------- | ---------------- | -------------------------------- | -------------------------------------------------------------------------------------------
`pipenv`   | `>= v2018.11.26` | Python dependency management     | [pipenv.readthedocs.io](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
`node/npm` | `>= v11.10.0`    | JavaScript dependency management | [nodejs.org](https://nodejs.org/en/download/)

**Run tests**

```sh
./test
```

_This will go through each service directory to install dependencies, and run the tests._

_Script will exit immediately if any command exits with a non-zero code._

## Services

Service APIs are described using the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification).

[Analytics](./analytics/openapi.yaml) | [Cards](./cards/openapi.yaml) | [Gateway](./gateway/openapi.yaml) | [Signing](./signing/openapi.yaml) | [Website](./website/openapi.yaml)
------------------------------------- | ----------------------------- | --------------------------------- | --------------------------------- | ---------------------------------

_These documents can be visualized using the [Swagger Editor](https://editor.swagger.io)._

## Students

<table>
    <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Student ID</th>
        <th>Username</th>
        <th>Responsibilities</th>
    </tr>
    <tr>
        <td>Charles Hardy</td>
        <td><a href="mailto:m.user.work@gmail.com">m.user.work@gmail.com</a></td>
        <td>27417888</td>
        <td><a href="https://github.com/Winterhart">Winterhart</a></td>
        <td>
            <ul>
                <li>Cards Service</li>
                <li>Gateway Service</li>
                <li>Presentation</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Gabriel Harel</td>
        <td><a href="mailto:gabrielj.harel@gmail.com">gabrielj.harel@gmail.com</a></td>
        <td>40006459</td>
        <td><a href="https://github.com/g-harel">g-harel</a></td>
        <td>
            <ul>
                <li>Analytics Service</li>
                <li>Signing Service</li>
                <li>Website Service</li>
                <li>Presentation</li>
            </ul>
        </td>
    </tr>
</table>

## License

[MIT](/LICENSE)
