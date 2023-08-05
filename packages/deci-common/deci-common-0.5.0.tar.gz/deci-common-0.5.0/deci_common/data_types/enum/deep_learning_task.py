from enum import Enum


class DeepLearningTask(str, Enum):
    CLASSIFICATION = "classification"
    SEMANTIC_SEGMENTATION = "semantic_segmentation"
    OBJECT_DETECTION = "object_detection"
    NLP = "nlp"
    OTHER = "other"
