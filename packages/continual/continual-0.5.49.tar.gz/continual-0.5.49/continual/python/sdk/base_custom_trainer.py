import pandas as pd
import logging


class BaseCustomTrainer:
    """
    Base Class for all custom model implementations
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize any state

        Parameters
        ----------
        logger: Logger
            Continual provided logger to log messages from
            this model
        """

        self._logger = logger

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

        raise NotImplementedError

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
        pandas.Series
            The class predictions for the input data
        """

        raise NotImplementedError

    def save(self, save_dir):
        """
        Serialize current instance state to disk in given
        directory (directory is already created)

        Parameters
        ----------
        save_dir : str
            Save path for serialized model file
        """

        raise NotImplementedError

    def load(self, load_dir: str):
        """
        Deserialize current instance state from given directory

        Parameters
        ----------
        load_dir: str
            The directory where the serialized files for this
            model are stored
        """
        raise NotImplementedError

    def default_parameters(self) -> dict:
        """
        Returns
        -------
        dict
            The default hyperparameters that will be
            passed to the fit function
        """

        raise NotImplementedError
