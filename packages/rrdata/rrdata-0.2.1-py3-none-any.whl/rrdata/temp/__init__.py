# -*- coding: utf-8 -*-
import importlib
import json
import logging
import os
import pkgutil
import pprint
from logging.handlers import RotatingFileHandler

import pandas as pd
import pkg_resources
from pkg_resources import get_distribution, DistributionNotFound

from rrdata.rrdatad import index
from rrdata.rrdatad import stock

from rrdata.consts import DATA_SAMPLE_ZIP_PATH,  RRSDK_HOME

"""
try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
"""
logger = logging.getLogger(__name__)


def init_log(file_name="rrsdk.log", log_dir=None, simple_formatter=True):
    if not log_dir:
        log_dir = rrsdk_env["log_path"]

    root_logger = logging.getLogger()

    # reset the handlers
    root_logger.handlers = []

    root_logger.setLevel(logging.INFO)

    file_name = os.path.join(log_dir, file_name)

    file_log_handler = RotatingFileHandler(file_name, maxBytes=524288000, backupCount=10)

    file_log_handler.setLevel(logging.INFO)

    console_log_handler = logging.StreamHandler()
    console_log_handler.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    if simple_formatter:
        formatter = logging.Formatter("%(asctime)s  %(levelname)s  %(threadName)s  %(message)s")
    else:
        formatter = logging.Formatter(
            "%(asctime)s  %(levelname)s  %(threadName)s  %(name)s:%(filename)s:%(lineno)s  %(funcName)s  %(message)s"
        )
    file_log_handler.setFormatter(formatter)
    console_log_handler.setFormatter(formatter)

    # add the handlers to the logger
    root_logger.addHandler(file_log_handler)
    root_logger.addHandler(console_log_handler)


os.environ.setdefault("SQLALCHEMY_WARN_20", "1")
pd.set_option("expand_frame_repr", False)
pd.set_option("mode.chained_assignment", "raise")
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

rrsdk_env = {}

rrsdk_config = {}

_plugins = {}


def init_env(rrsdk_home: str, **kwargs) -> dict:
    """
    init env
    :param rrsdk_home: home path for rrsdk
    """
    data_path = os.path.join(rrsdk_home, "data")
    tmp_path = os.path.join(rrsdk_home, "tmp")
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    rrsdk_env["rrsdk_home"] = rrsdk_home
    rrsdk_env["data_path"] = data_path
    rrsdk_env["tmp_path"] = tmp_path

    # path for storing ui results
    rrsdk_env["ui_path"] = os.path.join(rrsdk_home, "ui")
    if not os.path.exists(rrsdk_env["ui_path"]):
        os.makedirs(rrsdk_env["ui_path"])

    # path for storing logs
    rrsdk_env["log_path"] = os.path.join(rrsdk_home, "logs")
    if not os.path.exists(rrsdk_env["log_path"]):
        os.makedirs(rrsdk_env["log_path"])

    init_log()

    pprint.pprint(rrsdk_env)

    # init config
    init_config(current_config=rrsdk_config, **kwargs)
    # init plugin
    # init_plugins()

    return rrsdk_env


def init_config(pkg_name: str = None, current_config: dict = None, **kwargs) -> dict:
    """
    init config
    """

    # create default config.json if not exist
    if pkg_name:
        config_file = f"{pkg_name}_config.json"
    else:
        pkg_name = "rrsdk"
        config_file = "config.json"

    logger.info(f"init config for {pkg_name}, current_config:{current_config}")

    config_path = os.path.join(rrsdk_env["rrsdk_home"], config_file)
    if not os.path.exists(config_path):
        from shutil import copyfile

        try:
            sample_config = pkg_resources.resource_filename(pkg_name, "config.json")
            if os.path.exists(sample_config):
                copyfile(sample_config, config_path)
        except Exception as e:
            logger.warning(f"could not load config.json from package {pkg_name}")

    if os.path.exists(config_path):
        with open(config_path) as f:
            config_json = json.load(f)
            for k in config_json:
                current_config[k] = config_json[k]

    # set and save the config
    for k in kwargs:
        current_config[k] = kwargs[k]
        with open(config_path, "w+") as outfile:
            json.dump(current_config, outfile)

    pprint.pprint(current_config)
    logger.info(f"current_config:{current_config}")

    return current_config


def init_plugins():
    for finder, name, ispkg in pkgutil.iter_modules():
        if name.startswith("rrsdk_"):
            try:
                _plugins[name] = importlib.import_module(name)
            except Exception as e:
                logger.warning(f"failed to load plugin {name}", e)
    logger.info(f"loaded plugins:{_plugins}")



#init_env(rrsdk_home=RRSDK_HOME)

# register to meta
#import rrdata.contract as rrdata_contract
#import rrdata.recorders as rrdata_recorders
#import rrdata.factors as rrdata_factors

#__all__ = ["rrsdk_env", "rrsdk_config", "init_log", "init_env", "init_config"] #, "__version__"]