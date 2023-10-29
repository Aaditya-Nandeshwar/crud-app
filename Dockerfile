FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ../curd-app-backup .

EXPOSE 80

CMD [ "python3", "app.py"]
