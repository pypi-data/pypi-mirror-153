import os
from .constants import API_ENDPOINT


class Configuration:
    def __init__(self):
        self.reload()

    def reload(self):
        # authentication process
        self._token = os.getenv('NG_API_AUTHTOKEN')
        self._login = os.getenv('LOGIN')
        self._password = os.getenv('PASSWORD')
        # system env variables
        self._job_id = os.environ.get('JOBID')
        self._pipeline_id = os.environ.get('PIPELINE_ID')
        self._eid = os.environ.get('EID')
        self._endpoint = os.environ.get('NG_API_ENDPOINT', API_ENDPOINT)
        self._component_name = os.environ.get('NG_COMPONENT_NAME')
        self._group_name = os.environ.get('NG_STATUS_GROUP_NAME', '')

        # Authentication from Token or login/password
        if self._token is None or self._token == '':
            if self._login is None or self._login == '':
                raise Exception("No LOGIN found. Set the environment variable with the LOGIN")
            if self._password is None or self._password == '':
                raise Exception("No PASSWORD found. Set the environment variable with the PASSWORD")

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def job_id(self):
        return self._job_id

    @property
    def eid(self):
        return self._eid

    @property
    def component_name(self):
        return self._component_name

    @property
    def group_name(self):
        return self._group_name

    @property
    def pipeline_id(self):
        return self._pipeline_id

    @property
    def token(self):
        return self._token

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password
