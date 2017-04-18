# myretail-restful-service
Technical Assessment Case Studies

Written in Python. Uses Falcon for REST.
Uses Docker for running in a container.

## Using Docker to run this application

### Build
  - `docker build --tag myretail-restful-service .`

### Run (using gunicorn)
  - `docker run --rm \
    --name myretail-restful-service \
    -p 8080:8080 \
    myretail-restful-service`

### Show
  - `curl http://localhost:8080`
  - alternatively, open `http://localhost:8080` in a web browser