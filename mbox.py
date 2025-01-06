#!/usr/bin/env python3

import locale
import os
import subprocess
import sys


def linecount(filename):
    return int(subprocess.Popen(['wc', '-l', filename], stdout=subprocess.PIPE).communicate()[0].split()[0])


def progress_bar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_length = int(round(bar_length* count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_length + '-' * (bar_length - filled_up_length)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()


class MboxReader:
    def __init__(self, filename):
        self.line_count = linecount(filename)
        self.handle = open(filename, 'rb')
        assert self.handle.readline().startswith(b'From ')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.handle.close()

    def __iter__(self):
        return iter(self.__next__())

    def __next__(self):
        lines_read = 0
        in_header = False
        flags = 'skip-first'
        while True:
            line = self.handle.readline()
            lines_read += 1
            if line == b'' or (line.startswith(b'From ') and not line.startswith(b'From MAILER_DAEMON')):
                progress_bar(lines_read, self.line_count)
                if flags != 'skip-first':
                    yield flags
                if line == b'':
                    break
                in_header = True
                flags = ''
                continue
            if in_header and line == b'\n':
                in_header = False
            if in_header and (line.startswith(b'Status: ') or line.startswith(b'X-Status: ')):
                status_line = str(line.decode('utf-8')).split()
                if len(status_line) == 2:
                    flags += status_line[1]


try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    arg_index = 1
    while arg_index < len(sys.argv):
        arg = sys.argv[arg_index]
        file_size = os.stat(arg).st_size
        with MboxReader(arg) as mbox:
            num_messages = 0
            num_read = 0
            num_non_recent = 0
            num_answered = 0
            num_flagged = 0
            num_draft = 0
            num_deleted = 0
            for message in mbox:
                for flag in message:
                    if flag == 'R':
                        num_read += 1
                    elif flag == 'O':
                        num_non_recent += 1
                    elif flag == 'A':
                        num_answered += 1
                    elif flag == 'F':
                        num_flagged += 1
                    elif flag == 'T':
                        num_draft += 1
                    elif flag == 'D':
                        num_deleted += 1
                num_messages += 1
            print(f"\033[K{arg}: size={file_size:n}, count={num_messages:n}, downloaded={num_non_recent:n}, unread={num_messages - num_read:n}, deleted={num_deleted:n}")
        arg_index += 1
except KeyboardInterrupt:
    print()
    exit(1)