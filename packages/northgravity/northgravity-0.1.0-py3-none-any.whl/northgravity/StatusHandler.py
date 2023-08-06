from . import LOGGER_NAME, config
from .HTTPCalller import HTTPCaller
import time
import logging

log = logging.getLogger(LOGGER_NAME)

class StatusHandler:
    '''
    Allows to send statuses to the Status Page of the NorthGravity Application.
    Each status type has a color and a corresponding message.
    - INFO: Blue
    - ERROR: Red
    - WARNING: Orange
    '''

    def __init__(self):
        self.caller = HTTPCaller()
        self.eid = config.eid
        self.job_id = config.job_id
        self.component_name = config.component_name
        self.group_name = config.group_name

    def send_status(self, status, message):
        # Set the api call for the status connected to the new log event
        log.debug(f'Send status with status {status} and message {message}')

        payload = {'jobId': self.job_id,
                   'eId': self.eid,
                   'status': status,
                   'message': message,
                   'className': 'python',
                   'groupName': self.group_name,
                   'componentName': self.component_name,
                   'time': time.strftime('%Y-%m-%dT%H:%M:%S'),
                   }

        r = self.caller.post(path="/status", payload=payload, headers={'X-KH-E-ID': self.eid})

        log.debug(f'URL: {r.url} \nHeaders: {r.request.headers} \nPayload: {payload}')

        if r.status_code > 201:
            log.info("Sending status response was: " + str(r.status_code) + " and text " + str(r.text))

        return

    def info(self, message):
        self.send_status('INFO', message)

    def error(self, message):
        self.send_status('ERROR', message)

    def warn(self, message):
        self.send_status('WARN', message)
