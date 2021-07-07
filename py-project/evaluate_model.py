from src.utils.logger import logging
from config import config
from src.loaders.loader import Loader
from src.preprocesing.preprocesing import Preprocesing
from sklearn.model_selection import train_test_split
from src.model.model import Model


def main():

    logging.info("Starting main")

    config_name = "svm-local"  # TODO coming from args

    logging.info(f"Model config selected: {config_name}")

    model_config = config["model_config"][config_name]
    assert model_config is not None, "Configuration not supported"

    # load data
    loader = Loader(model_config["loader_name"])
    data = loader.load_data()

    logging.info(f"Data loaded: {data['label'].value_counts()}")

    # preprocesing data
    preprocesing = Preprocesing(model_config["preprocesing_name"])
    X, y = preprocesing.preprocess(data)

    logging.info(f"Data preprocessed")

    # divide data
    _, x_test, _, y_test = train_test_split(
        X,
        y,
        test_size=model_config["train_split"]["test_size"],
        random_state=model_config["train_split"]["random_state"],
    )

    logging.info(f"Data divided to evaluate the model")

    # load model
    model = Model(model_config["model_name"]).getModelInstance()
    model.load()

    logging.info(f"Model loaded")

    # check model
    preds = model.predict(x_test)
    logging.info(
        f"Model accuracy: {model.print_f1score(y_test, preds)}",
    )

    logging.info("Ending main")


if __name__ == "__main__":
    main()
