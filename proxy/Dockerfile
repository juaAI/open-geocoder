FROM ubuntu:latest

WORKDIR /app

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install git python3-pip -y

# copy files
COPY /. .

# install packages
RUN pip3 install -r requirements.txt
# install fixed fastapi-limiter since official package got a unfixed bug
RUN pip3 install git+git://github.com/marvingabler/fastapi-limiter

# set env args
ENV cert=certs/cert.pem
ENV certkey=certs/privkey.pem
ENV ratelimit=100
ENV ratereset=60

# expose port
EXPOSE 443

# start proxy server
ENTRYPOINT ["python3", "server.py"]
