from src.utils.logger import logging
from config import config
from src.loaders.loader import Loader
from src.preprocesing.preprocesing import Preprocesing
from sklearn.model_selection import train_test_split
from src.model.model import Model


def main():

    logging.info("Starting main")

    config_name = config["app_model_active"]

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
    x_train, x_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=model_config["train_split"]["test_size"],
        random_state=model_config["train_split"]["random_state"],
    )

    logging.info(f"Data divided to fit the model")

    # fit model
    model = Model(model_config["model_name"]).getModelInstance()
    model.fit(x_train, x_test, y_train, y_test)

    logging.info(f"Model trained")

    # check model
    preds = model.predict(x_test)
    f1_score = model.print_f1score(y_test, preds)
    logging.info(f"Model accuracy: {f1_score}")

    # store new model
    model.save()
    logging.info(f"New model stored")

    logging.info("Ending main")


if __name__ == "__main__":
    main()
