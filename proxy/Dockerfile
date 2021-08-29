FROM ubuntu:latest

WORKDIR /app

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install git

# copy files
COPY /. .

# install packages
RUN pip install -r requirements.txt
# install fixed fastapi-limiter since official package got a unfixed bug
RUN git clone https://github.com/marvingabler/fastapi-limiter && cd fastapi-limiter && pip install .

# get args from docker-compose.yml
ARG ssl
ARG cert
ARG cert-key
ARG host
ARG port
ARG rate-limit
ARG rate-reset

# copy ssl cert
ADD ${cert} ${cert}
ADD ${cert-key} ${cert-key}

# expose port
EXPOSE 433

# start proxy server
ENTRYPOINT ["python", "app.py"]
