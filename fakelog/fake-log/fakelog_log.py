#!/usr/bin/env python3
from faker import Faker
import argparse
import random
import datetime
import json
import time
import sys


faker = Faker()

parser = argparse.ArgumentParser()

parser.add_argument(
    "--number-rows",
    "-n",
    type=int,
    dest='number_rows',
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
    "--sleep",
    "-s",
    help="Sleep this long between lines (in seconds)",
    default=0.0,
    type=float
)

args = parser.parse_args()


output_type = args.output_type
file_prefix = args.file_prefix
log_lines = args.number_rows


def output_file(output_type):

    timestr = time.strftime("%Y%m%d-%H%M%S")

    outFileName = 'access_log_'+timestr + \
        '.log' if not file_prefix else file_prefix+'_access_log_'+timestr+'.log'

    if output_type == 'log':
        return open(outFileName, 'w')

    if output_type == 'console':
        return sys.stdout


f = output_file(output_type)

for i in range(log_lines):
    file = json.dumps({
        "log": faker.text(),
        "stream": random.choice(("stdout", "stderr")),
        "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "_tags": "faker_log"
    })

    f.write('%s\n' % (file))
    f.flush()

    if args.sleep:
        time.sleep(args.sleep)
