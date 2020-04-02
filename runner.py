#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import getpass
import os
import pexpect
from concurrent.futures import ThreadPoolExecutor


class Runner:
    def __init__(self, number_threads, output_directory, password):
        self.number_threads = number_threads
        self.output_directory = output_directory
        self.password = password
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        self.log_execution = open(os.path.join(self.output_directory, 'execution.log'), 'w')

    def __del__(self):
        self.log_execution.close()

    def log(self, message):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%Sh")
        print('{}: {}'.format(now, message), flush=True)
        self.log_execution.write('{}: {}\n'.format(now, message))
        self.log_execution.flush()

    def run(self, _command, _command_number, password=None):
        self.log('Executando %s...' % _command)
        process = pexpect.spawn('/bin/bash -c "{}"'.format(_command.replace('"', "'")), encoding='utf8')
        if password is not None:
            process.expect(['[pP]assword', '[sS]enha'])
            process.sendline(password)

        output_file = open(os.path.join(self.output_directory, 'command_{}.log'.format(_command_number)), 'w')
        output_file.write('{}\n\n'.format(_command))

        result = process.readlines()

        process.close()

        if (
                (process.exitstatus is not None and process.exitstatus != 0)
                or
                (process.signalstatus is not None and process.signalstatus != 0)
        ):
            output_file.write('Comando finalizado com erros.\n\n')
            self.log('Commando %s executado com erro.' % _command)
            exit()
        else:
            self.log('Commando %s executado.' % _command)

        for line in result:
            output_file.write(line)

        output_file.close()

    def start(self):
        password = getpass.getpass("Entre com sua senha por favor:") if self.password else None
        commands = open(args.command, 'r')
        with ThreadPoolExecutor(max_workers=self.number_threads) as executor:
            for i, command in enumerate(commands):
                command = command.strip()
                if not command.startswith('#'):
                    future = executor.submit(self.run, command, i+1, password)
        commands.close()


parser = argparse.ArgumentParser('Runner 1.01')
parser.add_argument('-c', '--command', help='File with command list to execute. One command per line', required=True)
parser.add_argument('-n', '--numberThreads', help='Number threads to execute commands', type=int, default=1)
parser.add_argument('-o', '--output', help='Output result directory', default='.')
parser.add_argument('-p', '--password', help='Fill passwords if requested by commands in execution', action='store_true')

args = parser.parse_args()
runner = Runner(args.numberThreads, args.output, args.password)
runner.start()
