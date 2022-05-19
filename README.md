# django-template
a homemade django template for my remote cluster and local development 

## TL'DR
```shell
$ django-admin startproject \
  --template=https://github.com/DrChai/django-template/archive/main.zip \
  --extension=py,yml,yaml,env,toml \
  project_name  
$ mv examples/env .env # then edit
# Generate up-to-date lock file: pdm lock / poetry lock

```
## Running as Docker Container
### Docker build
```shell
docker build -t ctn_name . # build for production
docker build -t ctn_name --build-arg DEBUG=true . # build for development
```
### Docker run (local development)
```shell
touch db.sqlit3 # create a db file for volume mapping if needed
docker run --rm -it --env-file .env -p 8000:8000 -v $PWD/db.sqlit3:/app/db.sqlit3 ctn_name ./start-server.sh python manage.py runserver 0.0.0.0:8000
```
## Running as Docker Compose
```shell
$ touch db.sqlit3 # create a db file for volume mapping if needed
$ cp examples/settings_override.dev.py ./docker.settings_override.py
$ cp examples/docker-compose.override.dev.yml docker-compose.override.yml
$ docker-compose up --build -d
```
## Examples of production configuration
* [**Docker**](https://github.com/DrChai/django-template/tree/main/examples/docker)
* [**Kubernetes**](https://github.com/DrChai/django-template/tree/main/examples/k8s)