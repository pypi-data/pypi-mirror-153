from enum import Enum

import numpy
from deci_common.abstractions.base_model import Schema
from deci_common.data_types.enum.deep_learning_task import DeepLearningTask
from deci_common.helpers import get_all_enum_fields_in_web_form


class BatchSize(int, Enum):
    ONE = 1
    EIGHT = 8
    SIXTEEN = 16
    THIRTY_TWO = 32
    SIXTY_FOUR = 64


class BatchSizeEdge(int, Enum):
    ONE = 1
    TWO = 2
    FOUR = 4
    EIGHT = 8


class Metric(str, Enum):
    ACCURACY = "accuracy"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    MEMORY = "memory_footprint"
    SIZE = "model_size"


class AccuracyMetricType(str, Enum):
    PERCENTAGE = "percentage"
    FLOAT = "float"


class AccuracyMetricKey(str, Enum):
    TOP1 = "Top-1"
    TOP5 = "Top-5"
    AUC = "AUC"
    PRECISION = "Precision"
    RECALL = "Recall"
    F1_SCORE = "F1 Score"
    TRUE_POSITIVES = "True Positives"
    TRUE_NEGATIVES = "True Negatives"
    FALSE_POSITIVES = "False Positives"
    FALSE_NEGATIVES = "False Negatives"
    MIOU = "mIoU"
    PIXEL_ACCURACY = "Pixel Accuracy"
    DICE_COEFFICIENT = "Dice Coefficient (F1 Score)"
    MAP = "mAP"
    COCO_MAP = "mAP@0.5:0.95"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    ABS_REL = "AbsRel"
    SQ_REL = "SqRel"
    RMSE = "Root Mean Squared Error"
    RMSElog = "Root Mean Squared Error - Log"
    SLLOG = "Sllog"
    LOG10 = "Log-10"
    PCK = "PCK"
    PCKH = "PCKh"
    PDJ = "PDJ"
    OKS = "OKS"
    CUSTOM = "Custom"


class MapDLTaskToDefaultAccuracyMetric(str, Enum):
    OBJECT_DETECTION = AccuracyMetricKey.COCO_MAP.value
    SEMANTIC_SEGMENTATION = AccuracyMetricKey.MIOU.value
    CLASSIFICATION = AccuracyMetricKey.TOP1.value


class AccuracyMetric(Schema):
    key: str
    value: float
    type: AccuracyMetricType
    isPrimary: bool


class Architecture(str, Enum):
    RESNET18 = "resnet18"
    RESNET50 = "resnet50"
    RESNET34 = "resnet34"
    RESNET50_3343 = "resnet50_3342"
    RESNET101 = "resnet101"
    RESNET152 = "resnet152"
    RESNET18_CIFAR = "resnet18_cifar"
    RESNET_CUSTOM = "resnet_custom"
    RESNET50_CUSTOM = "resnet50_custom"
    RESNET_CUSTOM_CIFAR = "resnet_custom_cifar"
    RESNET50_CUSTOM_CIFAR = "resnet50_custom_cifar"
    MOBILENET_V2 = "mobilenet_v2"
    MOBILENET_V2_135 = "mobilenet_v2_135"
    CUSTOM_MOBILENET_V2 = "mobilenet_v2_custom"
    MOBILENET_V3_Large = "mobilenet_v3_large"
    MOBILENET_V3_SMALL = "mobilenet_v3_small"
    MOBILEMET_V3_CUSTOM = "mobilenet_v3_custom"
    YOLO_V3 = "yolo_v3"
    TINY_YOLO_V3 = "tiny_yolo_v3"
    CUSTOM_DENSENET = "custom_densenet"
    DENSENET121 = "densenet121"
    DENSENET161 = "densenet161"
    DENSENET169 = "densenet169"
    DENSENET201 = "densenet201"
    SHELFNET18 = "shelfnet18"
    SHELFNET34 = "shelfnet54"
    SHELFNET50 = "shelfnet50"
    SHELFNET50_3343 = "shelfnet50_3343"
    SHELFNET101 = "shelfnet101"
    SHELFNET_V2_X0_5 = "shelfnet_v2_x0_5"
    SHELFNET_V2_X1_0 = "shelfnet_v2_x1_0"
    SHELFNET_V2_X1_5 = "shelfnet_v2_x1_5"
    SHELFNET_V2_X2_0 = "shelfnet_v2_x2_0"
    SHELFNET_V2_CUSTOM = "shelfnet_v2_custom"
    DARKNET53 = "darknet53"
    CSP_DARKENT53 = "CSPDarknet"
    RESNEXT50 = "resnext50"
    RESNEXT101 = "resnext101"
    GOOGLENET = "googlenet"
    EFFICIENTNET_B0 = "efficientnet_b0"
    EFFICIENTNET_B1 = "efficientnet_b1"
    EFFICIENTNET_B2 = "efficientnet_b2"
    EFFICIENTNET_B3 = "efficientnet_b3"
    EFFICIENTNET_B4 = "efficientnet_b4"
    EFFICIENTNET_B5 = "efficientnet_b5"
    EFFICIENTNET_B6 = "efficientnet_b6"
    EFFICIENTNET_B7 = "efficientnet_b7"
    EFFICIENTNET_B8 = "efficientnet_b8"
    EFFICIENTNET_L2 = "efficientnet_l2"
    EFFICIENTNET_CUSTOM = "efficientnet_custom"
    REGNETY200 = "regnety200"
    REGNETY400 = "regnety400"
    REGNETY600 = "regnety600"
    REGNETY800 = "regnety800"
    REGNET_CUSTOM = "regnet_custom"
    REGNET_NAS = "regnet_nas"
    YOLO_V5S = "yolo_v5s"
    YOLO_V5M = "yolo_v5m"
    YOLO_V5L = "yolo_v5l"
    YOLO_V5X = "yolo_v5x"
    YOLO_V5_CUSTOM = "yolo_v5_custom"
    YOLO_V5_MOBILE = "yolo_v5_mobile"
    SSD_MOBILENET_V1 = "ssd_mobilenet_v1"
    SSD_LITE_MOBILENET_V2 = "ssd_lite_mobilenet_v2"


