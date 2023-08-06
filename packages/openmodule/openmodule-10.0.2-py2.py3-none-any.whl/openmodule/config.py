import builtins
import functools
import importlib.util
import inspect
import logging
import os
import warnings
from contextlib import contextmanager
from socket import gethostname
from typing import Optional, Type, TypeVar

import yaml
from pydantic import ValidationError
from pydantic.main import BaseModel


def _save_cast(obj, key, to_type, default):
    try:
        return to_type(obj[key])
    except (ValueError, TypeError, KeyError):
        return default


def int(key: str, default: int = 0) -> int:
    assert isinstance(default, (builtins.int,)), "default argument must be of type int"
    return _save_cast(os.environ, key, builtins.int, builtins.int(default))


def float(key: str, default: float = 0.0) -> float:
    assert isinstance(default, (builtins.int, builtins.float)), "default argument must be of type int or float"
    return _save_cast(os.environ, key, builtins.float, builtins.float(default))


def string(key: str, default: str = "") -> str:
    assert isinstance(default, str), "default argument must be of type string"
    res = os.environ.get(key, default)
    invalid_chars = "\"' \r\n\t"
    res = res.strip(invalid_chars)
    return res


def bool(key: str, default: bool = False) -> bool:
    assert isinstance(default, builtins.bool), "default argument must be of type bool"
    val = get(key) or ""
    val = val.upper().strip('\'" .,;-_')
    if not val:
        return default
    return val in ["T", "TRUE", "1", "Y", "YES", "J", "JA", "ON"]


def get(key: str, default: Optional[str] = "") -> str:
    return os.environ.get(key, default)


_inside_docker_cached = None


def _inside_docker():
    global _inside_docker_cached
    if _inside_docker_cached is not None:
        return _inside_docker_cached
    else:
        if os.path.exists('/.dockerenv'):
            _inside_docker_cached = True
            return _inside_docker_cached

        path = '/proc/self/cgroup'
        if os.path.isfile(path):
            with open(path, "r") as f:
                _inside_docker_cached = any('docker' in line for line in f)
        else:
            _inside_docker_cached = False

        return _inside_docker_cached


def debug():
    if "DEBUG" in os.environ:
        return bool("DEBUG", default=False)
    elif testing():
        return False
    else:
        return version() == "unknown" and not _inside_docker()


def bridged_slave():
    if "BRIDGED_SLAVE" in os.environ:
        return bool("BRIDGED_SLAVE", default=False)
    else:
        return None


def dist_folder():
    if testing():
        return string("DIST_FOLDER", "../tests/dist2")
    elif debug():
        return string("DIST_FOLDER", "../dist2")
    else:
        return string("DIST_FOLDER", "/opt/openmodule/dist2")


def settings_module():
    if testing() and os.path.exists("../tests/config.py"):
        return string("SETTINGS_MODULE", "tests.config")
    return string("SETTINGS_MODULE", "config")


def log_level() -> int:
    log_levels = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "VERBOSE": logging.DEBUG,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "ERR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "CRIT": logging.CRITICAL,
        "FATAL": logging.FATAL
    }
    default_log_level = logging.DEBUG if debug() else logging.INFO
    return log_levels.get(os.environ.get("LOG_LEVEL", "").upper(), default_log_level)


def version() -> str:
    version = string("VERSION", "")
    if not version:
        if os.path.isfile("VERSION"):
            with open("VERSION", "r") as f:
                version = f.read()
    if not version:
        version = "unknown"
    return version.strip("\r\n\t ")


def resource() -> str:
    resource = string("AUTH_RESOURCE", "")
    if not resource:
        # in test mode we allow using hostname, to make sure that the CI execution (docker) behaves like the local
        if testing() or not _inside_docker():
            resource = gethostname()
    return resource


def broker_pub(default: str = "tcp://127.0.0.1:10200") -> str:
    broker_host = string("BROKER_HOST", "")
    broker_pub_port = int("BROKER_PUB_PORT", 10200)
    broker_pub = string("BROKER_PUB", "")

    if broker_pub:
        return broker_pub
    elif broker_host and broker_pub_port:
        # use legacy configs
        return "tcp://{}:{}".format(broker_host, broker_pub_port)
    else:
        return default


def broker_sub(default: str = "tcp://127.0.0.1:10100") -> str:
    broker_host = string("BROKER_HOST", "")
    broker_sub_port = int("BROKER_SUB_PORT", 10100)
    broker_sub = string("BROKER_SUB", "")

    if broker_sub:
        return broker_sub
    elif broker_host and broker_sub_port:
        # use legacy configs
        return "tcp://{}:{}".format(broker_host, broker_sub_port)
    else:
        return default


def validate_config_module(config):
    required_keys = ["NAME", "RESOURCE", "VERSION", "DEBUG", "TESTING"]
    for x in required_keys:
        assert hasattr(config, x), f"the config module requires the variable {x}"

    if hasattr(config, "BROKER_PUB_PORT") or hasattr(config, "BROKER_SUB_PORT"):
        warnings.warn(
            "BROKER_(P/S)UB_PORT and BROKER_HOST are to be replaced with BROKER_(P/S)UB. In order to \n"
            "remain backwards compatible, you can use BROKER_PUB = config.broker_pub() which correctly \n"
            "interprets the deprecated environment variables",
            DeprecationWarning
        )


class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
    def ignore_unknown(self, node):
        return None


SafeLoaderIgnoreUnknown.add_constructor(None, SafeLoaderIgnoreUnknown.ignore_unknown)

YamlType = TypeVar("YamlType", bound=BaseModel)


