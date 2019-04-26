import os
import flask
from unittest import mock


@mock.patch.dict(os.environ, {'RATE_LIMITING_THRESHOLD': '3'})
@mock.patch.dict(os.environ, {'BLOCKED_IP_TIMEOUT': '3'})
def test_authorize_success():
    # print os.environ
    from ..views.gateway import authorize_request
    req = mock.patch.object(flask, "request")
    environ = {'REMOTE_ADDR': '12.12.12.12'}
    req.__setattr__('environ', environ)
    storage = fakeStorage
    authorize_request(req, storage)
    authorize_request(req, storage)
    assert authorize_request(req, storage)


@mock.patch.dict(os.environ, {'RATE_LIMITING_THRESHOLD': '2'})
@mock.patch.dict(os.environ, {'BLOCKED_IP_TIMEOUT': '3'})
def test_authorize_failure():
    # print os.environ
    from ..views.gateway import authorize_request
    req = mock.patch.object(flask, "request")
    environ = {'REMOTE_ADDR': '12.12.12.12'}
    req.__setattr__('environ', environ)
    storage = fakeStorage
    authorize_request(req, storage)
    authorize_request(req, storage)
    authorize_request(req, storage)
    authorize_request(req, storage)
    assert not authorize_request(req, storage)


class fakeStorage():
    memory = []
    def get(self, key):
        """ Get data using key """
        try:
            for i, row in enumerate(self.memory):
                if key == row[0]:
                    return [row[0], row[1], row[2]]
        except Exception as error:
            print(error)

        return ['new', None, 'mwmee']

    def set(self, key, data):
        """ Set Data  """
        try:
            print(data['counter'])
            for i, row in enumerate(self.memory):
                if key == row[0]:
                    self.memory.remove(row)

            self.memory.append([data['ip'], data['counter'], data['last_transaction']])
        except Exception as error:
            print(error)

    def exists(self, key):
        """ Exists  """
        exist = False
        try:
            super
        except Exception as error:
            print(error)
        return exist

