FROM python:3.8
MAINTAINER Åke Brissman <ake.brissman@gmail.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
        sqlite3

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data
RUN mkdir -p /app/gateway
RUN mkdir -p /app/instance

COPY app.py /app
COPY README.md /app
COPY gateway /app/gateway
COPY utils /app/utils
COPY instance /app/instance
# COPY migrations /app/migrations

ARG BUILD_VERSION
ENV SERVICE_BUILD_VERSION ${BUILD_VERSION}
ENV SERVICE_HOST_URL ''

EXPOSE 5010

VOLUME ["/gateway_service"]

CMD ["python", "app.py"]
