# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> AgentLifeCycle handles life cycle of Cognicept Agents

import time
import docker
import boto3
import base64
import json
import os
import sys
import subprocess
import dateutil
from datetime import datetime
import re
import glob
from multiprocessing import Process, Queue
import requests
import botocore
import shutil
import pkg_resources
from tabulate import tabulate
from cogniceptshell.common import bcolors
from cogniceptshell.common import generate_progress_bar
from cogniceptshell.common import permission_safe_docker_call
from subprocess import DEVNULL
from docker.types import LogConfig


class AgentLifeCycle:
    """
    A class to manage agent and Cognicept's docker container lifecycle
    ...

    Parameters
    ----------
    None

    Methods
    -------
    configure_containers(cfg):
        Loads agent configuration from `COG_AGENT_CONTAINERS` and `COG_AGENT_IMAGES`
    get_status(args):
        Prints status of docker containers listed in `COG_AGENT_CONTAINERS`.
    get_last_event(args):
        Prints last log in `~/.cognicept/agent/logs/`.
    restart(args):
        Stops and starts the containers listed in `COG_AGENT_CONTAINERS`.
    start(args):
        Starts the containers listed in `COG_AGENT_CONTAINERS`. If `args` has parameter `list`, starts only containers in the list.
    stop(args):
        Stops the containers listed in `COG_AGENT_CONTAINERS`. If `args` has parameter `list`, stops only containers in the list.
    update(args):
        Pulls docker images listed in `COG_AGENT_IMAGES`.
    run_orbitty(args):
        Starts Orbitty.
    """

    # default configuration of containers and images
    _docker_container_names = ["cgs_diagnostics_agent", "remote_intervention_agent",
                               "cgs_diagnostics_ecs_api", "cgs_diagnostics_streamer_api", "cgs_bagger_server"]
    _docker_images = {}
    _docker_images["remote_intervention_agent"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/remote_intervention_agent:latest"
    _docker_images["kriya_watchdog"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/remote_intervention_agent:latest"
    _docker_images["cgs_diagnostics_agent"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_agent:latest"
    _docker_images["cgs_diagnostics_ecs_api"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_api:latest"
    _docker_images["cgs_diagnostics_streamer_api"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_api:latest"
    _docker_images["orbitty"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/orbitty:latest"
    _docker_images["cgs_bagger_server"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_rosbagger:latest"

    def configure_containers(object, cfg):
        """
        Loads agent configuration from `COG_AGENT_CONTAINERS` and `COG_AGENT_IMAGES`

                Parameters:
                        cfg (Configuration): Cognicept configuration
                Returns:
                        None
        """

        if("COG_AGENT_CONTAINERS" in cfg.config and "COG_AGENT_IMAGES" in cfg.config):
            container_names = cfg.config["COG_AGENT_CONTAINERS"].split(";")
            image_names = cfg.config["COG_AGENT_IMAGES"].split(";")
            if(len(image_names) == len(container_names)):
                object._docker_container_names = container_names
                object._docker_images = {}
                i = 0
                for container_name in container_names:
                    object._docker_images[container_name] = image_names[i]
                    i = i + 1
            else:
                print(
                    "`COG_AGENT_CONTAINERS` and `COG_AGENT_IMAGES` do not coincide. Using default.")

            if("COG_ORBITTY_ENABLED" in cfg.config and "COG_ORBITTY_IMAGE" in cfg.config):
                if(bool(cfg.config["COG_ORBITTY_ENABLED"])):
                    object._docker_images["orbitty"] = cfg.config["COG_ORBITTY_IMAGE"]
        else:
            print(
                "Undefined `COG_AGENT_CONTAINERS` or `COG_AGENT_IMAGES`. Using default.")

    def _get_latest_log_loc(object, args):
        """
        Retrieve path to the last log in `~/.cognicept/agent/logs/` relative to `~/.cognicept/` or `path` specified by args.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        latest_log_loc (str): path to latest log relative to `~/.cognicept/`
        """
        # get latest log location
        latest_log_loc_file_path = os.path.expanduser(
            args.path+"agent/logs/latest_log_loc.txt")
        latest_log_loc = ""
        try:
            with open(latest_log_loc_file_path) as txt_file:
                latest_log_loc_temp = txt_file.readline()
                latest_log_loc_temp = latest_log_loc_temp[:-1]
                latest_log_loc = latest_log_loc_temp.replace(
                    "/$HOME/.cognicept/", "")
                latest_log_loc = latest_log_loc.replace(".cognicept/", "")
        except:
            cgs_agent_status = bcolors.FAIL + "UNKNOWN" + bcolors.ENDC

        return latest_log_loc

    def get_status(object, args):
        """
        Prints status of docker containers listed in `COG_AGENT_CONTAINERS`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`

        """
        permission_docker_call_result = permission_safe_docker_call(
            docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        # check status of cgs_agent
        # get latest log location
        latest_log_loc = object._get_latest_log_loc(args)
        # read latest status and set for display
        file_path = os.path.expanduser(
            args.path+latest_log_loc+"/logDataStatus.json")
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                period_since_update = datetime.utcnow(
                ) - dateutil.parser.parse(data["timestamp"])
                if(period_since_update.seconds < 30 and period_since_update.seconds >= 0):
                    cgs_agent_status = bcolors.OKBLUE + \
                        data["message"].upper() + bcolors.ENDC
                else:
                    cgs_agent_status = bcolors.WARNING + "STALE" + bcolors.ENDC

        except:
            cgs_agent_status = bcolors.FAIL + "Error" + bcolors.ENDC

        for container_name in object._docker_container_names:
            print(container_name, end=': ', flush=True)
            try:
                container = client.containers.get(container_name)
                if container.status != "running":
                    print(bcolors.WARNING + "OFFLINE" + bcolors.ENDC)
                else:
                    if(container_name == "cgs_diagnostics_agent"):
                        print(cgs_agent_status)
                    elif(container_name == "remote_intervention_agent"):
                        object._parse_remote_intervention_agent_logs(
                            container.logs(tail=50))
                    else:
                        print(bcolors.OKBLUE + "ONLINE" + bcolors.ENDC)
            except docker.errors.NotFound:
                print(bcolors.FAIL + "CONTAINER NOT FOUND" + bcolors.ENDC)

    def get_last_event(object, args):
        """
        Prints last log in `~/.cognicept/agent/logs/`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`

        """
        # get latest log location
        latest_log_loc = object._get_latest_log_loc(args)

        # read and display latest log if any
        file_path = os.path.expanduser(args.path+latest_log_loc)
        try:
            print(bcolors.OKBLUE +
                  "Looking for the latest event log..." + bcolors.ENDC)
            # should read only latest logData#.json file and not logDataStatus.json
            list_of_log_files = [fn for fn in glob.glob(file_path + "/*.json")
                                 if not os.path.basename(fn).endswith("logDataStatus.json")]
            latest_log_file = max(list_of_log_files, key=os.path.getctime)

            with open(latest_log_file) as json_file:
                data = json.load(json_file)
                print(bcolors.OKGREEN+"Latest Event Log:" + bcolors.ENDC)
                print(json.dumps(data, indent=4, sort_keys=True))
        except:
            print(bcolors.WARNING + "No event logs present." + bcolors.ENDC)

    def _parse_remote_intervention_agent_logs(object, logs):
        """
        Parses logs to find status of remote intervention agent. Prints status.

                Parameters:
                        logs: container logs

        """
        logs_lines = logs.splitlines()
        # parse logs to get current status
        ri_agent_status = {}
        ri_agent_status["AGENT"] = ""
        ri_agent_status["WEBRTC"] = ""
        ri_agent_status["WEBSOCKET"] = ""

        # find latest status of the each module (agent, webrtc, websocket)
        for line in reversed(logs_lines):
            for key, value in ri_agent_status.items():
                if(value != ""):
                    continue
                matches = re.search(
                    '^.*{}:: STATUS:: (?P<status>.*).*$'.format(key), str(line))
                if(matches is not None):
                    ri_agent_status[key] = matches.groups(0)[0]
            if(ri_agent_status["AGENT"] != "" and ri_agent_status["WEBRTC"] != "" and ri_agent_status["WEBSOCKET"] != ""):
                continue

        output_text = bcolors.OKBLUE + "ONLINE" + bcolors.ENDC

        for key, value in ri_agent_status.items():
            if(value == ""):
                # if not found, it was not yet initialized
                output_text = bcolors.WARNING + "NOT INITIALIZED" + bcolors.ENDC
                break
            if(value != "OK"):
                output_text = bcolors.WARNING + key + value + bcolors.ENDC
                break
        print(output_text)

    def _detached_restart(object, args):
        """
        Runs _restart_protocol in detached mode with printing muted.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """

        if os.fork() != 0:
            return
        sys.stdout = open(os.devnull, 'w')
        result = object._restart_protocol(args)
        sys.stdout = sys.__stdout__
        return result

    def _restart_protocol(object, args):
        """
        Stops and starts the containers listed in `COG_AGENT_CONTAINERS`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        object.stop(args)
        result = object.start(args)
        return result

    def restart(object, args):
        """
        Stops and starts the containers listed in `COG_AGENT_CONTAINERS`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded in attached mode, always True in detached mode
        """
        if args.detach:
            result = True
            print("Running restart in detached mode")
            p = Process(target=object._detached_restart, args=(args,))
            p.start()
        else:
            result = object._restart_protocol(args)

        return result

    def start(object, args):
        """
        Starts the containers listed in `COG_AGENT_CONTAINERS`. If `args` has parameter `list`, starts only containers in the list.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        print("Called start")
        print("Starting agents")
        result = object.run_agents(args)
        return result

    def stop(object, args):
        """
        Stops the containers listed in `COG_AGENT_CONTAINERS`. If `args` has parameter `list`, stops only containers in the list.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """

        print("Stopping agents")
        result = object.remove_agents(args)
        return result

    def status(object, args):
        object.get_status(args)
        object.status_datadog(args)
        return True

    def remove_agents(object, args):
        """
        Stops the containers listed in `args.list`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """

        # if list of agents is not specified, restart all
        if(not hasattr(args, 'list') or len(args.list) == 0):
            args.list = object._docker_container_names
        permission_docker_call_result = permission_safe_docker_call(
            docker.from_env)
        if permission_docker_call_result is None:
            return False

        client = permission_docker_call_result
        print("STOP: ")
        flag_success = True
        for container_name in args.list:
            print("   - " + container_name, end=': ', flush=True)
            try:
                container = client.containers.get(container_name)
                container.stop(timeout=10)
                container.remove()
                print(bcolors.OKBLUE + "DONE" + bcolors.ENDC)
            except docker.errors.NotFound:
                print(bcolors.WARNING + "NOT FOUND" + bcolors.ENDC)
                flag_success = False
            except docker.errors.APIError:
                print(bcolors.FAIL + "ERROR" + bcolors.ENDC)
                flag_success = False
        return flag_success

    def run_agents(object, args):
        """
        Starts the containers listed in `args.list`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        # if list of agents is not specified, restart all
        if(not hasattr(args, 'list') or len(args.list) == 0):
            args.list = object._docker_container_names

        object._agent_run_options = {}
        object._agent_run_options["cgs_diagnostics_agent"] = {"command": "rosrun error_resolution_diagnoser error_resolution_diagnoser", "volumes": {
            args.config.config_path + "agent/logs/": {"bind": "/root/.cognicept/agent/logs", "mode": "rw"}}, "network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_ecs_api"] = {
            "command": "/src/ecs_endpoint.py", "network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_streamer_api"] = {"command": "/src/streamer_endpoint.py", "volumes": {
            args.config.config_path + "agent/logs/bunched_logs": {"bind": "/root/.cognicept/agent/logs/bunched_logs", "mode": "rw"}}, "network_mode": "host"}

        object._agent_run_options["health_aggregator"] = {"command": "roslaunch health_monitoring_aggregator aggregator.launch --wait", "volumes": {
            args.config.config_path + "health_config.yaml": {"bind": "/home/aggregator_ws/src/health_monitoring_aggregator/config.yml", "mode": "rw"}}, "network_mode": "host"}

        # kriya run config
        object._agent_run_options["remote_intervention_agent"] = {
            "command": "", "network_mode": "host"}
        if(args.config.is_ssh_enabled()):
            object._agent_run_options["remote_intervention_agent"]["volumes"] = {
                args.config.config_path + "ssh/id_rsa": {"bind": "/root/.ssh/id_rsa", "mode": "rw"}}
        if(args.config.is_audio_enabled()):
            object._agent_run_options["remote_intervention_agent"]["devices"] = ["/dev/snd"]
        object._agent_run_options["kriya"] = object._agent_run_options["remote_intervention_agent"]
        object._agent_run_options["kriya_watchdog"] = {
            "command": "python3 /home/watchdog.py", "volumes": {
                args.config.config_path + "kriya_logs/": {"bind": "/root/logs/", "mode": "rw"},
                "/var/run/docker.sock/": {"bind": "/var/run/docker.sock/", "mode": "rw"}}}

        object._agent_run_options["kopilot"] = {"command": "", "network_mode": "host", "volumes": {
            args.config.config_path + "kockpit.yaml": {"bind": "/root/config/kockpit.yaml", "mode": "rw"}}}

        object._agent_run_options["rosbridge"] = {
            "command": "roslaunch rosbridge_server rosbridge_websocket.launch", "network_mode": "host"}
        object._agent_run_options["test"] = {"command": "bash"}
        object._agent_run_options["cgs_bagger_server"] = {"command": "rosrun cognicept_rosbagger bagger_action_server.py", "volumes": {
            args.config.config_path + "bags/": {"bind": "/root/.cognicept/bags", "mode": "rw"}}, "network_mode": "host"}
        object._agent_run_options["other"] = {
            "command": "", "network_mode": "host"}
        permission_docker_call_result = permission_safe_docker_call(
            docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        print("RUN: ")
        success_flag = True
        for container_name in args.list:
            print("   - " + container_name, end=': ', flush=True)
            try:
                if(container_name not in object._docker_images):
                    if("COG_AGENT_CONTAINERS" in args.config.config):
                        containers = " (configured list: " + \
                            args.config.config["COG_AGENT_CONTAINERS"] + ")"
                    else:
                        containers = ""
                    print(bcolors.WARNING + "NOT FOUND" +
                          bcolors.ENDC + containers)
                    success_flag = False
                    continue

                if(container_name in object._agent_run_options.keys()):
                    options = object._agent_run_options[container_name]
                else:
                    options = object._agent_run_options["other"]
                options["name"] = container_name
                options["detach"] = True
                options["environment"] = args.config.config
                options["restart_policy"] = {"Name": "unless-stopped"}
                options["tty"] = True
                options["log_config"] = LogConfig(
                    type=LogConfig.types.JSON, config={'max-size': '5m'})
                if "command" in options:
                    command = options.pop("command")
                else:
                    command = ""
                container = client.containers.run(
                    object._docker_images[container_name], command, **options)
                print(bcolors.OKBLUE + "DONE" + bcolors.ENDC)
            except docker.errors.ContainerError:
                print(bcolors.WARNING + "ALREADY EXISTS" +
                      bcolors.ENDC + " (run `cognicept update`)")
            except docker.errors.ImageNotFound:
                print(bcolors.WARNING + "IMAGE NOT FOUND" +
                      bcolors.ENDC + " (run `cognicept update`)")
                success_flag = False
            except docker.errors.APIError:
                print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
                success_flag = False
        return success_flag

    def status_datadog(object, args):
        """
        Prints datadog status.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        sts = subprocess.call(
            ['sudo', 'sh', '-c', "systemctl status datadog-agent", "-p"], shell=True, stdout=DEVNULL, stderr=DEVNULL)
        if sts == 0:
            print("Health monitor status:" +
                  bcolors.OKBLUE + " ACTIVE" + bcolors.ENDC)
        elif sts == 4:
            print("Health monitor status:" +
                  bcolors.FAIL + " NOT FOUND" + bcolors.ENDC)
        else:
            print("Health monitor status:" +
                  bcolors.WARNING + " INACTIVE" + bcolors.ENDC)

    def run_orbitty(object, args):
        """
        Starts Orbitty.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        None
        """
        os.system("xhost +local:root")
        permission_docker_call_result = permission_safe_docker_call(
            docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        try:
            options = {}
            options["name"] = "orbitty"
            options["detach"] = False
            options["privileged"] = True
            options["volumes"] = {}
            options["volumes"][args.config.config_path] = {
                "bind": "/config", "mode": "rw"}
            options["volumes"]["/tmp/.X11-unix"] = {
                "bind": "/tmp/.X11-unix", "mode": "rw"}
            environment = args.config.config
            environment["QT_X11_NO_MITSHM"] = 1
            environment["DISPLAY"] = ":0"
            options["environment"] = args.config.config
            options["remove"] = True
            options["tty"] = True
            command = "roslaunch orbitty orbitty.launch"
            client.containers.run(
                object._docker_images["orbitty"], command, **options)
        except docker.errors.ContainerError:
            print(bcolors.WARNING + "ALREADY RUNNING" + bcolors.ENDC)
        except docker.errors.ImageNotFound:
            print(bcolors.WARNING + "IMAGE NOT FOUND" +
                  bcolors.ENDC + " (run `cognicept update`)")
        except docker.errors.APIError:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
        os.system("xhost -local:root")

    def _update_protocol(object, args):
        """
        Pulls docker images listed in `COG_AGENT_IMAGES`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        # Attempt to login to ECR client
        login_success = object._ecr_login(args)

        # If login failed, return false
        if login_success is False:
            print("Your update credentials may have expired. Run `cognicept keyrotate` to refresh credentials and try `cognicept update` again.")
            return False

        print("Info: This may take a while depending on your connection.")
        images = set(object._docker_images.values())

        # load extra images to update
        if("COG_EXTRA_IMAGES" in args.config.config):
            image_names = args.config.config["COG_EXTRA_IMAGES"].split(";")
            if(len(image_names) > 0):
                images = images.union(set(image_names))

        N = len(images)
        i = 0
        success_flag = True
        for image_name in images:
            i = i + 1
            image_name_short = image_name.replace(
                "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/", "cognicept/")
            try:
                for status in object.docker_client.pull(image_name, stream=True, decode=True):
                    if("progress" not in status):
                        status["progress"] = ""
                    if("status" not in status):
                        status["status"] = "Error"
                    terminal_size = shutil.get_terminal_size().columns
                    progress = ""
                    if("progressDetail" in status and "total" in status["progressDetail"]):
                        progress = generate_progress_bar(
                            status["progressDetail"]["current"], status["progressDetail"]["total"], 1, 10)
                        status = "[" + str(i) + "/" + str(N) + "] " + image_name_short + \
                            " - " + status["status"] + " " + progress
                        if(terminal_size > 0):
                            print('{:{terminal_size}.{terminal_size}}'.format(
                                status, terminal_size=terminal_size), end="\r", flush=True)
                        else:
                            print('{:{trm_sz}.{trm_sz}}'.format(
                                status, trm_sz=80), end="\r", flush=True)
                print("[" + str(i) + "/" + str(N) + "] " + image_name_short +
                      " - " + bcolors.OKBLUE + "OK" + bcolors.ENDC + "\033[K")
            except docker.errors.ImageNotFound:
                print("[" + str(i) + "/" + str(N) + "] " + image_name_short +
                      " - " + bcolors.FAIL + "FAILED" + bcolors.ENDC + "\033[K")
                success_flag = False
            except:
                print("[" + str(i) + "/" + str(N) + "] " + image_name_short +
                      " - " + bcolors.FAIL + "FAILED" + bcolors.ENDC + "\033[K")
                success_flag = False

        print("Info: Run `cognicept restart` to redeploy updated agents.")
        return success_flag

    def _detached_update(object, args):
        """
        Runs the _update_protocol that pulls docker images listed in `COG_AGENT_IMAGES`.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        if os.fork() != 0:
            return

        sys.stdout = open(os.devnull, 'w')

        result = object._update_protocol(args)

        sys.stdout = sys.__stdout__

        return result

    def update(object, args):
        """
        Pulls docker images listed in `COG_AGENT_IMAGES`. Can be run in detached mode where printing is muted

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): Always True if run in detached mode, otherwise True if successful
        """
        if args.detach:
            result = True
            print("Running update in detached mode")
            p = Process(target=object._detached_update, args=(args,))
            p.start()
        else:
            result = object._update_protocol(args)

        return result

    def _construct_ecr_client(object, config_obj):
        """
        Member utility function to create ECR client `object.ecr_client` based on runtime.env credentials

                Parameters:
                        config_obj (Configuration): object holding Cognicept configuration
                Returns:
                        None      
        """
        # Get config
        local_cfg = config_obj.fetch_aws_keys()
        if local_cfg == False:
            return False
        if 'SessionToken' in local_cfg:
            object.ecr_client = boto3.client(
                'ecr', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AccessKeyId'],
                aws_secret_access_key=local_cfg['SecretAccessKey'],
                aws_session_token=local_cfg['SessionToken'])
        else:
            object.ecr_client = boto3.client(
                'ecr', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AccessKeyId'],
                aws_secret_access_key=local_cfg['SecretAccessKey'])
        return True

    def _ecr_login(object, args):
        """
        Member utility function that is called to login to ECR

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        # Construct client
        result = object._construct_ecr_client(args.config)
        if result == False:
            return False
        num_retries = 3
        for trial in range(num_retries):
            try:
                # Get token
                token = object.ecr_client.get_authorization_token()
                # Parse username, password
                username, password = base64.b64decode(
                    token['authorizationData'][0]['authorizationToken']).decode().split(':')
                # Get registry
                registry = token['authorizationData'][0]['proxyEndpoint']
                # Login
                docker_call_result = permission_safe_docker_call(docker.APIClient,
                                                                 base_url='unix://var/run/docker.sock')
                if docker_call_result is None:
                    return False

                object.docker_client = docker_call_result

                object.docker_client.login(username, password,
                                           registry=registry, reauth=True)
                # Return true for successful login
                return True
            except (docker.errors.APIError, botocore.exceptions.ClientError):
                # On failure, retry
                print('Attempt #' + str(trial+1) + bcolors.FAIL +
                      " FAILED" + bcolors.ENDC + "\033[K")
                # Wait for 1 second before retrying
                time.sleep(1.0)
        # If the loop is completed, login failed, so return false
        return False

    def display_version(object, args):
        """
        Display Cognicept-Shell version and docker images version

        Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        version = pkg_resources.require("cognicept-shell")[0].version
        data = {}
        images_version = []
        data['Container Name'] = object._docker_container_names
        # default value for version: "unknown/latest"
        for x in object._docker_images:
            image_data = object._docker_images[x].split(':')
            if len(image_data) > 1:
                images_version.append(image_data[1])
                image_data = []
            else:
                images_version.append("unknown/latest")
        data['Version'] = images_version
        print("Cognicept Shell Version "+version)
        print(tabulate(data, headers='keys', tablefmt='psql'))
        print("Runtime enviroment file directory: " + args.path)
