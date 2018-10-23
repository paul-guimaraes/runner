#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
from concurrent.futures import ThreadPoolExecutor

programName = 'Runner 1.0'

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--command', help='Command to execute.', required=True)
parser.add_argument('-n', '--numberThreads', help='Number threads to execute', type=int, required=True)

try:
    args = parser.parse_args()
except:
    print(programName, flush=True)
    exit(0)

def run(command):
    print('Running %s...' % command, flush=True)
    os.system(command)
    print('%s finished.' % command, flush=True)

commands = open(args.command, 'r')
with ThreadPoolExecutor(max_workers=args.numberThreads) as executor:
    for command in commands:
        command = command.rstrip()
        future = executor.submit(run, (command))
commands.close()
