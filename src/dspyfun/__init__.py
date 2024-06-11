# dspyfun/__init__.py
from pathlib import Path
from confz import BaseConfig, FileSource

from pydantic import BaseModel
from dspyfun.utils.path_tools import config_dir


class DspyfunConfig(BaseConfig):
    cluster_name: str
    zone: str
    project_id: str

    CONFIG_SOURCES = FileSource(file=config_dir() / "dspyfun_config.yaml")


def load_config() -> DspyfunConfig:
    return DspyfunConfig()


config = load_config()