def config_yaml_path():
    yaml_path = string("CONFIG_YAML", "")
    if not yaml_path:
        if debug():
            yaml_path = "../settings/default-debug.yml"
        elif testing():
            yaml_path = "../settings/default-testing.yml"
        else:
            yaml_path = "/data/config.yml"
    return yaml_path


def yaml(model: Type[YamlType], path: str = None) -> YamlType:
    yaml_path = path or config_yaml_path()
    try:
        if os.path.exists(yaml_path):
            import yaml
            with open(yaml_path, "r") as f:
                a = yaml.load(f, SafeLoaderIgnoreUnknown)
                return model.parse_obj(a or {})
        else:
            return model()
    except ValidationError as e:
        logging.exception("error during config yaml loading, something is wrong with the configuration")
        raise e from None


def testing():
    return bool("TESTING", False)


def database_folder() -> str:
    path = string("DATABASE_FOLDER", f"/data/sqlite/")
    if testing():
        path = "../sqlite/test/"
    elif debug():
        path = "../sqlite/debug/"
    return path


def run_checks() -> bool:
    return debug() or testing()


empty = object()


def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)

    return inner


def unpickle_lazyobject(wrapped):
    return wrapped


class LazyObject:
    _wrapped = None

    def __init__(self):
        self._wrapped = empty

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        assert name != "_wrapped", "can't delete _wrapped"
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)


class Settings:
    def __init__(self, lazy_setting, settings_module):
        self._explicit_settings = set()

        # update this dict from global settings (but only for ALL_CAPS settings)
        options = dict()
        for setting in dir(GlobalSettings):
            if not setting.startswith("_") and setting.isupper():
                options[setting] = getattr(GlobalSettings, setting)
                setattr(self, setting, options[setting])

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module
        if settings_module:
            for setting in dir(settings_module):
                if setting.isupper():
                    setting_value = getattr(settings_module, setting)
                    options[setting] = setting_value
                    setattr(self, setting, setting_value)

        override = _override_settings.set_base(lazy_setting, options)
        for k, v in override.items():
            setattr(self, k, v)
            self._explicit_settings.add(k)

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }


class LazySettings(LazyObject):
    _settings_module = None
    _is_configured = False

    def __init__(self):
        super().__init__()

    def _setup(self):
        module_name = settings_module()
        module = importlib.import_module(module_name)
        self._wrapped = Settings(self, module)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is empty:
            return '<LazySettings [Unevaluated]>'
        return '<LazySettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }

    def __getattr__(self, name):
        """Return the value of a setting and cache it in self.__dict__."""
        if name == "_is_configured":
            return self._is_configured
        if self._wrapped is empty:
            self._setup()
        val = getattr(self._wrapped, name)
        self.__dict__[name] = val
        return val

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete a setting and clear it from cache if needed."""
        super().__delattr__(name)
        self.__dict__.pop(name, None)

    def configure(self, settings_module):
        assert self._wrapped is empty, 'Settings are already configured'
        self._wrapped = Settings(self, settings_module)

    def reset(self):
        self._wrapped = empty
        _override_settings.clear_all()

    def override(self, **options):
        _override_settings.override(**options)

    def clear_override(self, **options):
        _override_settings.clear_override(**options)


class OverrideSettings:
    lazy_setting = None

    def __init__(self):
        self.overrides = dict()

    def clear_all(self):
        self.lazy_setting = None
        self.overrides = dict()

    def override(self, **options):
        for k, v in options.items():
            if self.overrides.get(k):
                self.overrides[k].append(v)
            else:
                self.overrides[k] = [v]
            if self.lazy_setting is not None:
                setattr(self.lazy_setting, k, v)
                self.lazy_setting._wrapped._explicit_settings.add(k)

    def clear_override(self, **options):
        for k in options.keys():
            if self.overrides.get(k):
                self.overrides[k].pop()
                if self.lazy_setting is not None:
                    if len(self.overrides[k]) == 1:
                        self.lazy_setting._wrapped._explicit_settings.remove(k)

                    if len(self.overrides[k]) == 0:
                        # deletes the attribute if it never existed in the base config in the first place
                        delattr(self.lazy_setting, k)
                    else:
                        setattr(self.lazy_setting, k, self.overrides[k][-1])

    def set_base(self, lazy_setting, options):
        assert self.lazy_setting is None, "Do not use multiple settings"
        self.lazy_setting = lazy_setting
        overrides = {}
        for k, v in options.items():
            if self.overrides.get(k):
                overrides[k] = self.overrides[k][-1]
                self.overrides[k].insert(0, v)
            else:
                self.overrides[k] = [v]
        return overrides


@contextmanager
def override_context(**options):
    settings.override(**options)
    yield
    settings.clear_override(**options)


def override_settings(**options):
    def decorator(x):
        if inspect.isclass(x):
            original_run = x.run

            def new_run(inner_self, result=None):
                with override_context(**options):
                    original_run(inner_self, result)

            x.run = new_run
            return x
        elif callable(x):
            @functools.wraps(x)
            def wrapper(*args, **kwargs):
                with override_context(**options):
                    x(*args, **kwargs)

            return wrapper

    return decorator


class GlobalSettings:
    # usual
    NAME = string("NAME", "om_dev_unnamed_1")
    VERSION = version()
    RESOURCE = resource()
    DEBUG = debug()
    TESTING = testing()
    LOG_LEVEL = log_level()
    DATABASE_FOLDER = database_folder()

    # broker env vars
    BROKER_SUB = broker_sub()
    BROKER_PUB = broker_pub()

    LOCAL_DEVELOPMENT = bool("LOCAL_DEVELOPMENT", False)
    BRIDGED_SLAVE = bridged_slave()
    DIST_FOLDER = dist_folder()


settings = LazySettings()
_override_settings = OverrideSettings()
