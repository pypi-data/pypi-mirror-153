import pytest
import re

from cli_test_helpers import ArgvContext, EnvironContext

import cogniceptshell.interface

import getpass
import requests
import jwt

def setup_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("TEST_VARIABLE=first_value\nTEST_VARIABLE2=second_value")

def setup_file_for_init(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2")


def check_file_for_value(tmpdir, capsys, expected_value, expected_num_occurences):
    """
    Checks that results were properly written
    """
    with ArgvContext('cognicept', 'config', '--read' ,'--path', str(tmpdir) + "/"):
        capsys.readouterr()
        cogniceptshell.interface.main()
        output = str(capsys.readouterr().out)
        expected_pattern = r"\b{}\b".format(expected_value)
        matches = re.findall(expected_pattern, output, re.MULTILINE)
        assert len(matches) == expected_num_occurences

def test_read_file(tmpdir, monkeypatch, capsys):
    """
    Test changing multiple values of the `runtime.env` file
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'config', '--read' ,'--path', str(tmpdir) + "/"):
        cogniceptshell.interface.main()
        output = str(capsys.readouterr().out)
        matches = re.findall(r"\bfirst_value\b", output, re.MULTILINE)
        assert len(matches) == 1
        matches = re.findall(r"\bsecond_value\b", output, re.MULTILINE)
        assert len(matches) == 1

def test_config_values(tmpdir, monkeypatch, capsys):
    """
    Test changing multiple values of existing variables in config
    """
    setup_file(tmpdir)
    monkeypatch.setattr('builtins.input', lambda prompt: "new_value")

    with ArgvContext('cognicept', 'config', '--path', str(tmpdir) + "/"):
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("General config", pytrace=True)

    check_file_for_value(tmpdir, capsys, "new_value", 2)

def test_change_single_value(tmpdir, monkeypatch, capsys):
    """
    Test changing multiple values of the `runtime.env` file
    """
    setup_file(tmpdir)
    monkeypatch.setattr('builtins.input', lambda prompt: "TEST_VARIABLE2" if prompt == "Config name: " else "new_value")

    with ArgvContext('cognicept', 'config',  '--add' , '--path', str(tmpdir) + "/"):        
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("Config add with existing value", pytrace=True)

    check_file_for_value(tmpdir, capsys, "new_value", 1)

def test_add_new_value(tmpdir, monkeypatch, capsys):
    """
    Test adding new variable into the config
    """
    setup_file(tmpdir)
    monkeypatch.setattr('builtins.input', lambda prompt: "TEST_VARIABLE3" if prompt == "Config name: " else "new_value")

    with ArgvContext('cognicept', 'config',  '--add' , '--path', str(tmpdir) + "/"):        
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("Config add with existing value", pytrace=True)
    
    check_file_for_value(tmpdir, capsys, "first_value", 1)
    check_file_for_value(tmpdir, capsys, "second_value", 1)
    check_file_for_value(tmpdir, capsys, "new_value", 1)
    check_file_for_value(tmpdir, capsys, "TEST_VARIABLE3", 1)

def test_version_command_with_no_runtime_file(tmpdir):
    """
    Test Cognicept Version Command is still function when runtime file is missing
    """
    with ArgvContext('cognicept', 'version', '--path', str(tmpdir) + "/"):
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("Exception thrown when runtime file missing", pytrace=True)

def test_no_runtime_file(tmpdir):
    """
    Test exception is thrown when runtime file is missing
    """

    with ArgvContext('cognicept', 'config', '--path', str(tmpdir) + "/"):
        try:
            cogniceptshell.interface.main()
            pytest.fail("No exception thrown when runtime file missing", pytrace=True)
        except:
            pass

def test_no_command(tmpdir):
    """
    Test an exception thrown when command not passed.
    """
    setup_file(tmpdir)
    with ArgvContext('--path', str(tmpdir) + "/"):
        try:
            cogniceptshell.interface.main()
            pytest.fail("No command did not give an exception", pytrace=True)
        except:
            pass

def test_ssh_disable(tmpdir, monkeypatch, capsys):
    """
    Test disabling ssh
    """
    setup_file(tmpdir)
    monkeypatch.setattr('builtins.input', lambda prompt: "n")

    with ArgvContext('cognicept', 'config',  '--ssh' , '--path', str(tmpdir) + "/"):        
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("Failed to enable ssh.", pytrace=True)
    
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_SSH", 1)
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_SSH_KEY_AUTH", 1)
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_AUTOMATIC_SSH", 1)
    check_file_for_value(tmpdir, capsys, "False", 3)

def test_ssh_enable(tmpdir, monkeypatch, capsys):
    """
    Test enabling ssh
    """
    setup_file(tmpdir)
    monkeypatch.setattr('builtins.input', lambda prompt: "Y" if prompt == "Enable SSH access? (Y/n):" else "" if prompt[:16] == "Name of the user"  else "n")

    with ArgvContext('cognicept', 'config',  '--ssh' , '--path', str(tmpdir) + "/"):        
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("Failed to enable ssh.", pytrace=True)
    
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_SSH", 1)
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_SSH_KEY_AUTH", 1)
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_AUTOMATIC_SSH", 1)
    check_file_for_value(tmpdir, capsys, "True", 1)

def test_ssh_enable_all(tmpdir, monkeypatch, capsys):
    """
    Test enable
    """
    pytest.skip("This test would require root privileges and modify authorized_hosts file each time. Need to figure out how to mock.")

    setup_file(tmpdir)
    monkeypatch.setattr('builtins.input', lambda prompt: "Y")

    with ArgvContext('cognicept', 'config',  '--ssh' , '--path', str(tmpdir) + "/"):        
        try:
            cogniceptshell.interface.main()
        except:
            pytest.fail("Failed to enable ssh.", pytrace=True)
    
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_SSH", 1)
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_SSH_KEY_AUTH", 1)
    check_file_for_value(tmpdir, capsys, "COG_ENABLE_AUTOMATIC_SSH", 1)
    check_file_for_value(tmpdir, capsys, "True", 3)


class CorrectCredentialsWithOTP(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        encoded_jwt = jwt.encode({"user_claims": {"authorized": False}}, "secret", algorithm="HS256")
        return {"access_token": encoded_jwt}

class CorrectCredentialsWithoutOTP(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        encoded_jwt = jwt.encode({"user_claims": {"authorized": True}}, "secret", algorithm="HS256")
        return {"access_token": encoded_jwt}

class WrongCredentials(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {"Message": "Username and password combination not valid"}

class WrongOTPFeedback(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {"Message": "Invalid OTP!"}

class CorrectEnv(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {"ENV1": "VAL1", "ENV2": "VAL2"}

class WrongEnv(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        return None

def mock_credential_endpoint_without2FA(*args, **kwargs):
    if kwargs == {'json': {'username': 'correct_username', 'password': 'correct_password'}}:
        return CorrectCredentialsWithoutOTP()
    else:
        return WrongCredentials()

def mock_credential_endpoint_with2FA(*args, **kwargs):
    if args[0] == 'https://app.cognicept.systems/api/v1/user/login':
        if kwargs['json'] == {'username': 'correct_username', 'password': 'correct_password_otp'} or {'username': 'correct_username', 'password': 'correct_password_wrong_otp'}:
            return CorrectCredentialsWithOTP()
        else:
            return WrongCredentials()
    elif args[0] == 'https://app.cognicept.systems/api/v1/user/mfa/verify':
        if kwargs['json'] == {'otp': 'correct_password_otp'}:
            return CorrectCredentialsWithoutOTP()
        else:
            return WrongOTPFeedback()
    

def mock_spinup_endpoint(*args, **kwargs):
    if args[0] == 'https://app.cognicept.systems/api/v1/spinup/config/correct_org/correct_robot':
        return CorrectEnv()
    else:
        return WrongEnv()

def mock_mfa_endpoint(*args, **kwargs):
    if kwargs == {'json':{'otp':'correct_otp'}}:
        return CorrectCredentialsWithoutOTP()
    else:
        return WrongOTPFeedback()

def test_init_wrong_credentials(tmpdir, monkeypatch, capsys):
    """
    Test initialising with wrong credentials
    """
    setup_file_for_init(tmpdir)

    monkeypatch.setattr('builtins.input', lambda prompt: "wrong_username")
    monkeypatch.setattr('getpass.getpass', lambda prompt: "wrong_password")
    monkeypatch.setattr(requests, 'post', mock_credential_endpoint_without2FA)
    monkeypatch.setattr(requests, 'get', mock_spinup_endpoint)

    with ArgvContext('cognicept', 'init', '--robot_id', '123', '--org_id', 'abc', '--path', str(tmpdir) + "/"):
        cogniceptshell.interface.main()
        captured = capsys.readouterr()
        assert str(captured.out) == 'Failed to initialize the robot: Wrong credentials\n'


def test_init_correct_credentials_wrong_IDs(tmpdir, monkeypatch, capsys):
    """
    Test initialising with wrong credentials but wrong IDs
    """
    setup_file_for_init(tmpdir)

    monkeypatch.setattr('builtins.input', lambda prompt: "correct_username")
    monkeypatch.setattr('getpass.getpass', lambda prompt: "correct_password")
    monkeypatch.setattr(requests, 'post', mock_credential_endpoint_without2FA)
    monkeypatch.setattr(requests, 'get', mock_spinup_endpoint)

    with ArgvContext('cognicept', 'init', '--robot_id', '123', '--org_id', 'abc', '--path', str(tmpdir) + "/"):
        cogniceptshell.interface.main()
        captured = capsys.readouterr()
        assert str(captured.out) == 'Failed to initialize the robot: ID `123` in organization `abc` not found\n'


def test_init_correct_credentials_correct_IDs_without2FA(tmpdir, monkeypatch, capsys):
    """
    Test initialising with correct credentials and correct IDs, without 2FA Verfication activated
    """
    setup_file_for_init(tmpdir)

    monkeypatch.setattr('builtins.input', lambda prompt: "correct_username")
    monkeypatch.setattr('getpass.getpass', lambda prompt: "correct_password")
    monkeypatch.setattr(requests, 'post', mock_credential_endpoint_without2FA)
    monkeypatch.setattr(requests, 'get', mock_spinup_endpoint)

    with ArgvContext('cognicept', 'init', '--robot_id', 'correct_robot', '--org_id', 'correct_org', '--path', str(tmpdir) + "/"):
        cogniceptshell.interface.main()
        captured = capsys.readouterr()
        assert str(captured.out) == 'Successfully initialized configuration for the robot `correct_robot`. To start agents run `cognicept start`\n'
        check_file_for_value(tmpdir, capsys, "ENV1", 1)
        check_file_for_value(tmpdir, capsys, "ENV2", 1)
        check_file_for_value(tmpdir, capsys, "VAL1", 1)
        check_file_for_value(tmpdir, capsys, "VAL2", 1)

def test_init_correct_credentials_correct_IDs_with2FA_correctOTP(tmpdir, monkeypatch, capsys):
    """
    Test initialising with correct credentials and correct IDs with 2FA and correct OTP
    """
    setup_file_for_init(tmpdir)

    monkeypatch.setattr('builtins.input', lambda prompt: "correct_username")
    monkeypatch.setattr('getpass.getpass', lambda prompt: "correct_password_otp")
    monkeypatch.setattr(requests, 'post', mock_credential_endpoint_with2FA)
    monkeypatch.setattr(requests, 'get', mock_spinup_endpoint)

    with ArgvContext('cognicept', 'init', '--robot_id', 'correct_robot', '--org_id', 'correct_org', '--path', str(tmpdir) + "/"):
        cogniceptshell.interface.main()
        captured = capsys.readouterr()
        assert str(captured.out) == 'Successfully initialized configuration for the robot `correct_robot`. To start agents run `cognicept start`\n'
        check_file_for_value(tmpdir, capsys, "ENV1", 1)
        check_file_for_value(tmpdir, capsys, "ENV2", 1)
        check_file_for_value(tmpdir, capsys, "VAL1", 1)
        check_file_for_value(tmpdir, capsys, "VAL2", 1)

def test_init_correct_credentials_correct_IDs_with2FA_wrongOTP(tmpdir, monkeypatch, capsys):
    """
    Test initialising with correct credentials and correct IDs with 2FA and wrong OTP
    """
    setup_file_for_init(tmpdir)

    monkeypatch.setattr('builtins.input', lambda prompt: "correct_username")
    monkeypatch.setattr('getpass.getpass', lambda prompt: "correct_password_wrong_otp")
    monkeypatch.setattr(requests, 'post', mock_credential_endpoint_with2FA)
    monkeypatch.setattr(requests, 'get', mock_spinup_endpoint)

    with ArgvContext('cognicept', 'init', '--robot_id', 'correct_robot', '--org_id', 'correct_org', '--path', str(tmpdir) + "/"):
        cogniceptshell.interface.main()
        output = str(capsys.readouterr().out)
        matches_1 = re.findall('Invalid OTP! Please try again...', output, re.MULTILINE)
        matches_2 = re.findall('Failed to initialized robot: Invalid OTP entered 3 times', output, re.MULTILINE)
        assert len(matches_1) == 3
        assert len(matches_2) == 1