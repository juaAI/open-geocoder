FROM ubuntu:latest

WORKDIR /app

RUN echo $(ls /home/morpheus/)

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install git python3-pip -y

# copy files
COPY /. .

# install packages
RUN pip3 install -r requirements.txt
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
COPY ${cert} ${cert}
COPY ${cert-key} ${cert-key}

# expose port
EXPOSE 433

# start proxy server
ENTRYPOINT ["python3", "app.py"]
