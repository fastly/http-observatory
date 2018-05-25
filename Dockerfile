FROM debian:stretch

RUN apt-get update && apt-get -y install python3-pip

WORKDIR /app
COPY . .

RUN pip3 install --upgrade -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
#ENV FLASK_APP /app/api.py
#ENTRYPOINT ["/usr/local/bin/flask"]
#CMD ["run"]
ENTRYPOINT ["/app/api.py"]
