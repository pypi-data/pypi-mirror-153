# Copyright 2020 Cognicept Systems
# Author: Swarooph Seshadri (swarooph@cognicept.systems)
# --> common utilities for the cognicept shell goes here.
import docker

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_progress_bar(iteration, total, decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
        Parameters:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    output = "|" + bar + "| " + percent + "%"
    return output

class DockerPermissionError():
    identifier_string = "Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))"
    suggestion = "Error while fetching server API version, Your current user might not have permissions to access the resources. If docker is newly installed try:\n " \
                 "          sudo usermod -aG docker $USER\n" \
                 "Followed by rebooting your system."



def permission_safe_docker_call(func, *args, **kwargs):
    """
    Run a function while catching for docker permissions related exceptions.

            Parameters:
                    func: function to be executed
                    args: list of positional arguments for executing func
                    kwargs: Mapping of keyword arguments for executing func
            Returns:
                    result: None if failed, else returns result for function call
    """
    try:
        result = func(*args,**kwargs)
    except docker.errors.DockerException as docker_exception:
        if str(docker_exception) == DockerPermissionError.identifier_string:
            print(DockerPermissionError.suggestion)
            return None
        else:
            raise docker_exception
    return result