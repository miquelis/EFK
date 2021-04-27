FROM python:2.7

WORKDIR /usr/src/app
COPY ./files/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./files/fakelog.py ./
CMD [ "python", "./fakelog.py","-n 1000", "-s 1" ]