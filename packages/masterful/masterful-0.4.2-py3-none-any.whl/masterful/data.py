""" Data parameters and algorithms. """
from dataclasses import dataclass
import tensorflow as tf
from typing import Optional, Sequence, Tuple

import masterful.enums


@dataclass
class DataParams:
  """Parameters describing the datasets used during training.

  These parameters describe both the structure of the dataset
  (image and label shapes for examples) as well as semantic
  structure of the labels (the bounding box format for example,
  or whether or not the labels are sparse or dense).

  Args:
    num_classes: The number of possible classes in the dataset.
    task: The task this dataset will be used for.
    image_shape: The input shape of image data in the dataset,
      in the format (height, width, channels) if `input_channels_last=True`,
      otherwise (channels, height, width) if `input_channels_last=False`.
    image_range: The range of pixels in the input image space that
      of the dataset.
    image_dtype: The image data type in the dataset.
    image_channels_last: The ordering of the dimensions in the inputs.
      `input_channels_last=True` corresponds to inputs with shape
      (height, width, channels) while `input_channels_last=False`
      corresponds to inputs with shape (channels, height, width). Defaults
      to True.
    label_dtype: The data type of the labels.
    label_shape: The shape of the labels.
    label_structure: The tensor format of the label examples.
    label_sparse: True if the labels are in sparse format, False
      for dense (one-hot) labels.
    label_bounding_box_format: The format of bounding boxes in the label,
      if they exist.
  """
  num_classes: int = None
  task: "masterful.enums.Task" = None

  image_shape: Tuple = None
  image_range: "masterful.enums.ImageRange" = None
  image_dtype: tf.dtypes.DType = None
  image_channels_last: bool = True

  label_dtype: type = None
  label_shape: Tuple = None
  label_structure: "masterful.enums.TensorStructure" = None
  label_sparse: bool = None
  label_bounding_box_format: Optional[
      "masterful.enums.BoundingBoxFormat"] = None

  @property
  def image_width(self) -> int:
    """Gets the width of the images in this dataset."""
    if len(self.image_shape) > 2:
      return (self.image_shape[1]
              if self.image_channels_last else self.image_shape[2])
    else:
      return self.image_shape[1]

  @property
  def image_height(self) -> int:
    """Gets the height of the images in this dataset."""
    if len(self.image_shape) > 2:
      return (self.image_shape[0]
              if self.image_channels_last else self.image_shape[1])
    else:
      return self.image_shape[0]

  @property
  def image_channels(self) -> int:
    """Gets the number of channels in the images in this dataset."""
    if len(self.image_shape) > 2:
      return (self.image_shape[2]
              if self.image_channels_last else self.image_shape[0])
    else:
      return 0


def learn_data_params(
    dataset: "masterful.data.DatasetLike",
    image_range: "masterful.enums.ImageRange",
    num_classes: int,
    sparse_labels: bool,
    task: "masterful.enums.Task",
    bounding_box_format: "masterful.enums.BoundingBoxFormat" = None,
) -> DataParams:
  """Learns the :class:`DataParams` for the given dataset.

  Most parameters can be introspected from the dataset itself.
  Anything that cannot be introspected is passed into this function
  as an argument, or set on the :class:`DataParams` after creation.

  Example:

  .. code-block:: python

    training_dataset: tf.data.Dataset = ...
    dataset_params = masterful.data.learn_data_params(
        dataset=training_dataset,
        image_range=masterful.enums.ImageRange.ZERO_255,
        num_classes=10,
        sparse_labels=False,
        task=masterful.enums.Task.CLASSIFICATION)

  Args:
    dataset: A `tf.data.Dataset` instance to learn the parameters for.
    image_range: The range of pixels in the input image space that
      of the dataset.
    num_classes: The number of possible classes in the dataset.
    sparse_labels: True if the labels are in sparse format, False
      for dense (one-hot) labels.
    task: The task this dataset will be used for.
    bounding_box_format: The format of bounding boxes in the label,
      if they exist.

  Returns:
    A new instance of DataParams describing the passed in dataset.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


def learn_data_params_for_datasets(
    datasets: Sequence["masterful.data.DatasetLike"],
    image_range: "masterful.enums.ImageRange",
    num_classes: int,
    sparse_labels: Sequence[bool],
    task: "masterful.enums.Task",
    bounding_box_format: "masterful.enums.BoundingBoxFormat" = None,
) -> Sequence[DataParams]:
  """Learns the :class:`DataParams` for the given datasets.

  Convenience method for learning the data parameters for multiple
  datasets at a time.

  Example:

  .. code-block:: python

    # Learn parameters for three datasets at the same time
    training_dataset: tf.data.Dataset = ...
    validation_dataset: tf.data.Dataset = ...
    test_dataset: tf.data.Dataset = ...

    (training_dataset_params, validation_dataset_params, test_dataset_params) = masterful.data.learn_data_params(
        datasets=[training_dataset, validation_dataset, test_dataset),
        image_range=masterful.enums.ImageRange.ZERO_255,
        num_classes=10,
        sparse_labels=[False, False, False],
        task=masterful.enums.Task.CLASSIFICATION)


  Args:
    datasets: A list/tuple of `tf.data.Dataset` instance to learn the parameters for.
    image_range: The range of pixels in the input image space that
      of the dataset.
    num_classes: The number of possible classes in the dataset.
    sparse_labels: A list/tuple of True if the labels are in sparse format, False
      for dense (one-hot) labels.
    task: The task this dataset will be used for.
    bounding_box_format: The format of bounding boxes in the label,
      if they exist.

  Returns:
    A sequence of DataParams instances describing the passed in datasets.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )
