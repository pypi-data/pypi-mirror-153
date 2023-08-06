
import pytest
import requests
import getpass
import datetime

from cogniceptshell.configuration import Configuration
from tests.functional.test_config import check_file_for_value

class SuccessLoginResponse(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return {"AccessKeyId": "CORRECT_ACCESS_KEY", "SecretAccessKey": "CORRECT_SECRET_KEY", "SessionToken": "CORRECT_TOKEN", "Expiration": tomorrow.strftime("%Y-%m-%d %d/%m/ %H:%M:%S+00:00")}


class NotFoundResponse(object):
    def __init__(self):
        self.status_code = 404

class FailedResponse(object):
    def __init__(self):
        self.status_code = 401   

def mock_keyrotate_api(*args, **kwargs):
    if(args[0] == "https://dev.cognicept.systems/api/agent/v1/aws/assume_role"):
        if(kwargs["headers"]["Authorization"] == "Basic CORRECT-KEY" ):
            return SuccessLoginResponse()
        else:
            return FailedResponse()
    else:
        return NotFoundResponse()

def setup_correct_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COGNICEPT_API_URI=https://dev.cognicept.systems/api/agent/v1/\nCOGNICEPT_ACCESS_KEY=CORRECT-KEY")

def setup_wrong_uri_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COGNICEPT_API_URI=https://www.wronguri.com\nCOGNICEPT_ACCESS_KEY=INCORRECT-KEY")

def setup_wrong_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COGNICEPT_API_URI=https://dev.cognicept.systems/api/agent/v1/\nCOGNICEPT_ACCESS_KEY=INCORRECT-KEY")

def test_wrong_uri(tmpdir, capsys, monkeypatch):
    # setup wrong API URI
    setup_wrong_uri_file(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")
    try: 
        args = []
        local_cfg.cognicept_key_rotate(args)
        pytest.fail("Wrong uri did not give an exception", pytrace=True)
    except:
        check_file_for_value(tmpdir, capsys, "AWS_TOKEN_EXPIRATION", 0)
        check_file_for_value(tmpdir, capsys, "CORRECT_SECRET_KEY", 0)
        check_file_for_value(tmpdir, capsys, "CORRECT_TOKEN", 0)
        check_file_for_value(tmpdir, capsys, "CORRECT_ACCESS_KEY", 0)
        pass


def test_wrong_token(tmpdir, capsys, monkeypatch):
    # setup wrong token
    setup_wrong_file(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")
    try: 
        args = []
        result = local_cfg.cognicept_key_rotate(args)        
        assert(result == False)
    except:
        pytest.fail("Wrong token did not fail gracefully", pytrace=True)

def test_correct_login(tmpdir, capsys, monkeypatch):
    # setup API URI
    setup_correct_file(tmpdir)
    
    monkeypatch.setattr(requests, "get", mock_keyrotate_api)
    

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")
    try:
        args = []
        result = local_cfg.cognicept_key_rotate(args)
        assert(result == True)
    except:
        pytest.fail("Correct login gave exception", pytrace=True)

    
    # check if token was stored
    check_file_for_value(tmpdir, capsys, "AWS_TOKEN_EXPIRATION", 1)
    check_file_for_value(tmpdir, capsys, "CORRECT_SECRET_KEY", 1)
    check_file_for_value(tmpdir, capsys, "CORRECT_TOKEN", 1)
    check_file_for_value(tmpdir, capsys, "CORRECT_ACCESS_KEY", 1)
    