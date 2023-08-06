import json
import logging
import os
from typing import Dict, Optional

import yaml
from dotenv import dotenv_values

from openmodule.config import settings
from openmodule.models.base import OpenModuleModel


class BaseSetting(OpenModuleModel):
    env: Dict
    yml: Dict


class ServiceSetting(BaseSetting):
    parent: Optional[BaseSetting]


class PackageReader:
    def __init__(self, dist_folder: Optional[str] = None, yaml_loader=None):
        self.dist_folder = settings.DIST_FOLDER if dist_folder is None else dist_folder
        self.yaml_loader = yaml_loader or yaml.FullLoader
        self.log = logging.getLogger("PackageReader")

    def service_dir(self, service):
        return os.path.join(self.dist_folder, "_".join(service.replace("_", "-").rsplit("-", 1)))

    def _load_env(self, path):
        path = os.path.join(path, "env")
        if os.path.exists(path):
            try:
                res = dotenv_values(path)
                return res
            except Exception:
                self.log.error(f"ENV file {path} could not be read")
        else:
            self.log.warning(f"ENV file {path} does not exist")
        return {}

    def _load_yml(self, path):
        path = os.path.join(path, "yml")
        if os.path.exists(path):
            try:
                with open(path, "r") as file:
                    res = yaml.load(file, Loader=self.yaml_loader)
                    # load returns None on empty file, str on some invalid files
                    if not isinstance(res, dict):
                        self.log.error(f"YML file {path} could not be read")
                        return {}
                    return res
            except Exception:
                self.log.error(f"YML file {path} could not be read")
        return {}

    def _get_services(self, prefix=""):
        if not os.path.exists(self.dist_folder):
            self.log.warning(f"Dist folder {self.dist_folder} does not exist")
            return []
        services = [x.replace("-", "_") for x in os.listdir(self.dist_folder)]
        if prefix:
            prefix = prefix.replace("-", "_")
            services = [x for x in services if x.startswith(prefix)]
        return services

    def installed_services(self, prefix=""):
        """Check all installed services in the dist folder which have a valid revision file
          Args:
            prefix (str): Prefix for the service, empty string means no prefix, load all
        Returns:
            List of service names
        """
        services = self._get_services(prefix)
        result = []
        # check revision file
        for service in services:
            path = self.service_dir(service)
            # Check if valid service exists
            if os.path.exists(path) and os.path.exists(os.path.join(path, "revision")):
                result.append(service)
        return result

    def load_setting(self, service, with_parent=False) -> Optional[ServiceSetting]:
        """ Loads the settings of the specified service,
       Args:
           service (str): Service name
           with_parent (bool): attach parent services to the settings of their children
       Returns:
           ServiceSetting of the service if the service exists (directory + revision file) else None
       """
        path = self.service_dir(service)
        # Check if valid service exists
        if os.path.exists(path) and os.path.exists(os.path.join(path, "revision")):
            result = dict(yml=self._load_yml(path), env=self._load_env(path))
            if with_parent and result["env"].get("PARENT"):
                result["parent"] = self.load_setting(result["env"]["PARENT"])
            return ServiceSetting(**result)
        else:
            return None

    def load_with_service_prefix(self, prefix="", with_parent=False) -> Dict[str, ServiceSetting]:
        """ Loads all service settings of services that start with the given prefix
        Args:
            prefix (str): Prefix for the service, empty string means no prefix, load all
            with_parent (bool): attach parent services to the settings of their children
        Returns:
            Dict of service names and their ServiceSetting
        """

        services = self._get_services(prefix)
        result = dict()
        for service in services:
            if service not in result:
                setting = self.load_setting(service, with_parent)
                if setting:
                    result[service] = setting
                    if result[service].parent:
                        result[service].parent.env["NAME"] = result[service].parent
        return result

    def load_with_hardware_type_prefix(self, hw_type_prefix):
        """ Loads all service settings of services that have at least on hardware type starting with the
            given hardware type prefix
        Args:
            hw_type_prefix (str): Prefix for the hardware type of the service
        Returns:
            Dict of service names and their ServiceSetting which match the hardware type prefix it is given, else None
        """
        if not hw_type_prefix:
            return {}
        result = dict()
        services = self.load_with_service_prefix("hw")
        for key, setting in services.items():
            if setting.env.get("HARDWARE_TYPE", "") and \
                    any(x.startswith(hw_type_prefix) for x in json.loads(setting.env["HARDWARE_TYPE"])):
                result[key] = setting
        return result

    def load_with_parent_type_prefix(self, parent_type_prefix, with_parent=False):
        """ Loads all service settings of services that have at least on parent type starting with the
            given parent type prefix
        Args:
            parent_type_prefix (str): Prefix for the parent type of the service
            with_parent (bool): attach parent services to the settings of their children
        Returns:
            Dict of service names and their ServiceSetting with match the parent type prefix if it is given, else None

        """
        if not parent_type_prefix:
            return {}
        services = self.load_with_service_prefix("om", with_parent=with_parent)
        result = dict()
        for key, setting in services.items():
            if setting.env.get("PARENT_TYPE", "") and \
                    any(x.startswith(parent_type_prefix) for x in json.loads(setting.env["PARENT_TYPE"])):
                result[key] = setting
        return result


def is_bridged_slave():
    """ Checks if the current NUC is a bridged slave
    Returns:
        True if bridge slave, False if bridged master, None if not bridged or error
    """

    try:
        if settings.BRIDGED_SLAVE is not None:
            return settings.BRIDGED_SLAVE
    except AttributeError:
        pass

    reader = PackageReader(settings.DIST_FOLDER)
    services = reader.load_with_service_prefix("om-service-bridge")
    
    if len(services) > 1:
        reader.log.error("Multiple bridges are installed", extra=dict(bridges=list(services.keys())))
        return None
    elif services:
        bridge = next((v for v in services.values()), None)
        return bool(bridge.env.get("MASTER"))
    else:
        return None
