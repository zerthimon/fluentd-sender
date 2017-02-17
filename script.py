#!/usr/bin/env python
#
# docker run -d -e FLUENT_HOST=fluentd --link fluentd:fluentd zerthimon/fluentd-sender

import os
import logging
import time
from fluent import handler


FLUENT_HOST = os.getenv('FLUENT_HOST', 'fluentd-logger')
FLUENT_PORT = int(os.getenv('FLUENT_PORT', 24224))
FLUENT_TAG = os.getenv('FLUENT_TAG', 'docker.docker-tag')

if __name__ == "__main__":
    msgfmt = {
        'host': '%(hostname)s',
        'where': '%(module)s.%(funcName)s',
        'type': '%(levelname)s',
        'stack_trace': '%(exc_text)s',
        '@timestamp': '%(asctime)s.%(msecs)03d'
    }
    datefmt = '%Y-%m-%dT%H:%M:%S'

    logging.basicConfig(level=logging.INFO)
    logging.Formatter.converter = time.gmtime
    l = logging.getLogger('fluent.test')
    h = handler.FluentHandler(FLUENT_TAG, host=FLUENT_HOST, port=FLUENT_PORT)
    formatter = handler.FluentRecordFormatter(msgfmt, datefmt=datefmt)
    h.setFormatter(formatter)
    l.addHandler(h)

    while True:
        l.info({
            'from': 'userA',
            'to': 'userB'
            })
        l.info('{"from": "userC", "to": "userD"}')
        l.info("This log entry will be logged with the additional key: 'message'.")
        time.sleep(10)
