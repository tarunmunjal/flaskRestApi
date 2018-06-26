How to use the docker image
You can build a docker image using the following command:
cd to the folder where Dockerfile and api.py files are
docker build -t <NameTheImage> .

Once the docker image is built you can spin up containers using the following command
sudo docker run -d -p 80:5000 -e env_dbname=changeme -e env_dbserver=192.168.122.1 -e env_dbuser=changeme -e env_dbpassword=changeme -e env_port=5000 <Name Of the Image you choose in the build command>