from sklearn.pipeline import Pipeline

from SentimentModel.Processing import preprocessing as pp
from SentimentModel import model


pipe_rnn = Pipeline([
    ('tokenize', pp.TokenizeText()),
    ('pad', pp.PaddingText()),
    ('model', model.lstm_clf)
])
