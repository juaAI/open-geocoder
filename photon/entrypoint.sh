cd /data
if [ -d "photon_data/elasticsearch" ]; then
    echo "Found existing files"
else
    echo "Downloading new files"
    wget -N -O - https://download1.graphhopper.com/public/photon-db-latest.tar.bz2 | pbzip2 -cd | tar x
fi

ls

if [ -f "photon-0.3.5.jar" ]; then
    echo "Found local photon version"
else
    echo "Downloading photon"
    wget -O photon-0.3.5.jar https://github.com/komoot/photon/releases/download/0.3.5/photon-0.3.5.jar
fi

java -jar photon-0.3.5.jar
