FROM python:3.10.4-buster
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN ls
RUN pip3 install -r requirements.txt
CMD [ "python3", "APP/app.py"]
