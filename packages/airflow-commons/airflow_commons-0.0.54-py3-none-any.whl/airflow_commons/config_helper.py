from codecs import open as codec_open
import yaml


def read_config(config_file: str):
    """
    Reads config from a configuration file and returns a config dictionary

    :param config_file: relative location of config file
    :return: configs as dictionary
    """
    stream = codec_open(config_file, "r")
    return yaml.safe_load(stream)
