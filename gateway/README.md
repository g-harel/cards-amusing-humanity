
# Gateway 

This service is responsible for filtering request to the cluster.
To increase its capabilities, the service is running on `Gunicorn` with 
by default 2 workers/threads. See the `Dockerfile` for more details.

## Testing

Gateway is using `PyTest` to run unit test.


To run all tests:
- install all package: `pipenv install`
- Use the virtual environment: `pipenv shell`
- run tests: `pytest`
