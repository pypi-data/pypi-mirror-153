import pandas as pd
import time

import joblib
from tensorflow.keras.models import load_model

from SentimentModel.Config.core import config
from SentimentModel.Processing import data_management as dm
from SentimentModel.Processing import preprocessing as pp
from SentimentModel.Config import logging_config

_logger = logging_config.get_logger(__name__)

pipe = dm.load_pipeline_keras()


# tokenizer = joblib.load(config.app.MODELS_PATH + config.app.TOKENIZER_NAME)
# model = load_model(config.app.MODELS_PATH + config.app.MODEL_NAME)


def get_label(proba):
    idx = proba.argmax(axis=0)
    max_proba = proba[idx]

    if max_proba < config.model.NEUTRAL_THRESHOLD:
        return config.model.NEUTRAL_INDEX
    elif idx == 0:
        return config.model.NEGATIVE_INDEX
    elif idx == 1:
        return config.model.POSITIVE_INDEX



def make_bulk_prediction(raw: pd.Series, reg: pd.Series=None, clean=False) -> list:
    """Make multiple predictions using the saved model pipeline"""
    _logger.info("Predicting...")
    start = time.time()

    if reg:
        X = reg
    else:
        X = raw

    if clean:
        X = pp.CleanText().transform(X)
    
    predictions = pipe.predict_proba(X)

    # # X = tokenizer.transform(X)
    # # X = pp.PaddingText().transform(X)

    # # start = time.time()
    # # predictions = model.predict(X)


    labels = [config.model.CLASSES[int(get_label(p))] for p in predictions]

    labels_columns = [config.model.CLASSES[config.model.NEGATIVE_INDEX], config.model.CLASSES[config.model.POSITIVE_INDEX]]
    df_predictions = pd.DataFrame(predictions, columns=labels_columns)
    df_predictions['label'] = labels
    df_predictions.insert(0, 'tweet', raw)

    end = time.time()
    _logger.info("Prediction complete.")
    _logger.info(f"Prediction time: {(end - start)} seconds")
    return df_predictions


if __name__ == '__main__':
    x = dm.read_data()[:10]
    x = x['text']
    z = make_bulk_prediction(x, True)
    print(z)
