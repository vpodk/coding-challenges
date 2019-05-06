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
from io import BytesIO, StringIO

QUEUE = {}


class ApiHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
                print('job_id: %s' % job_id)
                output = json.dumps({'status': _get_job(job_id)})

        self.wfile.write(output.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        output = 'Bad Request'

        if self.path == '/jobs':
            output = json.dumps({'job_id': _create_jobs(body)})

        self.wfile.write(output.encode())


def _create_jobs(body):
    response = BytesIO()
    response.write(body)
    output = response.getvalue()

    if output[:5] == b'file=':  # Strip form field name.
        output = output[5:]

    output = urllib.parse.unquote_plus(output.decode())
    jobs.SESSION['jobs'] = jobs.parse(StringIO(output))
    jobs.SESSION['locker'] = threading.Lock()

    thread = threading.Thread(target=jobs.run)
    thread.start()
    QUEUE[str(thread.ident)] = thread

    return str(thread.ident)


def _get_job(job_id):
    thread = QUEUE.get(job_id)
    if thread:
        thread.join()
        return '200'
    return '404'


def main(server_class=HTTPServer, handler_class=ApiHTTPRequestHandler):
    server_class(('', 8000), handler_class).serve_forever()


if __name__ == "__main__":
    main()
