FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV env_port = 80 env_dbserver = "" env_dbname = ""  env_dbuser = ""  env_dbpassword = ""
ENTRYPOINT [ "python", "api.py"]