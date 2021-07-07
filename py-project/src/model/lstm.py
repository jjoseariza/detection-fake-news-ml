from sklearn.metrics import f1_score
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing import text, sequence
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.models import Sequential, load_model
from config import config
import pickle
import h5py
from io import BytesIO
from src.utils.logger import logging
from src.utils.blob_client import get_blob_client
import os


class LSTM_MODEL:
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.history = None
        self.tokenizer = None

    def print_f1score(self, preds, labels):
        # return self.model.evaluate(x_train,y_train)[1]*100
        return f1_score(labels, preds, average=config["lstm"]["lstm_f1_score_average"])

    def tokenize_data(self, x_train, x_test):
        logging.info(f"Creating tokenizer")
        self.tokenizer = text.Tokenizer(
            num_words=config["lstm"]["max_features"])
        self.tokenizer.fit_on_texts(x_train)
        self.save_tokenizer()

        tokenized_train = self.tokenizer.texts_to_sequences(x_train)
        X_train = sequence.pad_sequences(
            tokenized_train, maxlen=config["lstm"]["max_len"]
        )
        tokenized_test = self.tokenizer.texts_to_sequences(x_test)
        X_test = sequence.pad_sequences(
            tokenized_test, maxlen=config["lstm"]["max_len"]
        )
        return X_train, X_test

    def get_coefs(self, word, *arr):
        return word, np.asarray(arr, dtype="float32")

    def create_embedding(self):
        logging.info(f"Creating embedding")
        embedding_file = self.load_embedding()

        logging.info(f"Creating embedding indexes")
        embeddings_index = dict(
            self.get_coefs(*o.rstrip().rsplit(" "))
            for o in embedding_file
        )

        all_embs = np.stack(embeddings_index.values())
        emb_mean, emb_std = all_embs.mean(), all_embs.std()
        embed_size = all_embs.shape[1]

        word_index = self.tokenizer.word_index
        nb_words = min(config["lstm"]["max_features"], len(word_index))

        embedding_matrix = np.random.normal(
            emb_mean, emb_std, (nb_words, embed_size))
        for word, i in word_index.items():
            if i >= config["lstm"]["max_features"]:
                continue
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        return Embedding(
            config["lstm"]["max_features"],
            output_dim=embed_size,
            weights=[embedding_matrix],
            input_length=config["lstm"]["max_len"],
            trainable=False,
        )

    def create_learning_rate(self):
        logging.info(f"Creating Learning rate")
        return ReduceLROnPlateau(
            monitor=config["lstm"]["monitor"],
            patience=config["lstm"]["patience"],
            verbose=config["lstm"]["verbose"],
            factor=config["lstm"]["factor"],
            min_lr=config["lstm"]["min_lr"],
        )

    def create_neural_network(self):
        logging.info(f"Creating neural network")
        # Defining Neural Network
        self.model = Sequential()
        # Non-trainable embeddidng layer
        self.model.add(self.create_embedding())
        # LSTM
        self.model.add(
            LSTM(units=128, return_sequences=True,
                 recurrent_dropout=0.25, dropout=0.25)
        )
        self.model.add(LSTM(units=64, recurrent_dropout=0.1, dropout=0.1))
        self.model.add(Dense(units=32, activation="relu"))
        self.model.add(Dense(1, activation="sigmoid"))
        self.model.compile(
            optimizer=tensorflow.keras.optimizers.Adam(lr=0.01),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        logging.info(f"Neural network created")

    def fit(self, x_train, x_test, y_train, y_test):
        logging.info(f"Training model")
        X_train, X_test = self.tokenize_data(x_train, x_test)
        learning_rate_reduction = self.create_learning_rate()
        self.create_neural_network()

        self.history = self.model.fit(
            X_train,
            y_train,
            batch_size=config["lstm"]["batch_size"],
            validation_data=(X_test, y_test),
            epochs=config["lstm"]["epochs"],
            callbacks=[learning_rate_reduction],
        )
        self.is_trained = True
        logging.info(f"Model trained")

    def predict(self, x_test):
        assert self.is_trained, "Model should be trained before inference."

        if self.tokenizer is None:
            self.load_tokenizer()

        tokenized_test = self.tokenizer.texts_to_sequences(x_test)
        X_test = sequence.pad_sequences(
            tokenized_test, maxlen=config["lstm"]["max_len"]
        )

        pred = self.model.predict(X_test)

        logging.info(f"Model prediction: {pred[0]}")
        
        # pred[0] > 0.5 then the news is true
        # else then the news is false
        return pred[0] > 0.5

    def save_tokenizer(self, path=config["lstm"]["tokenizer_path"]):
        if config["lstm"]["from_azure"]:
            pickle.dump(self.tokenizer, open("lstm-tokenizer.pkl", "wb"))
            blob_client = get_blob_client("models", "lstm-tokenizer.pkl")
            with open("lstm-tokenizer.pkl", 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
             
        else:
            pickle.dump(self.tokenizer, open(path, "wb"))

    def load_tokenizer(self, path=config["lstm"]["tokenizer_path"]):
        logging.info(f"Loading tokenizer")
        if config["lstm"]["from_azure"]:
            blob_client = get_blob_client("models", "lstm-tokenizer.pkl")
            downloader = blob_client.download_blob(0)
            self.tokenizer = pickle.loads(downloader.readall())
            logging.info(f"Loaded from azure")
        else:
            self.tokenizer = pickle.load(open(path, "rb"))
            logging.info(f"Loaded from local")

    def load_embedding(self):
        logging.info(f"Loading embedding")
        if config["lstm"]["from_azure"]:
            
            filePath = "./glove.embedding.txt"
            if os.path.exists(filePath):
                return open(filePath)

            blob_client = get_blob_client("models", "glove.twitter.27B.100d.txt")
            with open(filePath, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            logging.info(f"Loaded from azure in local")

            return open(filePath)
        else:
            logging.info(f"Loaded from local")
            return open(config["lstm"]["embedding_file"])

    def save(self, path=config["lstm"]["default_save_path"]):
        if self.is_trained:
            if config["lstm"]["from_azure"]:
                self.model.save("lstm-glove.h5")
                blob_client = get_blob_client("models", "lstm-glove.h5")
                with open("lstm-glove.h5", 'rb') as data:
                    blob_client.upload_blob(data, overwrite=True)
            else:
                self.model.save(path)
                logging.info(f"Saved model to {path}")
        else:
            logging.warning("Cannot save the model. Train it first.")

    def load(self, path=config["lstm"]["default_save_path"]):
        logging.info(f"Loading model")
        if config["lstm"]["from_azure"]:
            blob_client = get_blob_client("models", "lstm-glove.h5")
            downloader = blob_client.download_blob(0)
            with BytesIO() as f:
                downloader.readinto(f)
                with h5py.File(f, 'r') as h5file:
                    self.model = load_model(h5file)
                    logging.info(f"Loaded from azure")
        else:
            self.model = load_model(path)
            logging.info(f"Loaded from local")

        self.load_tokenizer()

        self.is_trained = True
