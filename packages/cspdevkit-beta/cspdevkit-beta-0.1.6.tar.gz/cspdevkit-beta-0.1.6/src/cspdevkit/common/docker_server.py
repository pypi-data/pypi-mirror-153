#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/19 10:15
# @Author  : xgy
# @Site    : 
# @File    : docker_server.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import time

from loguru import logger
import yaml
from cspdevkit.common.utils import RunSys
from cspdevkit.common.config import Configure
from cspdevkit.common.http_client import HttpClient

# import docker
# docker_client = docker.from_env()
#
# api_client = docker.APIClient()


class DockerServer:

    def __init__(self, name, version, port, c_name=None, reload=True):
        self.name = name
        self.version = version
        self.port = port
        self.reload = reload
        self.container_name = c_name
        self.getter_container_name()
        self.interface_config = Configure().data
        self.http_client = HttpClient()
        self.image_url = None
        self.docker_client = None
        self.api_client = None
        self.check_env()

    def check_env(self):

        try:
            import docker
        except ImportError:
            logger.error("there is no docker try to install it, pip install docker")
            install_cmd = "pip install docker"
            install_cmd2 = "pip uninstall pywin32 -y"
            install_cmd3 = "pip install pywin32"

            RunSys(command=install_cmd).run_cli()
            RunSys(command=install_cmd2).run_cli()
            RunSys(command=install_cmd3).run_cli()

            # raise ImportError("docker install successful, please retry")
        import docker
        try:
            self.docker_client = docker.from_env()
        except docker.errors.DockerException:
            raise EnvironmentError("please start docker server first")

        self.api_client = docker.APIClient()

    def getter_container_name(self):
        if not self.container_name:
            container_name = self.name + "-v" + str(self.version)
            self.container_name = container_name

    def start(self):
        self.check_image()
        self.check_container()
        time.sleep(3)

    def check_container(self):
        import docker

        container_stats = True
        # 需判断容器存在和容器运行
        is_container_running = False
        try:
            is_container_exists = self.docker_client.containers.get(self.container_name)
        except docker.errors.NotFound:
            logger.info("container not exists: {}".format(self.container_name))
            is_container_exists = False

        if not is_container_exists:
            run_cmd = "docker run -d --name " + self.container_name + " -p " + str(self.port) + ":" + "5000 " + self.image_url
            try:
                logger.info("run container from the {}".format(self.image_url))
                RunSys(run_cmd).run_cli()
                time.sleep(8)
                return container_stats
            except:
                logger.error("start container error: {}".format(run_cmd))
                raise IOError("start container error: {}".format(run_cmd))

        # container_l = docker_client.containers.get()
        container_l = self.docker_client.containers.list()
        for item in container_l:
            if item.name == self.container_name:
                is_container_running = True
                break
        if is_container_running:
            res = self.api_client.inspect_container(self.container_name)
            container_port = res['HostConfig']['PortBindings']['5000/tcp'][0]['HostPort']
            if str(self.port) != container_port:
                raise AttributeError("there is a container named " + self.container_name + " running, but the port is " + str(container_port) + ", please setting another container name by param 'c_name' or delete the old")
            logger.info("{} is running".format(self.container_name))
        if not is_container_running and is_container_exists:
            restart_cmd = "docker start " + self.container_name
            res = self.api_client.inspect_container(self.container_name)
            container_port = res['HostConfig']['PortBindings']['5000/tcp'][0]['HostPort']
            if str(self.port) != container_port:
                raise AttributeError("there is a container named " + self.container_name + " exists, but the port is " + str(container_port) + ", please setting another container name by param 'c_name' or delete the old")
            try:
                logger.info("the container {} is exited but not running, try to restart it".format(self.container_name))
                RunSys(restart_cmd).run_cli()
                time.sleep(10)
                container_l = self.docker_client.containers.list()
                for item in container_l:
                    if item.name == self.container_name:
                        # is_container_running = True
                        logger.info("the container {} restart success".format(self.container_name))
                        break
                    else:
                        logger.warning("the container {} restart failed after 10 seconds".format(self.container_name))
                # logger.info("the container {} restart success".format(self.container_name))
            except:
                logger.error("restart container error: {}".format(restart_cmd))
                raise IOError("restart container error: " + restart_cmd)

    def check_image(self):
        import docker
        image = None
        image_url = self.gen_image_info()
        self.image_url = image_url
        try:
            # image = docker_client.images.get(self.name)
            image = self.docker_client.images.get(image_url)
            logger.info("the image {} exited".format(image))
        except docker.errors.ImageNotFound:
            logger.warning("the image {} not found, will be download".format(self.name))
            # docker api，无日志输出
            # split_name = self.name.split(":")
            # repository = split_name[0] + ":" + split_name[1]
            # tag = split_name[2]
            # client.images.pull(repository=repository, tag=tag)
            # 命令行下载
            # pull_cmd = "docker pull " + self.name
            pull_cmd = "docker pull " + image_url
            cmd_statu = RunSys(pull_cmd).run_cli()
            if not cmd_statu:
                raise KeyError("there is no docker image namded " + self.name)
        return image

    def gen_image_info(self):
        parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
        docker_dict_path = os.path.join(parent_path, "common/config", "docker_dict.yaml")
        info = {"info": "the images dict"}
        if not os.path.exists(docker_dict_path):
            with open(docker_dict_path, "w", encoding="utf-8") as fw:
                yaml.dump(info, fw)

        if self.reload:
            try:
                url = self.interface_config["search"]["docker"]
                name = self.name
                params = {"name": name, "version": self.version}
                res_dict = self.http_client.get(url, **params)
                image_url = res_dict["data"]["url"]
                self.updata_docker_config(name, image_url, docker_dict_path)
            except Exception:
                logger.error("can not search image info from the back-end. The last downloaded image will be used")
                docker_dict = Configure(path=docker_dict_path).data
                image_url = docker_dict.get(self.name, 0)
                if not image_url:
                    raise KeyError("No image found locally")
        else:
            docker_dict = Configure(path=docker_dict_path).data
            image_url = docker_dict.get(self.name, 0)
            if not image_url:
                raise KeyError("No image found locally")

        return image_url

    def updata_docker_config(self, name, url, path):
        docker_dict = Configure(path=path).data
        docker_dict[name] = url
        with open(path, "w", encoding="utf-8") as fw2:
            yaml.dump(docker_dict, fw2)


if __name__ == '__main__':
    print("start")

    # name = "unst2st"
    # version = 0.1
    # test_docker = DockerServer(name=name, version=version, port=9889, reload=False)
    # test_docker.check_image()
    # test_docker.check_container()
    # test_docker.getter_container_name()


