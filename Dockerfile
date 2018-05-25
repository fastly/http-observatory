FROM python:3-alpine

WORKDIR /app
COPY . .

RUN apk update && \
	apk add postgresql-libs && \
	apk add --no-cache --virtual .build-deps\
		gcc \
		libc-dev \
		linux-headers \
		postgresql-dev \
		&& \
	pip install --upgrade -r requirements.txt && \
	apk del .build-deps



ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
#ENV FLASK_APP /app/api.py
#ENTRYPOINT ["/usr/local/bin/flask"]
#CMD ["run"]
ENTRYPOINT ["/app/api.py"]
