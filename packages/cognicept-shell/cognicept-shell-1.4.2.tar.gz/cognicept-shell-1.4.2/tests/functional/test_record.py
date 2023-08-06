import os
import pytest
import re
import docker

from cli_test_helpers import ArgvContext, EnvironContext
from mock import patch
from docker.models.containers import Container
from docker.constants import DEFAULT_DOCKER_API_VERSION
from docker.errors import APIError

import cogniceptshell.interface


def setup_file(tmpdir):
    """
    Utility function to setup a fake runtime.env to run tests
    """
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2")
    p1 = tmpdir.mkdir("bags")
    b1 = p1.join('sample.bag')
    b1.write('placeholder')
    b2 = p1.join('sample.bag.active')
    b2.write('placeholder')


def mock_client(*args, **kwargs):
    """
    Mock function to setup a fake Docker client to get to the API calls.
    Individual API calls need to be mocked accordingly.
    """
    sample_client = docker.DockerClient(version=DEFAULT_DOCKER_API_VERSION)
    return sample_client


def mock_no_bagger(*args, **kwargs):
    """
    Mock function to raise docker error to spoof bagger container not available.
    """
    raise APIError("Mock API Error to spoof no bagger container running.")


class ContainerResponse():
    """
    Utility class to mimic container response returned after exec_run.
    Property output should be set to a generator object.
    """
    output = None


def get_status_str(cmd):
    """
    Utility function to return a generator object containing the status of bag recording to spoof container response.
    Takes the exec_run command to generate different types of responses.
    """

    status_str = ""
    if ("start" in cmd) or ("all" in cmd):
        status_str = "Recording state: Started. Goal Succeeded."
    elif "stop" in cmd:
        status_str = "Recording state: Stopped. Goal Succeeded."
    elif "pause" in cmd:
        status_str = "Recording state: Paused. Goal Succeeded."
    elif "resume" in cmd:
        status_str = "Recording state: Resumed. Goal Succeeded."
    elif "status" in cmd:
        status_str = "Recording state: Resumed. Goal Succeeded."
    yield status_str


def mock_bagger(*args, **kwargs):
    """
    Mock function that returns an empty Container object to spoof running of the bagger server container
    """
    return Container()


def mock_exec_run(*args, **kwargs):
    """
    Mock function that returns a ContainerResponse object to spoof running exec commands.
    Uses a generator object to yield bag record status like the docker logs API.
    """
    container_response = ContainerResponse()
    container_response.output = get_status_str(args[1])
    return container_response


def check_value(expected_pattern, output, expected_num_occurences):
    """
    Utility function to assert if an expected pattern is in an output 
    for specified # of occurrences
    """
    matches = re.findall(expected_pattern, output, re.MULTILINE)
    assert len(matches) == expected_num_occurences


def test_no_record_command(tmpdir, capsys):
    """
    Test if mandatory command missing is caught correctly
    """
    setup_file(tmpdir)
    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/"):
        try:
            cogniceptshell.interface.main()
            output = str(capsys.readouterr().out)
        except:
            pytest.fail(
                "Failed to check mandatory record command.", pytrace=True)

    expected_pattern = r"Required command is missing. Check `cognicept record --help` for more commands available."
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_no_start_args(tmpdir, capsys):
    """
    Test exception is thrown when start command does not have arguments
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--start'):
        try:
            cogniceptshell.interface.main()
            pytest.fail(
                "No exception thrown for no start command.", pytrace=True)

        except SystemExit:
            # Expecting a system exit
            pass

        except Exception:
            pytest.fail(
                "Failed to throw exception for no start args.", pytrace=True)


def test_no_server(tmpdir, capsys):
    """
    Test if bagger server is missing, it is caught correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--start', '/rosout'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_no_bagger):
                try:
                    cogniceptshell.interface.main()
                    output = str(capsys.readouterr().out)
                except:
                    pytest.fail(
                        "Failed to check server is running.", pytrace=True)

    expected_pattern = r"Bag Record Server not running or incorrect command provided."
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_invalid_topics(tmpdir, capsys):
    """
    Test if no valid topics are supplied, it is caught correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--start', 'rosout'):
        try:
            cogniceptshell.interface.main()
            pytest.fail(
                "No exception thrown for no valid topics.", pytrace=True)
        except SystemExit:
            # Expecting a system exit
            pass
        except:
            pytest.fail("Failed to invalid topics.", pytrace=True)


def test_start(tmpdir, capsys):
    """
    Test if start command performs correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--start', '/rosout'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_bagger):
                with patch("docker.models.containers.Container.exec_run", new=mock_exec_run):

                    try:
                        cogniceptshell.interface.main()
                        output = str(capsys.readouterr().out)
                    except:
                        pytest.fail(
                            "Uncaught exception detected", pytrace=True)

    expected_pattern = r"sample.bag.active"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_start_all(tmpdir, capsys):
    """
    Test if all command performs correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--all'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_bagger):
                with patch("docker.models.containers.Container.exec_run", new=mock_exec_run):
                    try:
                        cogniceptshell.interface.main()
                        output = str(capsys.readouterr().out)
                    except:
                        pytest.fail(
                            "Uncaught exception detected", pytrace=True)

    expected_pattern = r"sample.bag.active"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_pause(tmpdir, capsys):
    """
    Test if pause command performs correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--pause'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_bagger):
                with patch("docker.models.containers.Container.exec_run", new=mock_exec_run):
                    try:
                        cogniceptshell.interface.main()
                        output = str(capsys.readouterr().out)
                    except:
                        pytest.fail(
                            "Uncaught exception detected", pytrace=True)

    expected_pattern = r"Paused"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_resume(tmpdir, capsys):
    """
    Test if resume command performs correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--resume'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_bagger):
                with patch("docker.models.containers.Container.exec_run", new=mock_exec_run):
                    try:
                        cogniceptshell.interface.main()
                        output = str(capsys.readouterr().out)
                    except:
                        pytest.fail(
                            "Uncaught exception detected", pytrace=True)

    expected_pattern = r"Resumed"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)


def test_status(tmpdir, capsys):
    """
    Test if status command performs correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--status'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_bagger):
                with patch("docker.models.containers.Container.exec_run", new=mock_exec_run):
                    try:
                        cogniceptshell.interface.main()
                        output = str(capsys.readouterr().out)
                    except:
                        pytest.fail(
                            "Uncaught exception detected", pytrace=True)

        expected_pattern = r"Resumed"
        expected_num_occurences = 1
        check_value(expected_pattern, output, expected_num_occurences)


def test_stop(tmpdir, capsys):
    """
    Test if stop command performs correctly
    """
    setup_file(tmpdir)

    with ArgvContext('cognicept', 'record', '--path', str(tmpdir) + "/", '--stop'):
        with patch("docker.from_env", new=mock_client):
            with patch("docker.models.containers.ContainerCollection.get", new=mock_bagger):
                with patch("docker.models.containers.Container.exec_run", new=mock_exec_run):
                    try:
                        cogniceptshell.interface.main()
                        output = str(capsys.readouterr().out)
                    except:
                        pytest.fail(
                            "Uncaught exception detected", pytrace=True)

    expected_pattern = r"sample.bag"
    expected_num_occurences = 1
    check_value(expected_pattern, output, expected_num_occurences)
