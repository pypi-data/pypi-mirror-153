
import docker


class MockDockerClient:
    """
    Class to mock docker client
    """

    def __init__(self):
        self.containers = MockDockerContainers()


class MockDockerContainers:
    """
    Class to mock docker.containers API
    """

    def __init__(self):
        self._running_containers = []
        self._stopped_containers = []

    def run(self, docker_image, command, **options):
        """
        Mock run container command
        """
        if(not "name" in options):
            raise docker.errors.ContainerError("Container name is empty")
        container_name = options["name"]
        print("called run " + container_name)
        if(container_name in self._running_containers):
            raise docker.errors.ContainerError("Container already exists")
        else:
            self._running_containers.append(container_name)

    def _stop(self, container_name):
        """
        Helper stop container that is passed as lambda in returning docker object
        """
        self._running_containers.remove(container_name)
        self._stopped_containers.append(container_name)

    def _remove(self, container_name):
        """
        Helper remove function that is passed as lambda in returning docker object
        """
        self._stopped_containers.remove(container_name)

    def get(self, container_name):
        """
        Mock get container api
        """
        if(container_name in self._running_containers):
            def stop_function(timeout): return self._stop(container_name)
            def remove_function(): return self._remove(container_name)
            return MockContainer("running", stop_function, remove_function)
        else:
            raise docker.errors.NotFound("Container not found")


class MockContainer:
    """
    Class to mock docker.containers API
    """

    def __init__(self, status, stop_function, remove_function):
        self.status = status
        self.stop = stop_function
        self.remove = remove_function
