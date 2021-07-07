import pandas
from flask import Flask, request, jsonify
from config import config
from src.preprocesing.preprocesing import Preprocesing
from src.model.model import Model
from src.utils.blob_client import get_blob_client
import datetime
import uuid
import json

app = Flask(__name__)

# load the model
model_config = config["model_config"][config["app_model_active"]]
model = Model(model_config["model_name"]).getModelInstance()
model.load()

@app.route("/")
def index():
    return "Fake News Detector API"

@app.route("/predict", methods=["POST"])
def predict():
    request_data = request.get_json()
    data = pandas.json_normalize(request_data)

    # preprocesing data
    preprocesing = Preprocesing(
        model_config["preprocesing_name"],
        load_transform_model=model_config["load_transform_model"],
    )
    X, _ = preprocesing.preprocess(data)

    # prediction
    prediction = model.predict(X)

    return jsonify({"result" : bool(prediction)})

@app.route("/store-wrong", methods=["POST"])
def store_wrong():
    request_data = request.get_json()

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = f'{uuid.uuid4().hex}-{date}.json'

    blob_client = get_blob_client("feedback-data", file_name)
    blob_client.upload_blob(json.dumps(request_data))

    return jsonify({ "result" : True })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
