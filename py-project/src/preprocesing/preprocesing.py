from src.preprocesing.preprocesing_transform import PreprocesingTransform
from src.preprocesing.preprocesing_lstm import PreprocesingLSTM


class Preprocesing:
    def __init__(self, preprocesing_name, load_transform_model=False):
        self.preprocesing_name = preprocesing_name
        self.load_transform_model = load_transform_model
        if self.preprocesing_name == "preprocesing_transform":
            self.preprocessor = PreprocesingTransform()
        if self.preprocesing_name == "preprocesing_lstm":
            self.preprocessor = PreprocesingLSTM()

    def preprocess(self, data):
        assert self.preprocessor is not None, "Preprocessor not supported"
        return self.preprocessor.preprocess(data, self.load_transform_model)
