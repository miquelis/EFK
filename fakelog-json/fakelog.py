from faker import Faker
import json
import argparse
import datetime
import time
import gzip
import sys
import os

parser = argparse.ArgumentParser()
faker = Faker()

parser.add_argument(
    "--number-rows",
    "-n",
    type=int,
    dest='num_lines',
    help="Number log entries to generate",
    default=100
)

parser.add_argument(
    "--output",
    "-o",
    dest='output_type',
    help="Write to a Log file, a gzip file or to STDOUT",
    choices=['log', 'gzip', 'console'],
    default="console"
)

parser.add_argument(
    "--prefix",
    "-p",
    dest='file_prefix',
    help="Prefix the output file name",
    type=str
)

parser.add_argument(
    "--dir",
    "-d",
    dest='directory',
    help="Directory to save the file",
    type=str
)

parser.add_argument(
    "--sleep",
    "-s",
    help="Sleep this long between lines (in seconds)",
    default=0.0,
    type=float
)


args = parser.parse_args()

output_type = args.output_type
log_lines = args.num_lines
file_prefix = args.file_prefix
directory = args.directory


timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()

outFileName = 'access_log_'+timestr + \
    '.log' if not file_prefix else file_prefix+'_access_log_'+timestr+'.log'

outFileName = outFileName if not directory else os.path.join(
    directory, outFileName)


def output_file(output_type):
    if output_type == 'log':
        return open(outFileName, 'w')

    if output_type == 'gzip':
        return gzip.open(outFileName+'.gz', 'wb')

    if output_type == 'console':
        return sys.stdout


def faker_person_generator(faker):
    return {'last_name': faker.last_name(),
            'first_name': faker.first_name(),
            'street_address': faker.street_address(),
            'email': faker.email(),
            'ip': faker.ipv4(),
            'time': otime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}


f = output_file(output_type)

for x in range(log_lines):

    file = json.dumps(faker_person_generator(faker))

    if output_type == 'gzip':
        f.write((file.encode('utf-8')))
    else:
        f.write('%s\n' % (file))
        f.flush()

    if args.sleep:
        time.sleep(args.sleep)
