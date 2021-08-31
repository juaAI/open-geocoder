FROM ubuntu:latest

WORKDIR /app

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install wget pbzip2 bzip2 sudo openjdk-13-jre -y

# get latest osm data
EXPOSE 2322
WORKDIR /root
COPY entrypoint.sh .

ENTRYPOINT ["sh","entrypoint.sh"]
