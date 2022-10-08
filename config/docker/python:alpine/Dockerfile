# build stage
FROM python:alpine AS builder
# install Python/Django depencies
RUN apk add --update --no-ache --virtual .tmp \
    gcc libc-dev linux-headers make \
    # pillow
    jpeg-dev zlib-dev \
    # cffi
    libffi-dev \
    # postgres (alt. option: musl-dev postgresql-dev)
    libpq-dev
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
FROM python:alpine AS production
ENV PYTHONPATH=/app/pkgs
ENV PYTHONUNBUFFERED 1
ENV PATH "/app/bin:${PATH}"
COPY --from=builder /app/__pypackages__/3.*/lib /app/pkgs
COPY --from=builder /app/__pypackages__/3.*/bin /app/bin
COPY --from=builder /app/src /app
WORKDIR /app
RUN chmod u+x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000
VOLUME ["/app/static", "/app/media"]
