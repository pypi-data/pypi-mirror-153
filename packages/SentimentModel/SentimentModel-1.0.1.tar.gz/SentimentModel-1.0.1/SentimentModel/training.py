import time
from SentimentModel.Processing import data_management as dm
from SentimentModel.Processing import preprocessing as pp
from SentimentModel.Config.core import config
from SentimentModel.Config import logging_config
from SentimentModel import pipeline
# from SentimentModel import word_embeddings

_logger = logging_config.get_logger(__name__)

def run_training(save_result: bool = True):
    """Train a Recurrent Neural Network."""
    _logger.info("Training...")
    start_time = time.time()


    df = dm.read_data()[:]
    X, y = dm.get_value_target(df)

    _logger.info("Cleaning data...")
    clean_text = pp.CleanText()
    X_cleaned = clean_text.transform(X)

    # embedding_matrix = word_embeddings._Word2Vec().make_embedding_matrix(X_cleaned)
    # pipeline.pipe_rnn.named_steps['model'].set_params(
    #     embedding_matrix=embedding_matrix)

    _logger.info("Training model...")
    pipeline.pipe_rnn.fit(X_cleaned, y)

    if save_result:
        dm.save_pipeline_keras(pipeline.pipe_rnn)

    end_time = time.time()
    _logger.info("Training complete.")
    _logger.info(f"Training time {(end_time - start_time)//60} minutes.")


if __name__ == '__main__':
    run_training(save_result=True)
