# About
A RESTful API service providing access to bid data extracted from [MnDOT's published bid abstracts](https://www.dot.state.mn.us/bidlet/abstract.html).

View the OpenAPI docs: [https://mndotbidprices.com/api/v1/docs](https://mndotbidprices.com/api/v1/docs)

View the dashboard application powered by this API: [https://mndotbidprices.com/](https://mndotbidprices.com/)

# Develop
## Test Suite
Unit tests were developed using the pytest library. The following commands can be issued from the project root directory; pytest will handle test discovery. 
```
# Run most tests (completes in <10 seconds)
$ pytest
```
Some of the extract, transform, load (ETL) tests can take an extended amount of time to complete. These will be skipped unless the tag `--run-slow` is provided
```
# Run all tests (completes in 1-2 minutes)
$ pytest --run-slow
```


# Deploy
## Publish a new build
Run the following commands to build and push a new docker image to docker-hub
```
$ poetry version [patch, minor, or major]
$ docker build -t depowered/mndot-bid-api:tagname .
$ docker push depowered/mndot-bid-api:tagname
```

## Deploy with Docker Compose
1. Create a .env or .env file that contains the following variables
    ```
    API_KEY     # key for authenticating ETL, create, update, and delete routes
    DB_FILE     # sqlite file name
    ```

2. Rename the docker-compose.template.yml to docker-compose.yml
3. Configure the content of the .yml to point at the appropriate resources for the given host machine
4. Pull the docker image
    ```
    $ docker pull depowered/mndot-bid-api:tagname
    ```
5. Start the service
    ```
    $ docker compose up service
    ```