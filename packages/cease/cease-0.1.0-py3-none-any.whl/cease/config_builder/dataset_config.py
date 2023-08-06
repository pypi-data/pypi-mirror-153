import json
from pathlib import Path

from cease import logger


class ConfigBuilder:
    def __init__(self, config_file_path, dataset):
        self.config_file_path = Path(config_file_path)
        self.config = json.load(self.config_file_path.open())
        self.dataset_name = dataset
        logger.info(f"Config file loaded: {self.config_file_path}")

    def save(self):
        with self.config_file_path.open("w") as f:
            json.dump(self.config, f, indent=8)
        logger.info(f"Config file saved: {self.config_file_path}")


class DatasetConfigBuilder(ConfigBuilder):
    def __init__(self, config_file_path, dataset):
        super().__init__(config_file_path, dataset)

    def get_config(self):
        config = self.config[self.dataset_name]["dataset_config"]
        logger.info(f"Dataset config loaded: {config}")
        return config

    def update_config(self, config):
        self.config[self.dataset_name]["dataset_config"] = config
        logger.info(f"Dataset config updated: {config}")
        self.save()


class ModelConfigBuilder(ConfigBuilder):
    def __init__(self, config_file_path, dataset):
        super().__init__(config_file_path, dataset)

    def populate_files_from_dataset_config(self):
        if self.dataset_name not in self.config:
            logger.error(f"Dataset {self.dataset_name} not found in config file")
            return

        dataset_config = self.config[self.dataset_name]["dataset_config"]
        self.config[self.dataset_name]["model_config"][
            "test_file_path"
        ] = dataset_config["test_file_path"]
        self.config[self.dataset_name]["model_config"][
            "train_file_path"
        ] = dataset_config["train_file_path"]
        self.config[self.dataset_name]["model_config"][
            "attack_file_path"
        ] = dataset_config["attack_file_path"]
        self.config[self.dataset_name]["model_config"][
            "train_labels_file_path"
        ] = dataset_config["train_labels_file_path"]
        self.config[self.dataset_name]["model_config"][
            "test_labels_file_path"
        ] = dataset_config["test_labels_file_path"]
        self.config[self.dataset_name]["model_config"][
            "attack_labels_file_path"
        ] = dataset_config["attack_labels_file_path"]

        logger.info(f"Model config updated: {self.config}")
        self.save()

    def get_config(self):
        config = self.config[self.dataset_name]["model_config"]
        self.populate_files_from_dataset_config()
        logger.info(f"Model config loaded: {config}")
        return config

    def update_config(self, config):
        self.config[self.dataset_name]["model_config"] = config
        logger.info(f"Model config updated: {config}")
        self.save()
