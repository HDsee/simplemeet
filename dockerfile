FROM python:3.8

WORKDIR /simplmeet

ADD . /simplemeet

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3020

CMD [ "python","./app.py"]
