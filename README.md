# myretail-restful-service
Technical Assessment Case Studies

Written in Python. Uses Falcon for REST.
Uses Docker for running in a container.

# Requirements for Use
  - Docker installed locally
  - Redis-cli installed locally

## Initial Setup
Since there is no POST request available in this
application, we need to do a little setup with our
database before we can get started.
  1. Start up the redis server
    - https://github.com/sladebaumann/myretail-restful-service-redis
  2. Use the redis-cli (local version) to populate initial data hash
    - `redis-cli -h localhost -p 6379 ping`
    - `redis-cli HMSET 13860428 value 13.49 currency_code USD`
    - https://redis.io/topics/rediscli

You will need the Redis container service running while interacting
with this application.

## Using Docker to run this application

### Build
  - `docker build --tag myretail-restful-service .`

### Run (using gunicorn)
  - `docker run --rm --name myretail-restful-service --net=host -p 8080:8080 myretail-restful-service`

### Interact
  - GET a product by id
    - `curl localhost:8080/products/13860428`
    - alternatively, open `localhost:8080/products/13860428` in a web browser
  - PUT new value by id
  - `curl localhost:8080/products/13860428 -X PUT -H "Content-Type: application/json" -d '{"current_price": {"currency_code": "USD", "value": 11.99}, "id": 13860428, "name": "The Big Lebowski (Blu-ray)"}'`
