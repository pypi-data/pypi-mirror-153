import os
import shutil
from typing import Optional, Dict

import yaml
from openmodule.config import settings
from openmodule_test.utils import DeveloperError


class FakePackageCreator:
    def __init__(self, dist_folder=None):
        self.dist_folder = dist_folder or settings.DIST_FOLDER
        if not os.path.exists(self.dist_folder):
            os.makedirs(self.dist_folder, exist_ok=True)

    def service_dir(self, service):
        return os.path.join(self.dist_folder, "_".join(service.replace("_", "-").rsplit("-", 1)))

    @staticmethod
    def _create_revision(path, revision):
        if revision:
            with open(os.path.join(path, "revision"), "w") as file:
                file.write(str(revision))

    def create_om_service(self, service_name, env_kwargs, yml=""):
        if not service_name.startswith("om"):
            raise DeveloperError(f"Openmodule services always start with om, invalid service name: {service_name}")
        path = self.service_dir(service_name)
        if os.path.exists(path):
            raise DeveloperError(f"Path {path} already exists")
        else:
            os.makedirs(path)
            self._create_revision(path, 1)
            with open(os.path.join(path, "yml"), "w") as file:
                file.write(yml)
            with open(os.path.join(path, "env"), "w") as file:
                file.write(f"NAME={service_name.replace('-', '_')}\n")
                for key, value in env_kwargs.items():
                    if key.upper() != "NAME":
                        file.write(f"{key.upper()}={value}\n")

    def create_hw_service(self, service_name, env_kwargs, ip, additional_yml_kwargs: Optional[Dict] = None):
        if not service_name.startswith("hw"):
            raise DeveloperError(f"Hardware services always start with hw, invalid service name: {service_name}")
        path = self.service_dir(service_name)
        if os.path.exists(path):
            raise DeveloperError(f"Path {path} already exists")
        else:
            os.makedirs(path)
            self._create_revision(path, 1)
            with open(os.path.join(path, "yml"), "w") as file:
                yml_dict = dict(ip=ip, network=dict(addresses=[f"{ip}/24"], dhcp=False,
                                                    gateway=".".join([ip.rsplit(".", 1)[0], "1"]),
                                                    nameservers=["8.8.8.8", ["1.1.1.1"]],
                                                    ntp_servers=[]))
                if additional_yml_kwargs:
                    yml_dict.update(additional_yml_kwargs)
                file.write(yaml.dump(yml_dict))
            with open(os.path.join(path, "env"), "w") as file:
                file.write(f"NAME={service_name.replace('-', '_')}\n")
                for key, value in env_kwargs.items():
                    if key.upper() != "NAME":
                        file.write(f"{key.upper()}={value}\n")

    def create_service(self, service_name, env: Optional[str] = "", yml: Optional[str] = "",
                       revision: Optional[int] = 1):
        path = self.service_dir(service_name)
        if os.path.exists(path):
            raise DeveloperError(f"Path {path} already exists")
        else:
            os.makedirs(path)
            if revision is not None:
                self._create_revision(path, revision)
            if yml is not None:
                with open(os.path.join(path, "yml"), "w") as file:
                    file.write(yml)
            if env is not None:
                with open(os.path.join(path, "env"), "w") as file:
                    file.write(env)

    def clean_dist_folder(self):
        try:
            shutil.rmtree(self.dist_folder)
        except Exception:
            pass
