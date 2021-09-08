# django-template
a homemade django template for my remote cluster and local development 

## TL'DR
```shell
$ django-admin startproject \
  --template=https://github.com/DrChai/django-template/archive/main.zip \
  --extension=py,yml,yaml,env \
  project_name
$ mv examples/env .env # then edit
$ mv examples/docker-compose.override.dev.yml docker-compose.override.yml
$ docker-compose build
```
## Examples of production configuration
* [**Docker**](https://github.com/DrChai/django-template/tree/main/examples/docker)
* [**Kubernetes**](https://github.com/DrChai/django-template/tree/main/examples/k8s)