
import pytest
import re
import requests
import datetime
import os
import boto3, botocore
from mock import patch

from cogniceptshell.configuration import Configuration
from cogniceptshell.agent_life_cycle import AgentLifeCycle

from tests.unit.mock_docker_client import MockDockerClient


class SuccessEcrCredentials(object):
    def __init__(self):
        self.status_code = 200
    def json(self):
        return {"AccessKeyId": os.getenv('AWS_ACCESS_KEY_ID',""), "SecretAccessKey": os.getenv('AWS_SECRET_ACCESS_KEY', ""), "SessionToken": "" }

class NotFoundLoginResponse(object):
    def __init__(self):
        self.status_code = 404


class SuccessAwsCredentials(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {"AccessKeyId": os.getenv('AWS_ACCESS_KEY_ID', ""), "SecretAccessKey": os.getenv('AWS_SECRET_ACCESS_KEY', ""), "SessionToken": ""}


class NotFoundMockResponse(object):
    def __init__(self):
        self.status_code = 404


def mock_aws_endpoint(*args, **kwargs):
    if(args[0] == "https://test.cognicept.systems/api/agent/v1/aws/assume_role"):
        return SuccessAwsCredentials()
    else:
        return NotFoundMockResponse()

def mock_ecr_endpoint(*args, **kwargs):
    if(args[0] == "https://test.cognicept.systems/api/v1/aws/assume_role/ecr"):
        return SuccessEcrCredentials()
    else:
        return NotFoundMockResponse()

def setup_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2")

def setup_with_orbitty(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2\nCOG_ORBITTY_ENABLED=True\nCOG_ORBITTY_IMAGE=412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/orbitty:latest")

def setup_wrong_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1")

def setup_test_docker_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("AWS_ACCESS_KEY_ID=TESTKEY\nAWS_SECRET_ACCESS_KEY=TESTKEY\nAWS_SESSION_TOKEN=TESTTOKEN\nCOG_AGENT_CONTAINERS=test\nCOG_AGENT_IMAGES=ubuntu:latest\nCOGNICEPT_API_URI=https://test.cognicept.systems/api/agent/v1/\nCOGNICEPT_ACCESS_KEY=CORRECT-KEY")

def setup_wrong_api(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=test\nCOG_AGENT_IMAGES=ubuntu:latest\nCOGNICEPT_API_URI=https://wrongaddress.com/")


def setup_logs(tmpdir):

    expected_location = ".cognicept/agent/logs/directory"
    logs_dir = tmpdir.mkdir("agent").mkdir("logs")
    p = logs_dir.join("latest_log_loc.txt")
    p.write(expected_location + "\n")
    latest_log_dir = logs_dir.mkdir("directory")
    p2 = latest_log_dir.join("logDataStatus.json")
    p2.write('{"agent_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","compounding":"Null","create_ticket":true,"description":"Null","event_id":"Null","level":"Heartbeat","message":"Offline","module":"Status","property_id":"64dd2881-7010-4d9b-803e-42ea9439bf17","resolution":"Null","robot_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","source":"Null","telemetry":{},"timestamp":"2020-06-26T09:33:47.995496"}')

    p3 = latest_log_dir.join("logData1.json")
    p3.write('{"agent_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","compounding":false,"create_ticket":false,"description":"Null","event_id":"2a9e5abc-0412-4840-badc-d83094ddc0c6","level":"2","message":"Setting pose (10.986000): 9.700 9.600 -0.000","module":"Localization","property_id":"64dd2881-7010-4d9b-803e-42ea9439bf17","resolution":"Null","robot_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","source":"amcl","telemetry":{"nav_pose":{"orientation":{"w":0.99999148220339307,"x":0,"y":0,"z":-0.0041274108907466923},"position":{"x":0.02080195682017939,"y":0.024943113508386214,"z":0}},"odom_pose":{"orientation":{"w":0.99999999991375599,"x":0,"y":0,"z":-1.3133466028590658e-05},"position":{"x":7.9073011611115254e-06,"y":-1.4214209401935302e-10,"z":0}}},"timestamp":"2020-06-26T07:37:25.506519"}')


def mock_good_ecr_pull(self, operation_name, kwarg):
    """
    Utility mock AWS SDK for a good ECR pull function
    """
    # Used to check is ECR -- was called, fail wantedly for test framework to catch
    if (operation_name == 'GetAuthorizationToken'):
        raise boto3.exceptions.Boto3Error
    else:
        raise SystemExit


def mock_bad_ecr_pull(self, operation_name, kwarg):
    """
    Utility mock AWS SDK for a bad ECR pull function
    """
    # Used to check is ECR -- was called, fail wantedly with ClientError to handle
    if (operation_name == 'GetAuthorizationToken'):
        # Raising exception to simulate bad credentials
        resp = {
            'Error': {
                'Code': 'SomeServiceException',
                'Message': 'Details/context around the exception or error'
            },
            'ResponseMetadata': {
                'RequestId': '1234567890ABCDEF',
                'HostId': 'host ID data will appear here as a hash',
                'HTTPStatusCode': 400,
                'HTTPHeaders': {'header metadata key/values will appear here'},
                'RetryAttempts': 0
            }
        }

        raise(botocore.exceptions.ClientError(resp, operation_name))
    else:
        raise SystemExit


def test_init(tmpdir):
    # setup container/image config
    setup_file(tmpdir)


    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    assert(len(agent_lifecycle._docker_container_names) == 2)
    assert(len(agent_lifecycle._docker_images) == 2)
    assert(agent_lifecycle._docker_images[agent_lifecycle._docker_container_names[0]] == "image1")
    assert(agent_lifecycle._docker_images[agent_lifecycle._docker_container_names[1]] == "image2")

def test_orbitty_init(tmpdir):
    # setup container/image config
    setup_with_orbitty(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    assert(len(agent_lifecycle._docker_container_names) == 2)
    assert(len(agent_lifecycle._docker_images) == 3)


def test_incorrect_init(tmpdir):

    # setup container/image config
    setup_wrong_file(tmpdir)


    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    assert(len(agent_lifecycle._docker_container_names) == 5)
    assert(len(agent_lifecycle._docker_images) == 7)

def test_latest_log_loc(tmpdir):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_logs(tmpdir)

    agent_lifecycle = AgentLifeCycle()
    returned_location = agent_lifecycle._get_latest_log_loc(args)

    assert(returned_location == "agent/logs/directory")

def test_get_last_event(tmpdir, capsys):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_logs(tmpdir)

    agent_lifecycle = AgentLifeCycle()

    capsys.readouterr().out
    agent_lifecycle.get_last_event(args)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"\b2020-06-26T07:37:25.506519\b", output, re.MULTILINE)
    # check if file was found and printed 
    assert len(matches) == 1

def test_parsing_ok_kriya_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: ERROR
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: ERROR
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: ERROR
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK"""
    capsys.readouterr().out
    agent_lifecycle._parse_remote_intervention_agent_logs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ONLINE", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_not_init_kriya_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.169204677]: WEBSOCKET:: STATUS:: INIT"""
    capsys.readouterr().out
    agent_lifecycle._parse_remote_intervention_agent_logs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"NOT INITIALIZED", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_agent_error_kriya_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: ERROR"""
    capsys.readouterr().out
    agent_lifecycle._parse_remote_intervention_agent_logs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ERROR", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_websocket_error_kriya_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: ERROR
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK"""
    capsys.readouterr().out
    agent_lifecycle._parse_remote_intervention_agent_logs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ERROR", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_webrtc_error_kriya_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: ERROR
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK"""
    capsys.readouterr().out
    agent_lifecycle._parse_remote_intervention_agent_logs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ERROR", output, re.MULTILINE)
    assert len(matches) == 1

def test_run(tmpdir, capsys):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_test_docker_file(tmpdir)
    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    args.config = local_cfg
    args.agents = True

    # run container
    mock_docker_client = MockDockerClient()
    with patch("docker.from_env", new=lambda: mock_docker_client):
        result = agent_lifecycle.start(args)
        assert result == True

        # check status
        output = capsys.readouterr().out
        print(output)
        agent_lifecycle.get_status(args)
        output = str(capsys.readouterr().out)

        print(output)
        matches1 = re.findall(r"ONLINE", output, re.MULTILINE)
        assert len(matches1) == 1

        result = agent_lifecycle.remove_agents(args)
        assert result == True

        # check if offline
        capsys.readouterr().out
        agent_lifecycle.get_status(args)
        output = str(capsys.readouterr().out)
        matches2 = re.findall(r"CONTAINER NOT FOUND", output, re.MULTILINE)
        assert len(matches2) == 1


def test_agent_restart(tmpdir, capsys):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_test_docker_file(tmpdir)
    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    args.config = local_cfg    
    args.agents = True

    mock_docker_client = MockDockerClient()
    with patch("docker.from_env", new=lambda: mock_docker_client):
        # run container
        args.list = ["test"]
        args.detach = False
        result = agent_lifecycle.restart(args)
        assert result == True
        
        args.list = ["test"]

        # run container
        args.list = ["unknown_container"]
        result = agent_lifecycle.restart(args)
        assert result == False

        # run container
        args.list = ["test","unknown_container"]
        result = agent_lifecycle.restart(args)
        assert result == False

        args.list = ["test"]
        result = agent_lifecycle.remove_agents(args)
        assert result == True

        result = agent_lifecycle.start(args)
        assert result == True

        del args.list
        result = agent_lifecycle.remove_agents(args)
        assert result == True


def test_correct_ecr_credentials(tmpdir, capsys, monkeypatch):

    # setup runtime variables
    setup_test_docker_file(tmpdir)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_good_ecr_pull):
        local_cfg = Configuration()
        local_cfg.load_config(str(tmpdir) + "/")

        args = type('', (), {})()
        args.path = str(tmpdir) + "/"
        args.reset = False
        args.config = local_cfg
        args.detach = False

        agent_lifecycle = AgentLifeCycle()
        agent_lifecycle.configure_containers(local_cfg)
        try:
            monkeypatch.setattr(requests, "get", mock_aws_endpoint)
            result = agent_lifecycle.update(args)            
        except boto3.exceptions.Boto3Error:
            result = True
        except Exception:
            result = False

    assert(result == True)


def test_wrong_ecr_credentials(tmpdir):

    # setup runtime variables
    setup_test_docker_file(tmpdir)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_bad_ecr_pull):
        local_cfg = Configuration()
        local_cfg.load_config(str(tmpdir) + "/")

        args = type('', (), {})()
        args.path = str(tmpdir) + "/"
        args.reset = False
        args.config = local_cfg
        args.detach = False

        agent_lifecycle = AgentLifeCycle()
        agent_lifecycle.configure_containers(local_cfg)
        try:
            result = agent_lifecycle.update(args)       
        except Exception:
            print('Update failed')
            result = True

    assert(result == False)

def test_display_version(tmpdir, capsys):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_file(tmpdir)
    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    capsys.readouterr().out
    agent_lifecycle.display_version(args)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"Cognicept Shell Version", output, re.MULTILINE)
    container_matches = re.findall(r"unknown/latest", output, re.MULTILINE)
    # check if Cognicept Version is printed out
    assert len(matches) == 1
    assert len(container_matches) == 2