import os
import time
import pytest
import re
import datetime
import requests
import docker
import botocore
import boto3
from mock import patch

from cli_test_helpers import ArgvContext, EnvironContext

import cogniceptshell.interface


class SuccessResponse(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return {"AccessKeyId": "CORRECT_ACCESS_KEY", "SecretAccessKey": "CORRECT_SECRET_KEY", "SessionToken": "CORRECT_TOKEN", "Expiration": tomorrow.strftime("%Y-%m-%d %d/%m/ %H:%M:%S+00:00")}


class NotFoundResponse(object):
    def __init__(self):
        self.status_code = 404

    def json(self):
        return {"Message": "Not Found"}


class FailedResponse(object):
    def __init__(self):
        self.status_code = 401

    def json(self):
        return {"Message": "Failed"}


def mock_keyrotate_api(*args, **kwargs):
    if((args[0] == "https://test.cognicept.systems/api/agent/v1/aws/assume_role") or
        (args[0] == "https://bad.cognicept.systems/api/agent/v1/aws/assume_role")):
        if(kwargs["headers"]["Authorization"] == "Basic CORRECT-KEY"):
            return SuccessResponse()
        else:
            return FailedResponse()
    else:
        return NotFoundResponse()


def setup_file(tmpdir):
    """
    Utility function to setup a fake runtime.env to run tests
    """
    p = tmpdir.join("runtime.env")
    p.write("AWS_ACCESS_KEY_ID=TESTKEY\nAWS_SECRET_ACCESS_KEY=TESTKEY\nAWS_SESSION_TOKEN=TESTTOKEN\nROBOT_CODE=TESTBOT\nCOG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2\nCOGNICEPT_API_URI=https://test.cognicept.systems/api/agent/v1/\nCOGNICEPT_ACCESS_KEY=CORRECT-KEY")


def setup_wrong_api(tmpdir):
    """
    Utility function to setup a fake runtime.env to run tests
    """
    p = tmpdir.join("runtime.env")
    p.write("AWS_ACCESS_KEY_ID=TESTKEY\nAWS_SECRET_ACCESS_KEY=TESTKEY\nAWS_SESSION_TOKEN=TESTTOKEN\nROBOT_CODE=TESTBOT\nCOG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2\nCOGNICEPT_API_URI=https://bad.cognicept.systems/api/agent/v1/\nCOGNICEPT_ACCESS_KEY=CORRECT-KEY")


def setup_bad_file(tmpdir):
    """
    Utility function to setup a fake runtime.env to run tests
    """
    p = tmpdir.join("runtime.env")
    p.write("AWS_ACCESS_KEY_ID=TESTKEY\nAWS_SECRET_ACCESS_KEY=TESTKEY\nAWS_SESSION_TOKEN=TESTTOKEN\nROBOT_CODE=TESTBOT\nCOG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2\nCOGNICEPT_API_URI=https://test.cognicept.systems/api/agent/v1/")


def setup_mock_bags(tmpdir):
    """
    Utility function to setup mock bag files to run tests
    """
    bags_dir = tmpdir.mkdir("bags")
    p = bags_dir.join("bag1.bag")
    p.write("TESTDATA")
    time.sleep(0.5)
    p = bags_dir.join("bag2.bag")
    p.write("TESTDATA")
    time.sleep(0.5)
    p = bags_dir.join("bag3.bag")
    p.write("TESTDATA")


def mock_upload_s3(self, operation_name, kwarg):
    """
    Utility mock AWS SDK for S3 upload function
    """
    # Used to check is S3 PutObject was called
    print(operation_name)


def mock_bad_cred_upload_s3(self, operation_name, kwarg):
    """
    Utility mock AWS SDK for S3 upload function
    """
    # Used to check is S3 PutObject was called
    raise(boto3.exceptions.S3UploadFailedError)


def mock_bagfile_api(*args, **kwargs):
    '''
    Utility mock bagfile Cognicept REST API for correct handling
    '''
    if(args[0] == "https://test.cognicept.systems/api/agent/v1/bagfile"):
        if(kwargs["json"]["robot_id"] == "TESTBOT" and
                kwargs["json"]["bagfile_name"] == "bag3.bag" and
                kwargs["json"]["bagfile_url"] == "bag3.bag"):
            return SuccessResponse()
        else:
            return NotFoundResponse()
    else:
        return FailedResponse()


def check_value(expected_pattern, output, expected_num_occurences):
    """
    Utility function to assert if an expected pattern is in an output 
    for specified # of occurrences
    """
    matches = re.findall(expected_pattern, output, re.MULTILINE)
    assert len(matches) == expected_num_occurences


def test_no_push_command(tmpdir, capsys):
    """
    Test if mandatory command missing is caught correctly
    """
    setup_file(tmpdir)
    with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/"):
        try:
            cogniceptshell.interface.main()
            output = str(capsys.readouterr().out)
        except:
            pytest.fail(
                "Failed to check mandatory push command.", pytrace=True)

    expected_pattern = r"Required command is missing."
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_no_bag_args(tmpdir, capsys):
    """
    Test exception is thrown when bag command does not have arguments
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag'):
        try:
            cogniceptshell.interface.main()
            pytest.fail(
                "No exception thrown for no bag command.", pytrace=True)

        except SystemExit:
            # Expecting a system exit
            pass

        except Exception:
            pytest.fail(
                "Failed to throw exception for no bag args.", pytrace=True)


def test_push_no_bag(tmpdir, capsys):
    """
    Test exception is thrown when no bag is found in the expected location
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'latest'):
        try:
            cogniceptshell.interface.main()
            pytest.fail(
                "No exception thrown for no bags.", pytrace=True)

        except SystemExit:
            # Expecting a system exit
            pass

        except Exception:
            pytest.fail(
                "Failed to throw exception for no bags.", pytrace=True)


