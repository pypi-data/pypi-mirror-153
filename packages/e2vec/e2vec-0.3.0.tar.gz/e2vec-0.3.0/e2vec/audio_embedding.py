import warnings
import numpy
import torchaudio
from typing import NamedTuple

warnings.filterwarnings("ignore")


class AudioEmbedding:
    """
    PyTorch model for audio embedding.
    """

    def __init__(self, name: str) -> None:
        self._bundle = getattr(torchaudio.pipelines, name)
        self._model = self._bundle.get_model()

    def __call__(
        self, audio_path: "str"
    ) -> NamedTuple("Results", [("feature_vector", numpy.ndarray)]):
        waveform, sample_rate = torchaudio.load(audio_path)
        waveform = torchaudio.functional.resample(
            waveform, sample_rate, self._bundle.sample_rate
        )
        feature_vector, _ = self._model.extract_features(waveform)
        feature_vector = feature_vector[0].detach().numpy()
        Results = NamedTuple("Results", [("feature_vector", numpy.ndarray)])
        return Results(feature_vector)
