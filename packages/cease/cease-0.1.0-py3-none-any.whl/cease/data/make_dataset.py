from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from cease import logger


class DatasetMaker:
    def __init__(self, dataset_name, config_builder):
        self.dataset_name = dataset_name
        self.config_builder = config_builder
        self.config = config_builder.get_config()
        logger.info(f"DatasetMaker initialized for {self.dataset_name}")

    def save_data(self, data):
        decision = self.config.get("decision")
        if not decision:
            raise ValueError("Decision not found in config")

        output_dir = self.config.get("output_dir")
        if not output_dir:
            raise ValueError("Output dir not found in config")
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_dir = str(output_dir)
        logger.info(f"Saving data to {output_dir}")

        X = data.drop([decision], axis=1)
        Y = data[decision]
        X_train, X_holdout, y_train, y_holdout = train_test_split(
            X, Y, test_size=0.33, random_state=42, stratify=data[decision]
        )
        X_test, X_attack, y_test, y_attack = train_test_split(
            X, Y, test_size=0.33, random_state=42, stratify=data[decision]
        )
        X_train = self.encode_categorical_features(X_train)
        X_attack = self.encode_categorical_features(X_holdout)
        X_test = self.encode_categorical_features(X_test)

        X_train = pd.DataFrame(self.apply_standard_scalar(X_train), columns=X.columns)
        X_test = pd.DataFrame(self.apply_standard_scalar(X_test), columns=X.columns)
        X_attack = pd.DataFrame(self.apply_standard_scalar(X_attack), columns=X.columns)

        train_file_path = f"{output_dir}/train.csv"
        test_file_path = f"{output_dir}/test.csv"
        attack_file_path = f"{output_dir}/attack.csv"
        train_labels_file_path = f"{output_dir}/train_labels.csv"
        test_labels_file_path = f"{output_dir}/test_labels.csv"
        attack_labels_file_path = f"{output_dir}/attack_labels.csv"

        X_train.to_csv(train_file_path, index=False)
        X_test.to_csv(test_file_path, index=False)
        X_attack.to_csv(attack_file_path, index=False)
        y_train.to_csv(train_labels_file_path, index=False)
        y_test.to_csv(test_labels_file_path, index=False)
        y_attack.to_csv(attack_labels_file_path, index=False)

        self.config["train_file_path"] = train_file_path
        self.config["test_file_path"] = test_file_path
        self.config["attack_file_path"] = attack_file_path
        self.config["train_labels_file_path"] = train_labels_file_path
        self.config["test_labels_file_path"] = test_labels_file_path
        self.config["attack_labels_file_path"] = attack_labels_file_path

        self.config_builder.update_config(self.config)

        return (
            train_file_path,
            test_file_path,
            attack_file_path,
            train_labels_file_path,
            test_labels_file_path,
            attack_labels_file_path,
        )

    def apply_standard_scalar(self, df):
        artifacts_dir = self.config.get("artifacts_dir")
        artifacts_dir = Path(artifacts_dir)
        if not artifacts_dir.exists():
            raise ValueError("Artifacts dir not found")
        if (artifacts_dir / "standard_scaler.pkl").exists():
            scaler = joblib.load(str(artifacts_dir / "standard_scaler.pkl"))
        else:
            scaler = StandardScaler()
            scaler.fit(df)
            joblib.dump(scaler, str(artifacts_dir / "standard_scaler.pkl"))
        return scaler.transform(df)

    def encode_categorical_features(self, df):

        artifacts_dir = self.config.get("artifacts_dir")
        logger.info(f"Artifacts dir: {self.config}")
        artifacts_dir = Path(artifacts_dir)
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        categorical = self.config.get("categorical_features")
        if not categorical:
            raise ValueError("categorical_features not found in config")
        logger.info(f"Categorical: {categorical}")
        for feature in categorical:
            feature_encoder = artifacts_dir / f"{feature}_encoder.pkl"
            if not feature_encoder.exists():
                le = preprocessing.LabelEncoder()
                le.fit(df[feature])
                joblib.dump(le, str(feature_encoder))
            else:
                le = joblib.load(str(feature_encoder))
            df[feature] = le.transform(df[feature])
        return df

    def prepare_pretrain_data(self):
        logger.info(f"Preparing pretrain data for {self.dataset_name}")
        train_file_path = Path(self.config["train_file_path"])
        test_file_path = Path(self.config["test_file_path"])
        attack_file_path = Path(self.config["attack_file_path"])
        train_labels_file_path = Path(self.config["train_labels_file_path"])
        test_labels_file_path = Path(self.config["test_labels_file_path"])
        attack_labels_file_path = Path(self.config["attack_labels_file_path"])

        X_train = pd.read_csv(train_file_path)
        X_test = pd.read_csv(test_file_path)
        X_attack = pd.read_csv(attack_file_path)
        y_train = pd.read_csv(train_labels_file_path)
        y_test = pd.read_csv(test_labels_file_path)
        y_attack = pd.read_csv(attack_labels_file_path)

        return X_train, X_test, X_attack, y_train, y_test, y_attack


