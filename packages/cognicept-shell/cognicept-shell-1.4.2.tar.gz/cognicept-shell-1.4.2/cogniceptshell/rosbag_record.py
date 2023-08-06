# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Swarooph Seshadri (swarooph@cognicept.systems)
# --> RosbagRecord class handles on demand rosbag recording for cognicept-shell

from dotenv import dotenv_values
import os
import time
from datetime import datetime, timedelta
import glob
import docker
from cogniceptshell.common import bcolors
from cogniceptshell.agent_life_cycle import AgentLifeCycle
from cogniceptshell.pusher import Pusher
from cogniceptshell.common import permission_safe_docker_call

class RosbagRecord:
    """
    A class to manage Cognicept's rosbag recording sessions
    ...

    Parameters
    ----------
    None

    Methods
    -------
    record(args):
        Main entrypoint to manage recording session for start/all/stop/pause/resume/status modes.
    start_record(args):
        Executes a docker command inside `cgs_bagger_server` container to start the recording session.
        Has built in retry mechanism based on bag file status which when fails restarts the `cgs_bagger_server` container automatically. 
        `args.start` should have a mandatory list of topics to record or `args.all` to record all topics.
    stop_record(args):
        Executes a docker command inside `cgs_bagger_server` container to stop the recording session.
        Has built in retry mechanism based on bag file status which when fails restarts the `cgs_bagger_server` container automatically.
        If `args.stop` is set to `autopush`, it calls a `Pusher` instance to upload the latest bag to S3.
    pause_record(args):
        Executes a docker command inside `cgs_bagger_server` container to pause the recording session.
        Has built in retry mechanism based on the container response in case command fails.
    resume_record(args):
        Executes a docker command inside `cgs_bagger_server` container to resume the recording session.
        Has built in retry mechanism  based on the container response in case command fails.
    get_record_status(args):
        Executes a docker command inside `cgs_bagger_server` container to get the status the recording session.
        Has built in retry mechanism  based on the container response in case command fails.
    print_status(args):
        Parses container response and prints to console if one exists and returns TRUE. If not returns false.
        Used to manage retry mechanism for pause/resume/status modes.
    get_latest_type_bag(args):
        Utility method to get the latest '.bag.active' or '.bag' file depending on what `type` is set to.
        Used to manage retry mechanism for start/stop modes.
    restart_bag_record_server(args):
        Utility function to restart the `cgs_bagger_server` container.
        Uses an instance of the `AgentLifeCycle` class.
    """

    def record(self, args):
        """
        Main entrypoint to manage recording session for start/all/stop/pause/resume/status modes.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        # Entry point method to decide which mode to call
        if((args.start is None) and (args.stop is False)
           and (args.pause is False) and (args.resume is False)
           and (args.all is False) and (args.status is False)):
            # start or stop must be provided
            print(bcolors.FAIL +
                  ("Required command is missing."
                   " Check `cognicept record --help` "
                   "for more commands available.") +
                  bcolors.ENDC)
        elif args.start:
            # to start recording
            print(bcolors.OKBLUE + "Starting recording" + bcolors.ENDC)
            self.start_record(args)
        elif args.all:
            # to start recording
            print(bcolors.OKBLUE + "Starting recording" + bcolors.ENDC)
            self.start_record(args)
        elif args.stop:
            # to stop recording
            print(bcolors.OKBLUE + "Stopping recording" + bcolors.ENDC)
            self.stop_record(args)
        elif args.pause:
            # to pause recording
            print(bcolors.OKBLUE + "Pausing recording" + bcolors.ENDC)
            self.pause_record(args)
        elif args.resume:
            # to resume recording
            print(bcolors.OKBLUE + "Resuming recording" + bcolors.ENDC)
            self.resume_record(args)
        elif args.status:
            # query recording status
            print(bcolors.OKBLUE + "Getting recording status" + bcolors.ENDC)
            self.get_record_status(args)
        else:
            # This should never execute
            print(bcolors.FAIL +
                  ("Required command is missing."
                   " Check `cognicept record --help` "
                   "for more commands available.") +
                  bcolors.ENDC)

    def validate_topic_names(self, args):
        valid_topic_names = []
        invalid_topic_names = []
        for topic in args.start:
            if topic.startswith('/'):
                valid_topic_names.append(topic)
            else:
                invalid_topic_names.append(topic)
                        
        if not valid_topic_names:
            print(bcolors.FAIL +
                  ("Valid Topic Names should start with a `/`. "
                  "Only these will be considered for recording. "
                  "No valid topic names found.") +
                  bcolors.ENDC)
            raise SystemExit
        else:
            print('Valid Topic Names: ', ','.join(valid_topic_names))

        args.start = valid_topic_names

    def start_record(self, args):
        """
        Executes a docker command inside `cgs_bagger_server` container to start the recording session.
        Has built in retry mechanism based on bag file status which when fails restarts the `cgs_bagger_server` container automatically. 
        `args.start` should have a mandatory list of topics to record 
        (or)
        `args.all` to record all topics.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        rosbag_start_cmd = "record_cmd.bash start "
        if args.all:
            selected_topics = '-a'
            rosbag_start_cmd = rosbag_start_cmd + selected_topics
        else:
            self.validate_topic_names(args)
            selected_topics = ','.join(args.start)
            rosbag_start_cmd = rosbag_start_cmd + "'" + selected_topics + "'"

        permission_docker_call_result = permission_safe_docker_call(docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        try:
            container = client.containers.get('cgs_bagger_server')
            num_retries = 3

            for retry in range(0, num_retries):

                container_response = container.exec_run(
                    rosbag_start_cmd, stream=True, stdout=True)
                # status = self.print_status(container_response)
                latest_active_bag = self.get_latest_type_bag(args, "active")

                if latest_active_bag:
                    print("Active bag file:   ", latest_active_bag)
                    break

                if retry < num_retries - 1:
                    print(bcolors.WARNING +
                          "Try failed. Retrying..." + bcolors.ENDC)
                else:
                    print(
                        bcolors.FAIL +
                        ("Recording Failed. "
                         "Restarting bag recording server. ") +
                        bcolors.ENDC)
                    self.restart_bag_record_server(args)
                    print(
                        bcolors.OKBLUE +
                        "Please try your record command again." +
                        bcolors.ENDC)
                    raise(SystemExit)

            print(bcolors.OKBLUE +
                  ("Use `cognicept record --status` "
                   "for detailed progress.\n"
                   "Use `cognicept record --stop` "
                   "to stop recording.") +
                  bcolors.ENDC)
        except docker.errors.APIError as e:
            print(
                bcolors.FAIL + "Bag Record Server not running or incorrect command provided." + bcolors.ENDC)

    def stop_record(self, args):
        """
        Executes a docker command inside `cgs_bagger_server` container to stop the recording session.
        Has built in retry mechanism based on bag file status which when fails restarts the `cgs_bagger_server` container automatically.
        If `args.stop` is set to `autopush`, it calls a `Pusher` instance to upload the latest bag to S3.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        rosbag_stop_cmd = "record_cmd.bash stop"
        permission_docker_call_result = permission_safe_docker_call(docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        try:
            container = client.containers.get('cgs_bagger_server')
            num_retries = 3

            for retry in range(0, num_retries):

                container_response = container.exec_run(
                    rosbag_stop_cmd, stream=True, stdout=True)
                # status = self.print_status(container_response)
                latest_bag = self.get_latest_type_bag(args, "bag")

                if latest_bag:
                    print("Recorded bag file: ", latest_bag)
                    break

                if retry < num_retries - 1:
                    print(bcolors.WARNING +
                          "Try failed. Retrying..." + bcolors.ENDC)
                else:
                    print(
                        bcolors.FAIL +
                        ("Unable to stop recording. "
                         "Restarting bag recording server. ") +
                        bcolors.ENDC)
                    self.restart_bag_record_server(args)
                    print(
                        bcolors.OKBLUE +
                        "Please start a new recording session." +
                        bcolors.ENDC)
                    raise(SystemExit)

            if args.stop == "autopush":
                pusher_instance = Pusher()
                args.bag = "latest"
                pusher_instance.push(args)
            else:
                print(bcolors.OKBLUE +
                      ("Use `cognicept push --bag` "
                       "to upload the latest recording to cloud.") +
                      bcolors.ENDC)
        except docker.errors.APIError as e:
            print(
                bcolors.FAIL + "Bag Record Server not running or incorrect command provided." + bcolors.ENDC)

    def pause_record(self, args):
        """
        Executes a docker command inside `cgs_bagger_server` container to pause the recording session.
        Has built in retry mechanism based on the container response in case command fails.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        rosbag_pause_cmd = "record_cmd.bash pause"
        permission_docker_call_result = permission_safe_docker_call(docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        try:
            container = client.containers.get('cgs_bagger_server')
            num_retries = 3

            for retry in range(0, num_retries):

                container_response = container.exec_run(
                    rosbag_pause_cmd, stream=True, stdout=True)
                resp_status = self.print_status(container_response)

                if resp_status:
                    print(bcolors.OKBLUE +
                          ("Use `cognicept record --resume` "
                           "to resume recording session.") +
                          bcolors.ENDC)
                    break

                if retry < num_retries - 1:
                    print(bcolors.WARNING +
                          "Try failed. Retrying..." + bcolors.ENDC)
                else:
                    print(
                        bcolors.FAIL +
                        ("Pausing Failed. "
                         "Try to stop completely using `cognicept record --stop`") +
                        bcolors.ENDC)

        except docker.errors.APIError as e:
            print(
                bcolors.FAIL + "Bag Record Server not running or incorrect command provided." + bcolors.ENDC)

    def resume_record(self, args):
        """
        Executes a docker command inside `cgs_bagger_server` container to resume the recording session.
        Has built in retry mechanism  based on the container response in case command fails.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        rosbag_resume_cmd = "record_cmd.bash resume"
        permission_docker_call_result = permission_safe_docker_call(docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        try:
            container = client.containers.get('cgs_bagger_server')
            num_retries = 3

            for retry in range(0, num_retries):

                container_response = container.exec_run(
                    rosbag_resume_cmd, stream=True, stdout=True)
                resp_status = self.print_status(container_response)

                if resp_status:
                    print(bcolors.OKBLUE +
                          ("Use `cognicept record --stop` "
                           "to stop recording session.") +
                          bcolors.ENDC)
                    break

                if retry < num_retries - 1:
                    print(bcolors.WARNING +
                          "Try failed. Retrying..." + bcolors.ENDC)
                else:
                    print(
                        bcolors.FAIL +
                        ("Resuming Failed. "
                         "Try to stop completely using `cognicept record --stop`") +
                        bcolors.ENDC)

        except docker.errors.APIError as e:
            print(
                bcolors.FAIL + "Bag Record Server not running or incorrect command provided." + bcolors.ENDC)

    def get_record_status(self, args):
        """
        Executes a docker command inside `cgs_bagger_server` container to get the status the recording session.
        Has built in retry mechanism  based on the container response in case command fails.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        rosbag_status_cmd = "record_cmd.bash status"
        permission_docker_call_result = permission_safe_docker_call(docker.from_env)
        if permission_docker_call_result is None:
            return False
        client = permission_docker_call_result
        try:
            container = client.containers.get('cgs_bagger_server')
            num_retries = 3

            for retry in range(0, num_retries):

                container_response = container.exec_run(
                    rosbag_status_cmd, stream=True, stdout=True)
                resp_status = self.print_status(container_response)

                if resp_status:
                    print(bcolors.OKBLUE +
                          ("Use `cognicept record --help` "
                           "for more information.") +
                          bcolors.ENDC)
                    break

                if retry < num_retries - 1:
                    print(bcolors.WARNING +
                          "Try failed. Retrying..." + bcolors.ENDC)
                else:
                    print(
                        bcolors.FAIL +
                        ("Failed to get status. "
                         "Try to stop completely using `cognicept record --stop` and restart bag recording server.") +
                        bcolors.ENDC)

        except docker.errors.APIError as e:
            print(
                bcolors.FAIL + "Bag Record Server not running or incorrect command provided." + bcolors.ENDC)

    def print_status(self, container_response):
        """
        Parses container response and prints to console if one exists
        Returns True/False based on if successful response was achieved.
        Used to manage retry mechanism for pause/resume/status modes.

                Parameters:
                        container_response: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        response_status (boolean): True if container_response is valid
        """
        output_response_str = str(next(container_response.output))
        str_beg = output_response_str.rfind('Recording state:')
        str_end = output_response_str.rfind('Goal Succeeded')

        if str_beg == -1:
            return False
        else:
            print(output_response_str[str_beg:str_end-2])
            return True

    def get_latest_type_bag(self, args, search_type):
        """
        Get the latest '.bag.active' or '.bag' file depending on what `type` is set to.
        Used to manage retry mechanism for start/stop modes.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                        search_type: Either `.active` or `.bag` based on which type of file needs to be found
                Returns:
                        latest_file (str): If file is found, full path str of the file otherwise ""
        """
        # Wait for the OS to initialize an active bag
        time.sleep(7.0)
        bag_path = os.path.expanduser(args.path+"bags")
        bag_list = glob.glob(bag_path+"/*." + search_type)
        if bag_list:
            latest_file = max(bag_list, key=os.path.getctime)
            latest_timestamp = os.path.getctime(latest_file)
            file_time = datetime.fromtimestamp(
                latest_timestamp)  # .strftime('%Y-%m-%d %H:%M:%S')
            sys_time = datetime.now()  # .strftime('%Y-%m-%d %H:%M:%S')
            if sys_time - file_time > timedelta(10.0):
                print('File time: ', file_time)
                print('Sys time: ', sys_time)
                print('Latest found file is not recent enough.')
                return ""
            else:
                # print('File time: ', file_time)
                # print('Sys time: ', sys_time)
                return latest_file
        else:
            return ""

    def restart_bag_record_server(self, args):
        """
        Utility function to restart the `cgs_bagger_server` container.
        Uses an instance of the `AgentLifeCycle` class.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        agent_lifetime = AgentLifeCycle()
        args.agents = None
        args.list = ['cgs_bagger_server']
        agent_lifetime.restart(args)
