"""Enumeration classes used in the Masterful API. """
import enum


@enum.unique
class Task(enum.Enum):
  """An enum to semantically specify a model's use case.

  Args:
    value: Overriden from :class:`enum.Enum`. Returns the member of this enum
      from the corresponding value.

  Attributes:
    CLASSIFICATION: Normal classification task like Alexnet on Imagenet.
    BINARY_CLASSIFICATION: Binary classification task.
    MULTILABEL_CLASSIFICATION: Multi-label classification task.
    DETECTION: Object detection (localization + classification) task.
    LOCALIZATION: Object localization task.
    SEMANTIC_SEGMENTATION: Semantic segmentation task.
    INSTANCE_SEGMENTATION: Instance segmentation task.
    KEYPOINT_DETECTION: Keypoint detection task.
  """
  CLASSIFICATION = "classification"
  BINARY_CLASSIFICATION = "binary_classification"
  MULTILABEL_CLASSIFICATION = "multilabel_classification"
  DETECTION = "detection"
  LOCALIZATION = "localization"
  SEMANTIC_SEGMENTATION = "semantic_segmentation"
  INSTANCE_SEGMENTATION = "instance_segmentation"
  KEYPOINT_DETECTION = "keypoint_detection"


@enum.unique
class ImageRange(enum.Enum):
  """An enum to model the image input ranges Masterful supports.

  ImageRange describes the range of the image pixel values.
  Common ranges include [0,255] and [0,1]. Some models also
  prefer to normalize the input data around the ImageNet
  mean and standard deviation.

  Args:
    value: Overriden from :class:`enum.Enum`. Returns the member of this enum
      from the corresponding value.

  Attributes:
    ZERO_ONE: Image range is [0,1].
    NEG_ONE_POS_ONE: Image range is [-1, 1].
    ZERO_255: Image range is [0,255].
    IMAGENET_CAFFE_BGR: Image is in BGR channel format, and each channel has been zero-centered around the Imagenet mean, without scaling.
    IMAGENET_TORCH: Image pixels were scaled to [0,1], then each channel was zero-centered around the Imagenet mean.
    CIFAR10_TORCH: Image pixels were scaled to [0,1], then each channel was zero-centered around the CIFAR10 mean.
    CIFAR100_TORCH: Image pixels were scaled to [0,1], then each channel was zero-centered around the CIFAR100 mean.
  """
  ZERO_ONE = "zero_one"
  NEG_ONE_POS_ONE = "neg_one_pos_one"
  ZERO_255 = "zero_255"
  IMAGENET_CAFFE_BGR = "imagenet_caffe_bgr"
  IMAGENET_TORCH = "imagenet_torch"
  CIFAR10_TORCH = "cifar10_torch"
  CIFAR100_TORCH = "cifar100_torch"


@enum.unique
class TensorStructure(enum.Enum):
  """An enum to specify tensor structures.

  A tensor structure is the physical data structure used to encapsulate
  individual tensors. This can either be a single tensor itself, in which
  case the single tensor is passed to each output of the model, or a tuple
  of tensors, in which case the number of tensors in the tuple must match exactly
  the number of outputs in the model.

  Attributes:
    SINGLE_TENSOR: Label or prediction consists of a single tensor, which is passed
      to all outputs of the model.

    TUPLE: Label or prediction consists of a tuple of tensors, which must map exactly
      to the number of outputs of a model.

    DICT: Label or prediction is a dictionary output tensors.
  """

  SINGLE_TENSOR = "single_tensor"
  TUPLE = "tuple"
  DICT = "dict"


@enum.unique
class BoundingBoxFormat(enum.Enum):
  """ Bounding box formats support by Masterful.

  Attributes:
    TENSORFLOW: The Tensorflow bounding box format is
      (ymin, xmin, ymax, xmax), normalized by the image dimensions
      into the range [0,1].
    VOC: The Pascal VOC bounding box format is
      (xmin, ymin, xmax, ymax) in pixel coordinates.
    COCO: The MSCOCO bounding box format is
      (xmin, ymin, width, height) in pixel coordinates.
    ALBUMENTATIONS: The Albumentations bounding box format is
      (xmin, ymin, xmax, ymax), normalized by the image dimension
      into the range [0,1]
    YOLO: The Yolo bounding box format is
      (x_center, y_center, width, height), normalized by the image
      dimensions into the range [0,1]
  """
  TENSORFLOW = 'tensorflow'
  VOC = 'voc'
  COCO = 'coco'
  ALBUMENTATIONS = 'albumentations'
  YOLO = 'yolo'


@enum.unique
class DatasetStatistics(enum.Enum):
  """An enum for datasets statistics required for Masterful's normalization."""
  CIFAR_10_MEAN = [0.4914, 0.4822, 0.4465]
  CIFAR_10_STD = [0.247, 0.243, 0.261]
  CIFAR_10_BGR_255 = [113.8575, 122.961, 125.307]
  CIFAR_100_MEAN = [0.5071, 0.4867, 0.4408]
  CIFAR_100_STD = [0.2675, 0.2565, 0.2761]
  CIFAR_100_BGR_255 = [129.3105, 124.1085, 112.404]
  IMAGENET_MEAN = [0.485, 0.456, 0.406]
  IMAGENET_STD = [0.229, 0.224, 0.225]
  IMAGENET_MEAN_BGR_255 = [103.939, 116.779, 123.68]