class MapAccuracyMetricsToDLTask(str, Enum):
    TOP1 = DeepLearningTask.CLASSIFICATION.value
    TOP5 = DeepLearningTask.CLASSIFICATION.value
    AUC = DeepLearningTask.CLASSIFICATION.value
    PRECISION = DeepLearningTask.CLASSIFICATION.value
    RECALL = DeepLearningTask.CLASSIFICATION.value
    F1_SCORE = DeepLearningTask.CLASSIFICATION.value
    TRUE_POSITIVES = DeepLearningTask.CLASSIFICATION.value
    TRUE_NEGATIVES = DeepLearningTask.CLASSIFICATION.value
    FALSE_POSITIVES = DeepLearningTask.CLASSIFICATION.value
    FALSE_NEGATIVES = DeepLearningTask.CLASSIFICATION.value
    MIOU = DeepLearningTask.SEMANTIC_SEGMENTATION.value
    PIXEL_ACCURACY = DeepLearningTask.SEMANTIC_SEGMENTATION.value
    DICE_COEFFICIENT = DeepLearningTask.SEMANTIC_SEGMENTATION.value
    MAP = DeepLearningTask.OBJECT_DETECTION.value
    COCO_MAP = DeepLearningTask.OBJECT_DETECTION.value
    # D1 = DeepLearningTask.DEPTH_ESTIMATION.value
    # D2 = DeepLearningTask.DEPTH_ESTIMATION.value
    # D3 = DeepLearningTask.DEPTH_ESTIMATION.value
    # ABS_REL = DeepLearningTask.DEPTH_ESTIMATION.value
    # SQ_REL = DeepLearningTask.DEPTH_ESTIMATION.value
    # RMSE = DeepLearningTask.DEPTH_ESTIMATION.value
    # RMSElog = DeepLearningTask.DEPTH_ESTIMATION.value
    # SLLOG = DeepLearningTask.DEPTH_ESTIMATION.value
    # LOG10 = DeepLearningTask.DEPTH_ESTIMATION.value
    # PCK = DeepLearningTask.POSE_ESTIMATION.value
    # PCKH = DeepLearningTask.POSE_ESTIMATION.value
    # PDJ = DeepLearningTask.POSE_ESTIMATION.value
    # OKS = DeepLearningTask.POSE_ESTIMATION.value

    @staticmethod
    def get_accuracy_metrics_keys_by_dl_task(dl_task: DeepLearningTask):
        return [
            AccuracyMetricKey[k] for k, v in MapAccuracyMetricsToDLTask.__members__.items() if v == dl_task
        ]  # use of __members__.items() is needed here because of the repetition of values in enum.


class QuantizationLevel(str, Enum):
    FP32 = "FP32"
    FP16 = "FP16"
    INT8 = "INT8"
    HYBRID = "Hybrid"

    @staticmethod
    def from_string(quantization_level: str) -> Enum:
        quantization_level = quantization_level.lower()
        if quantization_level == "fp32":
            return QuantizationLevel.FP32
        elif quantization_level == "fp16":
            return QuantizationLevel.FP16
        elif quantization_level == "int8":
            return QuantizationLevel.INT8
        elif quantization_level == "hybrid":
            return QuantizationLevel.HYBRID
        else:
            raise NotImplementedError(f'Quantization Level: "{quantization_level}" is not supported')

    @property
    def numpy_type(self):
        map_quantization_level_to_numpy_type = {
            QuantizationLevel.FP32: numpy.float32,
            QuantizationLevel.FP16: numpy.float16,
            QuantizationLevel.INT8: numpy.int8,
        }
        return map_quantization_level_to_numpy_type[self]


def get_all_architectures_in_web_form():
    return get_all_enum_fields_in_web_form(Architecture, custom={"mmp": "MMP", "csp_darknet53": "CSPDarknet"})


def get_all_dl_tasks_in_web_form():
    """
    This function made to serve the platform ui.
    Returns:
        all dl tasks transformed from  'object_detection' to 'objectDetection'
    """
    return get_all_enum_fields_in_web_form(DeepLearningTask, custom={"nlp": "NLP"})
