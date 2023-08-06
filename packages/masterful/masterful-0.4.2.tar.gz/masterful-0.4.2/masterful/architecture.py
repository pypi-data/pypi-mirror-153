""" Model architecture. """
from dataclasses import dataclass
import tensorflow as tf
from typing import Dict, Tuple


@dataclass
class ArchitectureParams:
  """Model architecture parameters.

  Parameters describing the model architecture used during training.
  These parameters describe structural attributes of the model,
  like input and output shapes, as well as higher order semantic
  parameters such as the task the model is attempting to solve.

  Args:
    task: A semantic description of the a model's predictions or groundtruth
      labels, such as single-label classification (CIFAR10/Imagenet) and
      detection (COCO).
    num_classes: The number of possible classes in the model prediction.
    ensemble_multiplier: The number of models to train as part of an ensemble.
      Defaults to 1, which disables ensembling and trains only a single model.
    custom_objects: Some TF/Keras models have custom objects (layers,
      initializers, etc). If so, in order to load/save/clone the model, you
      need to let TF/Keras know how to load/save them. A dictionary of class
      mappings is the typical way to do this.
    model_config: If the model is a Tensorflow Object Detection model,
      this is the configuration used to build the model.
    backbone_only: True if this model represents a backbone (feature extractor)
      only, without a classification or task specific head.
    input_shape: The input shape of image data the model expects,
      in the format (height, width, channels) if `input_channels_last=True`,
      otherwise (channels, height, width) if `input_channels_last=False`.
    input_range: The range of pixels in the input image space that
      the model is expecting.
    input_dtype: The image data type the model expects.
    input_channels_last: The ordering of the dimensions in the inputs.
      `input_channels_last=True` corresponds to inputs with shape
      (height, width, channels) while `input_channels_last=False`
      corresponds to inputs with shape (channels, height, width). Defaults
      to True.

    prediction_logits: True the model's output prediction is has no activation
      function. False means the model output is activated with a sigmoid
      or softmax layer.
    prediction_dtype: The dtype of the predictions.
    prediction_structure: The tensor structure of the model predictions.
    prediction_shape: The tensor shape of the model predictions. Only valid
      if the `prediction_structure` corresponds to `SINGLE_TENSOR`.
  """
  task: "masterful.enums.Task" = None
  num_classes: int = None
  ensemble_multiplier: int = 1
  custom_objects: Dict = None
  model_config: "object_detection.protos.model.DetectionModel" = None
  backbone_only: bool = False

  input_shape: Tuple = None
  input_range: "masterful.enums.ImageRange" = None
  input_dtype: tf.dtypes.DType = None
  input_channels_last: bool = True

  prediction_logits: bool = None
  prediction_dtype: tf.dtypes.DType = None
  prediction_structure: "masterful.enums.TensorStructure" = None
  prediction_shape: Tuple = None

  @property
  def input_width(self) -> int:
    """Gets the width of the model input."""
    if len(self.input_shape) > 2:
      return (self.input_shape[1]
              if self.input_channels_last else self.input_shape[2])
    else:
      return self.input_shape[1]

  @property
  def input_height(self) -> int:
    """Gets the height of the model input."""
    if len(self.input_shape) > 2:
      return (self.input_shape[0]
              if self.input_channels_last else self.input_shape[1])
    else:
      return self.input_shape[0]

  @property
  def input_channels(self) -> int:
    """Gets the number of channels in the model input."""
    if len(self.input_shape) > 2:
      return (self.input_shape[2]
              if self.input_channels_last else self.input_shape[0])
    else:
      return 0


def learn_architecture_params(
    model: tf.keras.Model,
    task: "masterful.enums.Task",
    input_range: "masterful.enums.ImageRange",
    num_classes: int,
    prediction_logits: bool,
    custom_objects: Dict = {},
    backbone_only: bool = False,
) -> ArchitectureParams:
  """Architecture parameter learner.

  Learns the parameters of the given model. Most attributes can
  be introspected from the model itself. Any attributes that
  cannot be introspected can be passed into the function, or set
  on the :class:`ArchitectureParams` after creation.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    architecture_params = masterful.architecture.learn_architecture_params(
        model=model,
        task=masterful.enums.Task.CLASSIFICATION,
        input_range=masterful.enums.ImageRange.ZERO_255,
        num_classes=10,
        prediction_logits=False)

  Args:
    model: The model to learn the parameters for.
    task: A semantic description of the a model's predictions or groundtruth
      labels, such as single-label classification (CIFAR10/Imagenet) and
      detection (COCO).
    input_range: The range of pixels in the input image space that
      the model is expecting.
    num_classes: The number of possible classes in the model prediction.
      If the model is a backbone only, then this should still be provided
      and represents the number of classes that should exist in in the
      classification head of the model.
    prediction_logits: True the model's output prediction is has no activation
      function. False means the model output is activated with a sigmoid
      or softmax layer.
    custom_objects: Some TF/Keras models have custom objects (layers,
      initializers, etc). If so, in order to load/save/clone the model, you
      need to let TF/Keras know how to load/save them. A dictionary of class
      mappings is the typical way to do this.
    backbone_only: True if this model represents a backbone (feature extractor)
      only, without a classification or task specific head. Defaults to False.

  Returns:
    An instance of :class:`ArchitectureParams` describing the attributes
    of the model.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )
