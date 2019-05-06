#!/usr/bin/python3
# -*- coding: utf-8 -*-
# http://google.github.io/styleguide/pyguide.html
"""The simple HTTP server script."""

import json
import re
import urllib.parse
import sys
import threading

sys.path.insert(1, './../lib')
import jobs

from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO

QUEUE = {}


class ApiHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles HTTP GET requests."""
        is_html = self.path == '/'
        content_type = 'text/html' if is_html else 'application/json'

        self.send_response(200)
        self.send_header('Content-type', '%s; charset=utf-8' % content_type)
        self.end_headers()
        output = 'Bad Request'

        if is_html:
            output = open('index.html', 'r').read()
        elif self.path == '/jobs':
            output = json.dumps(list(QUEUE.keys()))
        else:
            match = re.match(r'^/jobs/(\w+)', self.path)
            if match:
                job_id = match.group(1)
                output = json.dumps({'status': _get_job_status(job_id)})

        self.wfile.write(output.encode())

    def do_POST(self):
        """Handles HTTP POST requests."""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        output = 'Bad Request'

        if self.path == '/jobs':
            output = json.dumps({'job_id': _create_jobs(body)})

        self.wfile.write(output.encode())


def _create_jobs(body):
    """Creates new job.

    Args:
        body: The HTTP POST body.

    Returns:
        An identifier of created job.

    See:
        https://docs.python.org/3/library/threading.html#threading.Thread
        https://docs.python.org/3/library/io.html#text-i-o
    """
    if body[:5] == b'file=':  # Strip form field name.
        body = body[5:]

    body = urllib.parse.unquote_plus(body.decode())
    jobs.SESSION['jobs'] = jobs.parse(StringIO(body))
    jobs.SESSION['locker'] = threading.Lock()

    thread = threading.Thread(target=jobs.run)
    thread.start()
    QUEUE[str(thread.ident)] = thread

    return str(thread.ident)


def _get_job_status(job_id):
    """Gets job status by job Id.

    Args:
        job_id: Job Id to get status.

    Returns:
        A job status. 200 - Ok, 404 - Not Found.

    See:
        https://docs.python.org/3/library/threading.html#threading.Thread.join
    """
    thread = QUEUE.get(job_id)
    if thread:
        thread.join()
        return 200
    return 404


if __name__ == '__main__':
    HTTPServer(('', 8000), ApiHTTPRequestHandler).serve_forever()
