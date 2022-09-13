# Currently not working :sadge:

FROM python:3.10.4-buster
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "flask --app APP --debug run","--host=0.0.0.0"]
