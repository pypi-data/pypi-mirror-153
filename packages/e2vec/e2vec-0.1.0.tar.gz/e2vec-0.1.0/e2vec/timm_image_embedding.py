import warnings
from typing import NamedTuple

import numpy
import timm
import torch
from PIL import Image as PILImage
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
from torch import nn as nn

warnings.filterwarnings("ignore")


class TimmImageEmbedding:
    """
    Embedding extractor using timm.
    Args:
        model_name (`string`):
            Model name.
        weights_path (`string`):
            Path to local weights.
    """

    def __init__(
        self,
        model_name: str = "vit_large_patch16_224",
        num_classes: int = 1000,
        weights_path: str = None,
    ) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if weights_path:
            self.model = timm.create_model(
                model_name, checkpoint_path=weights_path, num_classes=num_classes
            )
        else:
            self.model = timm.create_model(
                model_name, pretrained=True, num_classes=num_classes
            )
        self.model.eval()
        config = resolve_data_config({}, model=self.model)
        self.tfms = create_transform(**config)

    def __call__(
        self, image
    ) -> NamedTuple("Outputs", [("feature_vector", numpy.ndarray)]):
        img_tensor = self.tfms(PILImage.open(image)).unsqueeze(0)
        Outputs = NamedTuple("Outputs", [("feature_vector", numpy.ndarray)])
        self.model.to(self.device)
        self.model.eval()
        features = self.model.forward_features(img_tensor)
        if features.dim() == 4:
            global_pool = nn.AdaptiveAvgPool2d(1)
            features = global_pool(features)
        features = features.to("cpu")
        features = features.flatten().detach().numpy()
        return Outputs(features)
