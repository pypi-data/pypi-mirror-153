import json
import pickle
import warnings
from datetime import datetime
from pathlib import Path

from hpsklearn import (
    HyperoptEstimator,
    ada_boost_classifier,
    any_classifier,
    bagging_classifier,
    decision_tree_classifier,
    extra_trees_classifier,
    forest_classifiers,
    gradient_boosting_classifier,
    k_neighbors_classifier,
    lightgbm_classification,
    mlp_classifier,
    one_vs_one_classifier,
    one_vs_rest_classifier,
    output_code_classifier,
    passive_aggressive_classifier,
    random_forest_classifier,
    sgd_classifier,
    xgboost_classification,
)
from hyperopt import tpe

from cease import logger

warnings.filterwarnings("ignore")


class HyperOptTrainer:
    def __init__(self, config_builder, X_train, y_train, X_test, y_test):
        self.config_builder = config_builder
        self.config = config_builder.get_config()
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.classifiers = self.config.get("classifiers", ["xgboost"])
        self.max_evals = self.config.get("max_evals", 10)
        self.trial_timeout = self.config.get("trial_timeout", 120)
        self.models_dir = Path(
            self.config.get("models_dir", f"models/{self.config_builder.dataset_name}")
        )
        self.models_dir.mkdir(exist_ok=True)

    def _get_classifer(self, classifier_name):
        if classifier_name == "XGBClassifier":
            return xgboost_classification
        elif classifier_name == "RandomForestClassifier":
            return random_forest_classifier
        elif classifier_name == "ExtraTreesClassifier":
            return extra_trees_classifier
        elif classifier_name == "AdaBoostClassifier":
            return ada_boost_classifier
        elif classifier_name == "BaggingClassifier":
            return bagging_classifier
        elif classifier_name == "GradientBoostingClassifier":
            return gradient_boosting_classifier
        elif classifier_name == "LightGBMClassifier":
            return lightgbm_classification
        elif classifier_name == "MLPClassifier":
            return mlp_classifier
        elif classifier_name == "PassiveAggressiveClassifier":
            return passive_aggressive_classifier
        elif classifier_name == "SGDClassifier":
            return sgd_classifier
        elif classifier_name == "DecisionTreeClassifier":
            return decision_tree_classifier
        elif classifier_name == "KNeighborsClassifier":
            return k_neighbors_classifier
        elif classifier_name == "ForestClassifiers":
            return forest_classifiers
        elif classifier_name == "OneVsOneClassifier":
            return one_vs_one_classifier
        elif classifier_name == "OneVsRestClassifier":
            return one_vs_rest_classifier
        elif classifier_name == "OutputCodeClassifier":
            return output_code_classifier
        elif classifier_name == "any_classifier":
            return any_classifier
        else:
            raise Exception(f"Classifier {classifier_name} not supported")

    def train(self):
        for classifier in self.classifiers:
            if classifier in self.config["pretrained_model_paths"]:
                best_model = self.load(classifier)
                self.evaluate(best_model)
            else:
                hyperoptmodel = HyperoptEstimator(
                    classifier=self._get_classifer(classifier)(classifier),
                    preprocessing=[],
                    algo=tpe.suggest,
                    max_evals=self.max_evals,
                    trial_timeout=self.trial_timeout,
                )
                hyperoptmodel.fit(self.X_train, self.y_train)
                best_model = hyperoptmodel.best_model().get("learner")
                self.save(best_model)

    def evaluate(self, model):
        logger.info("Evaluating random_forest_model")
        score = model.score(self.X_test, self.y_test)
        logger.info(f"Model score : {score}")
        logger.info("Evaluation complete")
        return score

    def save(self, model):
        model_name = model.__class__.__name__
        model_path = self.models_dir / f"{model_name}"
        model_path.mkdir(exist_ok=True)

        model_output_path = (
            model_path / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pkl"
        )

        try:
            with open(model_output_path, "wb") as f:
                pickle.dump(model, f)
            logger.info(f"Model saved to {model_output_path}")
            if "pretrained_model_paths" not in self.config:
                self.config["pretrained_model_paths"] = {}

            score = self.evaluate(model)
            self.config["pretrained_model_paths"][model_name] = str(model_output_path)

            self.config_builder.update_config(self.config)

            if "model_scores" not in self.config:
                self.config["model_scores"] = {}

            self.config["model_scores"][model_name] = str(score)

            self.config_builder.update_config(self.config)
        except Exception as e:
            logger.error(f"Failed to save random_forest_model to {model_output_path}")
            logger.error(e)

    def load(self, model_name):
        model_load_path = self.config["pretrained_model_paths"][model_name]
        with open(model_load_path, "rb") as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {model_load_path}")
        return model
