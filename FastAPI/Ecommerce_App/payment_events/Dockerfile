FROM python:3.9.19-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requ.txt

CMD [ "python3","events.py" ]