def test_push_specific_unavailable_bag(tmpdir, capsys, monkeypatch):
    """
    Test if a specific unavailable bag being pushed is caught
    """
    setup_file(tmpdir)
    setup_mock_bags(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)

    with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'bag10.bag'):
        try:
            cogniceptshell.interface.main()
            output = str(capsys.readouterr().out)
        except Exception as exp:
            pytest.fail(
                "Failed to push latest bag: " + str(exp), pytrace=True)

    expected_pattern = r"Specified bag file not found in expected location:"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_push_latest(tmpdir, capsys, monkeypatch):
    """
    Test if latest arg pushes the latest bag
    """
    setup_file(tmpdir)
    setup_mock_bags(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_upload_s3):

        with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'latest'):
            try:
                cogniceptshell.interface.main()
                output = str(capsys.readouterr().out)
            except Exception as exp:
                pytest.fail(
                    "Failed to push latest bag: " + str(exp), pytrace=True)

    # Check if correct file is chosen to be uploaded
    expected_pattern = r"bag3.bag"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)

    # Check if correct boto method is called
    expected_pattern = r"PutObject"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_push_specific_available_bag(tmpdir, capsys, monkeypatch):
    """
    Test if a specific bag can be pushed
    """
    setup_file(tmpdir)
    setup_mock_bags(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_upload_s3):

        with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'bag1.bag'):
            try:
                cogniceptshell.interface.main()
                output = str(capsys.readouterr().out)
            except Exception as exp:
                pytest.fail(
                    "Failed to push specific bag: " + str(exp), pytrace=True)

    # Check if correct file is chosen to be uploaded
    expected_pattern = r"bag1.bag"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)

    # Check if correct boto method is called
    expected_pattern = r"PutObject"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_push_bad_credentials(tmpdir, capsys, monkeypatch):
    """
    Test bad credentials are handled and retry is triggered
    """
    setup_file(tmpdir)
    setup_mock_bags(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_bad_cred_upload_s3):

        with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'bag1.bag'):
            try:
                cogniceptshell.interface.main()
                output = str(capsys.readouterr().out)
            except Exception as exp:
                pytest.fail(
                    "Failed to push specific bag: " + str(exp), pytrace=True)

    # Check if 3 attempts failed
    expected_pattern = r"Attempt #3"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_metadata_post_correct(tmpdir, capsys, monkeypatch):
    """
    Test if metadata is posted correctly
    """
    setup_file(tmpdir)
    setup_mock_bags(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)
    monkeypatch.setattr(requests, "post", mock_bagfile_api)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_upload_s3):

        with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'latest'):
            try:
                cogniceptshell.interface.main()
                output = str(capsys.readouterr().out)
            except Exception as exp:
                pytest.fail(
                    "Failed to push latest bag with correct metdata: " + str(exp), pytrace=True)

    # Check if correct file is chosen to be uploaded
    expected_pattern = r"bag3.bag"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)

    # Check if correct boto method is called
    expected_pattern = r"PutObject"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)

    # Check if metadata was posted correctly
    expected_pattern = r"Metadata posted to Cognicept Cloud."
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_metadata_bad_api(tmpdir, capsys, monkeypatch):
    """
    Test if an invalid metadata API configured is handled correctly
    """
    setup_wrong_api(tmpdir)
    setup_mock_bags(tmpdir)

    monkeypatch.setattr(requests, "get", mock_keyrotate_api)
    monkeypatch.setattr(requests, "post", mock_bagfile_api)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_upload_s3):

        with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'latest'):
            try:
                cogniceptshell.interface.main()
                output = str(capsys.readouterr().out)
            except Exception as exp:
                pytest.fail(
                    "Failed to push latest bag with correct metdata: " + str(exp), pytrace=True)

    # Check if correct file is chosen to be uploaded
    expected_pattern = r"bag3.bag"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)

    # Check if correct boto method is called
    expected_pattern = r"PutObject"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)

    # Check if metadata was posted correctly
    expected_pattern = r"Cognicept REST API error: https://bad.cognicept.systems/api/agent/v1/ responded with 401"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_metadata_bad_file(tmpdir, capsys, monkeypatch):
    """
    Test if missing runtime.env variables is handled correctly
    """
    setup_bad_file(tmpdir)
    setup_mock_bags(tmpdir)
    monkeypatch.setattr(requests, "post", mock_bagfile_api)

    with patch('botocore.client.BaseClient._make_api_call', new=mock_upload_s3):

        with ArgvContext('cognicept', 'push', '--path', str(tmpdir) + "/", '--bag', 'latest'):
            try:
                cogniceptshell.interface.main()
                pytest.fail(
                    "No exception thrown for bad runtime configuration.", pytrace=True)
            except SystemExit:
                # Expecting a system exit
                pass
            except Exception as exp:
                pytest.fail(
                    "Failed to push latest bag with correct metdata: " + str(exp), pytrace=True)
