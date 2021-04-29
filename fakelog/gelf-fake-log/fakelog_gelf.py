from faker import Faker
from random import randint
import json
import argparse
import time
import gzip
import sys
import os
import random

parser = argparse.ArgumentParser()
faker = Faker()

parser.add_argument(
    "--number-rows",
    "-n",
    type=int,
    dest='number_rows',
    help="Number log entries to generate",
    default=1
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

parser.add_argument(
    "--files",
    "-f",
    dest='number_files',
    help="Amount of files that will be generated",
    default=1,
    type=int
)


args = parser.parse_args()

output_type = args.output_type
log_lines = args.number_rows
file_prefix = args.file_prefix
directory = args.directory
sleep = args.sleep


def create_file_name():
    timestr = time.strftime("%Y%m%d-%H%M%S")

    outFileName = 'access_log_'+timestr + \
        '.log' if not file_prefix else file_prefix+'_access_log_'+timestr+'.log'

    if not directory:
        outFileName = outFileName
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)

        outFileName = os.path.join(directory, outFileName)

    return outFileName


def output_file():
    outFileName = create_file_name()

    if output_type == 'log':
        return open(outFileName, 'w')

    if output_type == 'gzip':
        return gzip.open(outFileName+'.gz', 'wb')

    if output_type == 'console':
        return sys.stdout


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def faker_gelf_generator():
    return {
        "version":  float(random.randrange(100, 500))/100,
        "host": faker.safe_domain_name(),
        "short_message": faker.text(),
        "timestamp": time.time(),
        "level": random.randrange(1, 9),
        "_user_id": random_with_N_digits(5),
        "_tags": "faker_log_gelf"
    }


def create_gelf():
    f = output_file()

    for _ in range(log_lines):

        file = json.dumps(faker_gelf_generator())

        if output_type == 'gzip':
            f.write((file.encode('utf-8')))
        else:
            f.write('%s\n' % (file))
            f.flush()

        if sleep:
            time.sleep(sleep)


for i in range(args.number_files):

    print('%d %s' % (i+1, "file(s) generated"))

    create_gelf()
    if sleep:
        time.sleep(sleep)
