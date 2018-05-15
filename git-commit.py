#!/usr/bin/env python3

import git
import re
import datetime
import os
import argparse

from logging import basicConfig
from logging import getLogger
import logging

# arguments perser
parser = argparse.ArgumentParser(description='git commiter')
parser.add_argument('message', metavar='message', type=str,
                    help='commit message')
parser.add_argument('-A', action='store_true',
                    default=False,
                    help='add all. using git add -A.')

args = parser.parse_args()

# logger
basicConfig(level='INFO')
logger = getLogger(__name__)

repo = git.Repo('./')

if args.A:
    repo.git.add(A=True)

head = repo.head.commit

modified_files = head.diff(None)
mod_file_paths = []

if args.A:
    for f in modified_files:
        logger.info('add {}'.format(f.b_blob.name))

logger.info('number of added files : {}'.format(len(modified_files)))


if not modified_files:
    exit()

for mod_file in modified_files:

    # update date tag only markdown.
    if not mod_file.b_blob:
        continue
    if not mod_file.b_blob.name.endswith('md'):
        continue

    mod_file_paths.append(mod_file.b_path)

    with open(mod_file_paths[-1], 'r') as f:
        filedata = f.read()

    if not re.findall('date: ', filedata):
        # make date tag
        for last in re.finditer(r'\n---\n', filedata):
            pass

        filedata = filedata[:last.start()] +\
            '\ndate: {}\n---\n'.format(datetime.date.today()) +\
            filedata[last.end():]

        logger.info('make date tag : {}'.format(mod_file.b_path))
    else:
        # update date tag
        filedata = re.sub(r'date: .*\n',
                          'date: {}\n'.format(datetime.date.today()),
                          filedata, 1)

        logger.info('update date tag : {}'.format(mod_file.b_path))

    with open(mod_file_paths[-1], 'w') as f:
        f.write(filedata)

repo.index.add([p for p in mod_file_paths])

repo.index.commit(args.message)
logger.info('finish commiting!')
