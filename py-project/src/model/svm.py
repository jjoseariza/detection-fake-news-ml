import pickle
from config import config
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from src.utils.logger import logging


class SVM:
    def __init__(self):
        self.model = SVC(
            kernel=config["svm"]["kernel"], random_state=config["svm"]["random_state"]
        )
        self.is_trained = False

    def print_f1score(self, preds, labels):
        return f1_score(labels, preds, average=config["svm"]["svm_f1_score_average"])

    def fit(self, x_train, x_test, y_train, y_test):
        self.model.fit(x_train, y_train)
        self.is_trained = True

    def predict(self, X):
        assert self.is_trained, "Model should be trained before inference."
        return self.model.predict(X)

    def save(self, path=config["svm"]["default_save_path"]):
        if self.is_trained:
            pickle.dump(self.model, open(path, "wb"))
            logging.info(f"Saved model to {path}")
        else:
            logging.warning("Cannot save the model. Train it first.")

    def load(self, path=config["svm"]["default_save_path"]):
        self.model = pickle.load(open(path, "rb"))
        self.is_trained = True
