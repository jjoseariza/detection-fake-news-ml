#!/usr/bin/env python
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

config = {}

config["root_dir"] = ROOT_DIR
config["app_model_active"] = "lstm-azure"

config["azure"] = {
    "connection": "<AZURE-KEY>"
}

# Configurations
config["model_config"] = {
    "svm-local": {
        "model_name": "svm",
        "loader_name": "local_loader",
        "preprocesing_name": "preprocesing_transform",
        "load_transform_model": True,
        "train_split": {"test_size": 0.2, "random_state": 0},
    },
    "lstm-local": {
        "model_name": "lstm",
        "loader_name": "local_loader",
        "preprocesing_name": "preprocesing_lstm",
        "load_transform_model": False,
        "train_split": {"test_size": None, "random_state": 0},
    },
    "lstm-azure": {
        "model_name": "lstm",
        "loader_name": "blob_loader",
        "preprocesing_name": "preprocesing_lstm",
        "load_transform_model": False,
        "train_split": {"test_size": None, "random_state": 0},
    },
    "spacy-local": {
        "model_name": "spacy",
        "loader_name": "local_loader",
        "preprocesing_name": "preprocesing_transform",
        "load_transform_model": False,
        "train_split": {"test_size": 0.2, "random_state": 0},
    },
}

# Loaders
config["local_data_paths"] = [
    {
        "method": "load_from_csv",
        "path": "data/snoopes.csv",
    },
    {
        "method": "load_from_csv",
        "path": "data/metro-water.csv",
    },
    {
        "method": "load_from_csv",
        "path": "data/mix.csv",
    },
]

config["blob_loader"] = {
    "blob_container": "data",
    "blob_file_prefix": "data-",
}

# Preprocesing
config["preprocessing"] = {
    "stopwords-language": "english",
    "vec-max-featues": 5000,
    "output_path": ROOT_DIR + "/models/prep-transform.pkl",
}

# SVM
config["svm"] = {
    "kernel": "linear",
    "random_state": 0,
    "svm_f1_score_average": "macro",
    "default_save_path": ROOT_DIR + "/models/svm.pkl",
}

# LSTM
config["lstm"] = {
    "lstm_f1_score_average": "macro",
    "max_features": 10000,
    "max_len": 300,
    "embedding_file": ROOT_DIR + "/models/glove.twitter.27B.100d.txt",
    "batch_size": 256,
    "epochs": 10,
    "monitor": "val_accuracy",
    "patience": 2,
    "verbose": 1,
    "factor": 0.5,
    "min_lr": 0.00001,
    "from_azure": True,
    "tokenizer_path": ROOT_DIR + "/models/lstm-tokenizer.pkl",
    "default_save_path": ROOT_DIR + "/models/lstm-glove.h5",
}

# SpaCy
config["spacy"] = {
    "spacy_model": "",
    "spacy_pipe_name": "",
    "spacy_pipe_options": "",
    "spacy_pipe_labels": "",
    "text_data": "",
    "text_label": "",
    "spacy_pipe_name": "",
    "spacy_n_iter": "",
    "default_save_path": "",
}
