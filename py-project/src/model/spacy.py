from config import config
import os
import spacy
import random
from spacy.util import minibatch, compounding
from pathlib import Path
import yaml

# Adding the labels to textcat
LABELS = {
    "TRUE": True,
    "FAKE": False,
}


class SPACY:
    def __init__(self):
        self.nlp = None
        self.is_trained = False

    def create_model(self):
        self.nlp = spacy.load(config["spacy"]["spacy_model"])
        new_pipe = self.nlp.create_pipe(
            config["spacy"]["spacy_pipe_name"],
            config=config["spacy"]["spacy_pipe_options"],
        )
        self.nlp.add_pipe(new_pipe, last=True)

        for label in config["spacy"]["spacy_pipe_labels"]:
            self.new_pipe.add_label(label)

    def convert_trainning_data(self, data, split=0.8):
        tuples = data.apply(
            lambda row: (
                row[config["spacy"]["text_data"]],
                row[config["spacy"]["text_label"]],
            ),
            axis=1,
        )
        tuples = tuples.tolist()

        # Shuffle the data
        random.shuffle(tuples)
        texts, labels = zip(*tuples)

        # get the categories for each review
        cats = [{"TRUE": bool(y), "FAKE": not bool(y)} for y in labels]

        # Splitting the training and evaluation data
        split = int(len(tuples) * split)

        (train_texts, train_cats), (dev_texts, dev_cats) = (
            texts[:split],
            cats[:split],
        ), (texts[split:], cats[split:])

        train_data = list(zip(train_texts, [{"cats": cats} for cats in train_cats]))

        return (train_data, dev_texts, dev_cats)

    def evaluate(tokenizer, textcat, texts, cats):
        docs = (tokenizer(text) for text in texts)
        tp = 0.0  # True positives
        fp = 1e-8  # False positives
        fn = 1e-8  # False negatives
        tn = 0.0  # True negatives
        for i, doc in enumerate(textcat.pipe(docs)):
            gold = cats[i]
            for label, score in doc.cats.items():
                if label not in gold:
                    continue
                if label == "FAKE":
                    continue
                if score >= 0.5 and gold[label] >= 0.5:
                    tp += 1.0
                elif score >= 0.5 and gold[label] < 0.5:
                    fp += 1.0
                elif score < 0.5 and gold[label] < 0.5:
                    tn += 1
                elif score < 0.5 and gold[label] >= 0.5:
                    fn += 1
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        if (precision + recall) == 0:
            f_score = 0.0
        else:
            f_score = 2 * (precision * recall) / (precision + recall)
        return {"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}

    def fit(self, data):
        # Converting data
        (train_data, dev_texts, dev_cats) = self.convert_trainning_data(data)

        # Disabling other components
        other_pipes = [
            pipe
            for pipe in self.nlp.pipe_names
            if pipe != config["spacy"]["spacy_pipe_name"]
        ]

        with self.nlp.disable_pipes(*other_pipes):  # only train textcat
            optimizer = self.nlp.begin_training()

            print("Training the model...")
            print("{:^5}\t{:^5}\t{:^5}\t{:^5}".format("LOSS", "P", "R", "F"))

            # Performing training
            for i in range(config["spacy"]["spacy_n_iter"]):
                losses = {}
                batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self.nlp.update(
                        texts, annotations, sgd=optimizer, drop=0.2, losses=losses
                    )

                # Calling the evaluate() function and printing the scores
                with self.new_pipe.model.use_params(optimizer.averages):
                    scores = self.evaluate(
                        self.nlp.tokenizer, self.new_pipe, dev_texts, dev_cats
                    )

                print(
                    "{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}".format(
                        losses["textcat"],
                        scores["textcat_p"],
                        scores["textcat_r"],
                        scores["textcat_f"],
                    )
                )

        self.is_trained = True

    def predict(self, X, convert_to_int=True):

        predicted_values = [self.nlp(row).cats for row in X]
        predicted_values = self.map_labels_to_values(
            predicted_values, convert_to_int=convert_to_int
        )

        if len(predicted_values) == 1:
            predicted_values = predicted_values[0]

        return predicted_values

    def save(self, path=config["spacy"]["default_save_path"]):

        if self.is_trained:
            output_dir = Path(path)
            if not output_dir.exists():
                os.makedirs(output_dir)

            model_config = {
                "base_model": config["spacy"]["model"],
                "architecture": config["spacy"]["architecture_textcat"],
            }
            with open(os.path.join(output_dir, f"model_config.yaml"), "w") as file:
                documents = yaml.dump(model_config, file)
            self.nlp.meta["name"] = config["spacy"]["model_type"]
            self.nlp.to_disk(output_dir)

            self.logger.info(f"Saved model to {output_dir}")
        else:
            self.logger.warning("Cannot save the model. Train it first.")

    def load(self, path=config["spacy"]["default_save_path"]):
        output_dir = Path(path)
        with open(os.path.join(output_dir, f"model_config.yaml")) as file:
            model_config = yaml.load(file, Loader=yaml.FullLoader)
        self.architecture = model_config["spacy"]["architecture"]

        self.nlp = spacy.load(output_dir)
        self.is_trained = True
