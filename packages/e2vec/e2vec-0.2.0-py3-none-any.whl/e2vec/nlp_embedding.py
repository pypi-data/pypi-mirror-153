import warnings
from typing import NamedTuple

import numpy
from transformers import AutoModel, AutoTokenizer

warnings.filterwarnings("ignore")


class NLPEmbedding:
    """
    NLP embedding operator that uses the pretrained transformers model gathered by huggingface.
    Args:
        model_name (`str`):
            Which model to use for the embeddings.
    """

    def __init__(self, model_name: str) -> None:
        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def __call__(
        self, txt: str
    ) -> NamedTuple("Results", [("feature_vector", numpy.ndarray)]):
        inputs = self.tokenizer(txt, return_tensors="pt")
        outs = self.model(**inputs)
        feature_vector = outs.last_hidden_state.squeeze(0)
        Results = NamedTuple("Results", [("feature_vector", numpy.ndarray)])
        return Results(feature_vector.detach().numpy())
