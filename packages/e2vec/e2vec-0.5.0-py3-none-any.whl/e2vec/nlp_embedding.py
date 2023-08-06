import warnings
from typing import NamedTuple

import numpy
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore")


class NLPEmbedding:
    """
    NLP embedding operator that uses the pretrained transformers model gathered by sentence-transformers.
    Args:
        model_name (`str`):
            Which model to use for the embeddings.
    """

    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)

    def __call__(
        self, txt: str
    ) -> NamedTuple("Results", [("feature_vector", numpy.ndarray)]):
        feature_vector = self.model.encode(txt)
        Results = NamedTuple("Results", [("feature_vector", numpy.ndarray)])
        return Results(feature_vector)
