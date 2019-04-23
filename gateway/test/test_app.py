import os
from unittest import mock

@mock.patch.dict(os.environ, {'RATE_LIMITING_THRESHOLD': '3'})
@mock.patch.dict(os.environ, {'BLOCKED_IP_TIMEOUT': '3'})
def test_authorize():
    # print os.environ
    from ..views.gateway import authorize_request
    fake_Request = {
        'REMOTE_ADDR': '12.12.12.3'
    }
    assert authorize_request(fake_Request)