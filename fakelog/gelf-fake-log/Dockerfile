FROM python:3.8.5

WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./fakelog_gelf.py ./
CMD [ "python", "./fakelog_gelf.py","-n 10", "-s 1", "-o gzip", "-f 20", "-d logs" ]