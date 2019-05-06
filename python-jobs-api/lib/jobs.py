#!/usr/bin/python3
# -*- coding: utf-8 -*-
# http://google.github.io/styleguide/pyguide.html
"""Simple job processing system."""

import os
import subprocess
import sys
import threading

SESSION = {'running': 0, 'threads': 1}


def parse(fo):
    """Parses file-like or file object.

    Also this method is used in API classes as an imported library.

    Args:
        fo: The file-like or file object to parse.

    Returns:
        A dict with jobs found.

    See:
        https://docs.python.org/3/glossary.html#term-file-object
    """
    jobs = {}
    job_id = None

    for line in fo:
        line = line.strip()
        if line[:6] == 'job_id':
            job_id = line[7:]
            jobs[job_id] = {'job_id': job_id, 'complete': False}
        elif line[:7] == 'program':
            jobs[job_id]['program'] = line[8:]
        elif line[:14] == 'parent_job_ids':
            jobs[job_id]['parents'] = line[15:].split(' ')

    return jobs


def run():
    """Runs all jobs.

    Also this method is used in API classes as an imported library.
    """
    SESSION['locker'].acquire()
    jobs = SESSION['jobs']

    for job_id in jobs:
        job = jobs[job_id]
        if not job['complete']:
            parents = job.get('parents') or []
            if not [parent_id for parent_id in parents if \
               not jobs[parent_id]['complete']]:
                thread = threading.Thread(target=_exec, args=(job, ))
                thread.start()
                SESSION['running'] += 1
                if SESSION['running'] >= SESSION['threads']:
                    break

    SESSION['locker'].release()


def _exec(job):
    """Executes job command.

    Args:
        job: The job object with the command to execute.

    See:
        https://docs.python.org/3/library/os.html#os.system
    """
    os.system(job['program'])
    job['complete'] = True
    SESSION['running'] -= 1
    run()


def main():
    filepath = None
    threads = None

    if len(sys.argv) > 1:
        filepath = sys.argv[-1]
        if len(sys.argv) > 3 and sys.argv[1] == '-t' and sys.argv[2].isdigit():
            threads = int(sys.argv[2])

    if filepath and os.path.isfile(filepath):
        # https://docs.python.org/3/library/threading.html#threading.Lock
        SESSION['locker'] = threading.Lock()
        SESSION['threads'] = threads or 1
        with open(filepath, 'r') as fp:
            SESSION['jobs'] = parse(fp)
        run()
    else:
        print('Usage: %s [-t #] file' % __file__)


if __name__ == '__main__':
    main()
