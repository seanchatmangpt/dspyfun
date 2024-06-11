# dspyfun/config_manager.py
import yaml
from pydantic import BaseModel
from dspyfun import DspyfunConfig
from dspyfun.utils.path_tools import config_dir


class ConfigManager:
    def __init__(self):
        self.config = DspyfunConfig()

    def update_config(self, **kwargs):
        # Convert the frozen pydantic model to a dictionary
        config_dict = self.config.model_dump()

        # Update the dictionary with new values
        for key, value in kwargs.items():
            if key in config_dict:
                config_dict[key] = value

        # Create a new config instance
        self.config = DspyfunConfig(**config_dict)

        # Save the updated config to the YAML file
        self.save_config()

    def save_config(self):
        config_path = config_dir() / "dspyfun_config.yaml"
        with open(config_path, 'w') as file:
            yaml.dump(self.config.model_dump(), file)


config_manager = ConfigManager()
