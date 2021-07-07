from src.preprocesing.utils.preprocessing_tools import PreprocessText, Tfidf_transform


class PreprocesingTransform:
    def preprocess(self, data, load_transform_model):
        data["text_0"] = data["title"] + data["text"]

        processed_df = PreprocessText(data, "text_0")
        X = processed_df.text_0

        y = None
        if "label" in processed_df:
            y = processed_df.label

        X = Tfidf_transform(X, load_transform_model)

        return X, y
