from src.model.svm import SVM
from src.model.lstm import LSTM_MODEL

# from src.model.spacy import SPACY


class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        if self.model_name == "svm":
            self.model = SVM()
        if self.model_name == "lstm":
            self.model = LSTM_MODEL()
        # if self.model_name == "spacy":
        #     self.model = SPACY()

    def getModelInstance(self):
        assert self.model is not None, "Model not supported"
        return self.model
