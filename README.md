# django-template
a homemade django template for my remote cluster and local development 

## TL'DR
```shell
$ django-admin startproject \
  --template=https://github.com/DrChai/django-template/archive/main.zip \
  --extension=py,yml,yaml,env,toml \
  your_project_name
$ cd your_project_name  
$ cp config/.env . # then edit
# Generate up-to-date lock file: pdm lock / poetry lock

```
## Running as Docker Container
### Docker build
```shell
$ cp config/docker/python:slim/Dockerfile . # alpine version: config/docker/python:alpine/Dockerfile
$ cp config/settings_override.dev.py ./docker.settings_override.py
$ docker build -t ctn_name . # build for production
$ docker build -t ctn_name --build-arg DEBUG=true . # build for development
```
### Docker run (local development)
```shell
$ touch db.sqlite3 # create a db file for volume mapping if needed for local development
$ docker run --rm -it --env-file .env -p 8000:8000 -v $PWD/db.sqlite3:/app/db.sqlite3 ctn_name ./start-server.sh python manage.py runserver 0.0.0.0:8000
```
## Running with Docker Compose
```shell
$ touch db.sqlite3 # create a db file for volume mapping if needed for local development
$ cp config/docker/python:slim/Dockerfile .
$ cp config/settings_override.dev.py ./docker.settings_override.py # a production version for example: config/settings_override.prod.py
$ cp config/docker-compose/docker-compose.override.dev.yml docker-compose.override.yml # a production version for example: config/docker-compose/docker-compose.override.prod.yml
$ docker-compose up --build -d
```
## Examples of production configuration
* [**Docker**](https://github.com/DrChai/django-template/tree/main/config/docker)
* [**Kubernetes**](https://github.com/DrChai/django-template/tree/main/config/k8s)