class AdultIncomeDatasetMaker(DatasetMaker):
    def __init__(self, dataset_name, config_builder):
        super().__init__(dataset_name, config_builder)

    def make_dataset(self):
        raw_data_train = np.genfromtxt(
            f'{self.config["path"]}/{self.config["train"]}', delimiter=", ", dtype=str
        )

        df = pd.DataFrame(raw_data_train, columns=self.config["features"])

        logger.info(
            f"Dataset {self.dataset_name} created from {self.config['train']} with columns {df.columns}"
        )

        df = self.process(df)
        return df

    def transform(self, df):
        df = self.process(df)
        df = self.encode_categorical_features(df)
        labels = [None for _ in range(len(df))]
        if "income" in df.columns:
            labels = df.pop("income")
        logger.info(f"Dataset {self.dataset_name} columns: {df.columns}")
        df = self.apply_standard_scalar(df)
        return df, labels

    def process(self, df):
        logger.info(f"Processing dataset {self.dataset_name}...")
        df = df.astype(
            {
                "age": np.int64,
                "educational-num": np.int64,
                "hours-per-week": np.int64,
                "capital-gain": np.int64,
                "capital-loss": np.int64,
            }
        )

        df = df.replace(
            {
                "workclass": {
                    "Without-pay": "Other/Unknown",
                    "Never-worked": "Other/Unknown",
                }
            }
        )
        df = df.replace(
            {
                "workclass": {
                    "Federal-gov": "Government",
                    "State-gov": "Government",
                    "Local-gov": "Government",
                }
            }
        )
        df = df.replace(
            {
                "workclass": {
                    "Self-emp-not-inc": "Self-Employed",
                    "Self-emp-inc": "Self-Employed",
                }
            }
        )
        df = df.replace(
            {
                "workclass": {
                    "Never-worked": "Self-Employed",
                    "Without-pay": "Self-Employed",
                }
            }
        )
        df = df.replace({"workclass": {"?": "Other/Unknown"}})

        df = df.replace(
            {
                "occupation": {
                    "Adm-clerical": "White-Collar",
                    "Craft-repair": "Blue-Collar",
                    "Exec-managerial": "White-Collar",
                    "Farming-fishing": "Blue-Collar",
                    "Handlers-cleaners": "Blue-Collar",
                    "Machine-op-inspct": "Blue-Collar",
                    "Other-service": "Service",
                    "Priv-house-serv": "Service",
                    "Prof-specialty": "Professional",
                    "Protective-serv": "Service",
                    "Tech-support": "Service",
                    "Transport-moving": "Blue-Collar",
                    "Unknown": "Other/Unknown",
                    "Armed-Forces": "Other/Unknown",
                    "?": "Other/Unknown",
                }
            }
        )

        df = df.replace(
            {
                "marital-status": {
                    "Married-civ-spouse": "Married",
                    "Married-AF-spouse": "Married",
                    "Married-spouse-absent": "Married",
                    "Never-married": "Single",
                }
            }
        )

        df = df.replace(
            {
                "race": {
                    "Black": "Black",
                    "Asian-Pac-Islander": "Asian-Pac-Islander",
                    "Amer-Indian-Eskimo": "Amer-Indian-Eskimo",
                }
            }
        )

        df = df[
            [
                "age",
                "workclass",
                "education",
                "marital-status",
                "relationship",
                "occupation",
                "race",
                "gender",
                "capital-gain",
                "capital-loss",
                "hours-per-week",
                "income",
            ]
        ]

        df = df.replace({"income": {"<=50K": 0, "<=50K.": 0, ">50K": 1, ">50K.": 1}})

        df = df.replace(
            {
                "education": {
                    "Assoc-voc": "Assoc",
                    "Assoc-acdm": "Assoc",
                    "11th": "School",
                    "10th": "School",
                    "7th-8th": "School",
                    "9th": "School",
                    "12th": "School",
                    "5th-6th": "School",
                    "1st-4th": "School",
                    "Preschool": "School",
                }
            }
        )

        df = df.rename(
            columns={
                "marital-status": "marital_status",
                "hours-per-week": "hours_per_week",
                "capital-gain": "capital_gain",
                "capital-loss": "capital_loss",
            }
        )

        return df
