FROM python:3.8.5

WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./apache-fake-log-gen.py ./
CMD [ "python", "./apache-fake-log-gen.py","-n 1000", "-s 1" ]