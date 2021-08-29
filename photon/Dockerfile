FROM ubuntu:latest

WORKDIR /app

# create low privilege user
RUN adduser --disabled-password --gecos '' photonuser
USER photonuser
WORKDIR /home/photonuser/
RUN chmod a+rwx /home/photonuser/

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install wget pbzip2 bzip2 sudo openjdk-13-jre -y

# get latest osm data
WORKDIR /home/photonuser/photon_data
RUN wget -O - https://download1.graphhopper.com/public/photon-db-latest.tar.bz2 | pbzip2 -cd | tar x
RUN ls .

# get latest photon release
WORKDIR /home/photonuser
RUN wget -O - https://github.com/komoot/photon/releases/download/0.3.5/photon-0.3.5.jar

# Expose port and start app
EXPOSE 2322
ENTRYPOINT ["java","-jar", "photon-*.jar"]
