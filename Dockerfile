FROM python:slim
ENV PYTHONUNBUFFERED 1
ARG DEBUG=false
RUN mkdir /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends pipenv \
    # Geospatial
    binutils libproj-dev gdal-bin \
    # Optional1
#    g++ apt-utils gcc libssl-dev openssl curl \
    # Optional2
#    git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile
#running: docker run -it --rm -v $PWD:/app -w /app python:3-slim
COPY Pipfile.lock Pipfile.lock
#RUN pip install -U pip pipenv
ADD . /app/
RUN chmod a+x /app/entrypoint.sh
RUN if [ "$DEBUG" = "true" ] ; then pipenv install --dev --deploy --system; else pipenv install --deploy --system ; fi
ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000
VOLUME ["/app/static", "/app/media"]
