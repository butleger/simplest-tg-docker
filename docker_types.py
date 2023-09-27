import docker.types as types

class ContainerInfo:
    def __init__(self, name=None, image=None, labels=None, short_id=None, status=None):
        self.name = name
        self.image = image
        self.labels = labels
        self.short_id = short_id
        self.status = status


    @classmethod
    def from_docker_container(cls, container):
        return ContainerInfo(container.name, container.image, container.labels, container.short_id, container.status)


    def to_html(self):
        return  f"<b>{self.name}</b>\n" + \
                f"    Image: {str(self.image.tags[0])}\n" + \
                f"    Short ID: {str(self.short_id)}\n" + \
                f"    Status: {str(self.status)}\n"


class ImageInfo:
    def __init__(self, labels=None, tags=None, short_id=None):
        self.labels = labels
        self.tags = tags
        self.short_id = short_id


    @classmethod
    def from_docker_image(cls, image):
        return ImageInfo(image.labels, image.tags, image.short_id)


    def to_html(self):
        if len(self.tags) > 0:
            return f"<b>{self.tags[0]}</b>\n" + \
                    f"    Short ID: {self.short_id}\n"
        else:
            return ""


class NetworkInfo:
    def __init__(self, name=None, short_id=None, containers=None):
        self.name = name
        self.short_id = short_id
        self.containers = containers

    @classmethod
    def from_docker_network(cls, network):
        containers_info = []
        for docker_container in network.containers:
            containers_info.append(ContainerInfo(docker_container))
        return NetworkInfo(network.name, network.short_id, containers_info)


    def to_html(self):
        connected_containers = ""
        for container in self.containers:
            containers_info_html += container.to_html()
        return f"<b>{self.name}</b>\n" + \
                f"    Short ID: {self.short_id}\n" + \
                f"    Connected containers: \n" + \
                f"{containers_info_html}"