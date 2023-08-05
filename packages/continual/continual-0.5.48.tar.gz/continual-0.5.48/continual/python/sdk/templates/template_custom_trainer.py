import pandas as pd
import dill
import os
import logging

import sklearn.linear_model as sklm

from continual.python.sdk.base_custom_trainer import BaseCustomTrainer


"""
Template custom model class

ADD YOUR IMPLEMENTATION HERE.
"""


class MyCustomTrainer(BaseCustomTrainer):
    """
    My custom model
    """

    model_file_name: str = "custom_trainer.pkl"

    def __init__(self, logger: logging.Logger):
        """
        Initialize any state
        """
        self._logger = logger
        self.model_type = sklm.ElasticNet

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.DataFrame,
        X_val: pd.DataFrame,
        y_val: pd.DataFrame,
        params: dict,
    ):
        """
        Construct and train model defined by config on data.
        Store any model state in self

        Parameters
        ----------
        X: DataFrame
            The training
        y: DataFrame
            The training outputs
        X_val: DataFrame
            validation features
        y_val: DataFrame
            validation outputs
        params: dict
            hyperparameters to the model
        """

        if self.model_type:
            self.model = self.model_type(**params).fit(X, y)
        else:
            raise Exception("Model type not initialized")

    def predict(self, X: pd.DataFrame, params: dict) -> pd.Series:
        """
        Run trained model on data. Utilize
        any model state in self.

        Note: Continual will ensure that fit()
        has been called before predict()

        Parameters
        ----------
        X : DataFrame
            The features from which to get predictions
        params: dict
            hyperparameters to the model

        Returns
        -------
        pd.Series
            The class predictions for the input data
        """

        return self.model.predict(X)

    def save(self, save_dir) -> str:
        """
        Serialize current instance state to disk in given
        directory (directory is already created)

        Parameters
        ----------
        save_dir : str
            Save path for serialized model file
        """

        model_file_path = os.path.join(save_dir, self.model_file_name)
        with open(model_file_path, "wb") as model_file:
            dill.dump(self.model, model_file)

    def load(self, load_dir: str):
        """
        Deserialize current instance state from given directory

        Parameters
        ----------
        load_dir: str
            The directory where the serialized files for this
            model are stored
        """

        model_file_path = os.path.join(load_dir, self.model_file_name)
        with open(model_file_path, "rb") as model_file:
            self.model = dill.load(model_file)

    def default_parameters(self):
        """
        Returns
        -------
        dict
            The default hyperparameters that will be
            passed to the fit function
        """

        return {"random_state": 0}
