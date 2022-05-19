# build stage
FROM python:slim AS builder
# install Python/Django depencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # Geospatial
    binutils libproj-dev gdal-bin \
    # Optional
#    g++ apt-utils gcc libssl-dev \
    # Optional
#    git curl openssl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /app/
COPY . /app/src

# install PDM
ARG DEBUG=false
RUN pdm install --prod --no-lock --no-editable
RUN if [ "$DEBUG" = "true" ] ; then pdm install -G dev --no-lock --no-editable; fi


# run stage
FROM python:slim AS runner
ENV PYTHONPATH=/app/pkgs
ENV PYTHONUNBUFFERED 1

COPY --from=builder /app/__pypackages__/3.*/lib /app/pkgs
COPY --from=builder /app/src /app

WORKDIR /app
RUN chmod u+x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000
VOLUME ["/app/static", "/app/media"]
