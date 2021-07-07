from src.preprocesing.utils.preprocessing_tools import denoise_text


class PreprocesingLSTM:
    def preprocess(self, data, load_transform_model):
        data["text_0"] = data["title"] + data["text"]
        X = data["text_0"].apply(denoise_text)

        y = None
        if "label" in data:
            y = data.label

        return X, y
