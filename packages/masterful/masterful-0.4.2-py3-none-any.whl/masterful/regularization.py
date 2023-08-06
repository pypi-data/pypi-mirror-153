"""Regularization focused parameters and learning algorithms. """
import dataclasses
import numpy as np
import tensorflow as tf
from typing import Dict, Optional, Sequence, Tuple


@dataclasses.dataclass
class RegularizationParams:
  """Parameters controlling the regularization of the model during training.

  Regularization involves helping a model generalize
  to data it has not yet seen. Another way of saying this is that
  regularization is about fighting overfitting.

  Masterful supports a range of different augmentations in order
  to regularize the model during training. The core concept behind
  the Masterful augmentation strategy is "augmentation clustering",
  which groups structurally similar augmentations together
  (for example, color space augmentations are one group, spatial
  augmentations are another). In order to support this, we
  measure a range of different magnitudes for each cluster (the
  xxx_magnitude_table), the index of the magnitude selected for each
  cluster (xxx_cluster_to_index), and finally the optimal magnitude
  chosen for each cluster. Masterful automatically determines
  each cluster size and potential magnitude by measuring the
  "distance" each each augmentation moves the loss of the model.
  This is the "Distance Analysis" phase in the console output.

  Args:
    shuffle_buffer_size: The size of the shuffle buffer to use
      during training. If None or 0, the shuffle buffer size will
      be found automatically based on memory capacity.
    mirror: Specifies whether to apply mirror augmentation during
      training as part of the augmentation pipeline. Must be set to
      0.0 (off) or 1.0 (on).
    rot90: Specifies whether to apply a random discrete rotation during
      training as part of the augmentation pipeline. This will perform
      a random, discrete rotation of either  90, 180, or 270 degress. Must
      be set to either 0.0 (off) or 1.0 (on).
    rotate: Specifies whether to apply a random rotation during training
      as part of the augmentation pipeline. Must be an integer in the range
      [0,100], where 0 specifies no rotation, and 100 specifies maximum
      rotation (180 degrees).
    mixup: Controls Mixup label smoothing, as proposed in
      "mixup: Beyond Empirical Risk Minimization" (https://arxiv.org/abs/1710.09412).
      Must be a float in the range [0.0, 1.0].
    cutmix: Specifies whether to apply cutmix during training as part
      of the data augmentation pipeline. Cutmix was proposed in
      "CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features"
      (https://arxiv.org/abs/1905.04899) and must be a float in the
      range [0.0, 1.0].
    label_smoothing: Controls whether to use label smoothing regularization
      or not. Label Smoothing is a regularization technique that introduces
      noise for the labels. This accounts for the fact that datasets
      may have mistakes in them, so maximizing the likelihood of
      `log p(x|y)` directly can be harmful.
    hsv_cluster: The color space cluster to use during training. This
      is the index to use in order to find the magnitude of the cluster
      in the hsv_magnitude_table. The HSV cluster involves color,
      brightness, and hue jittering augmentations.
    hsv_cluster_to_index: Maps a cluster index to the index of the magnitude
      for that cluster in the hasv_magnitude_table.
    hsv_magnitude_table: A table of magnitudes to use for each cluster.
      The magnitude chosen is specified by `hsv_cluster`.
    contrast_cluster: The contrast cluster to use during training.
      This is the index to use in order to find the magnitude of
      the cluster in the hsv_magnitude_table. The contrast cluster
      involves (auto) contrast, solarize, posterize, and equalize
      augmentations.
    contrast_cluster_to_index: Maps a cluster index to the index of
      the magnitude for that cluster in the contrast_magnitude_table.
    contrast_magnitude_table: A table of magnitudes to use for each
      cluster. The magnitude chosen is specified by `contrast_cluster`.
    blur_cluster: The blur cluster to use during training. This
      is the index to use in order to find the magnitude of the cluster
      in the blur_magnitude_table. The blur contrast involves
      sharpening and desharpening augmentations.
    blur_cluster_to_index: Maps a cluster index to the index of
      the magnitude for that cluster in the blur_magnitude_table.
    blur_magnitude_table: A table of magnitudes to use for each
      cluster. The magnitude chosen is specified by `blur_cluster`.
    spatial_cluster: The spatial cluster to use during training.
      This is the index to use in order to find the magnitude of
      the cluster in the spatial_magnitude_table. The spatial cluster
      involves shear, translate, and zoom augmentations.
    spatial_cluster_to_index: Maps a cluster index to the index of
      the magnitude for that cluster in the spatial_magnitude_table.
    spatial_magnitude_table: A table of magnitudes to use for each
      cluster. The magnitude chosen is specified by `spatial_cluster`.
    synthetic_proportion: If synthetic data is used during training,
      the proportion of synthetic data to use from each dataset. Should
      be a list of floats in the range [0.0, 1.0].
  """
  shuffle_buffer_size: int = None

  mirror: float = None
  rot90: float = None
  rotate: int = None
  mixup: float = None
  cutmix: float = None
  label_smoothing: float = None

  hsv_cluster: int = None
  hsv_cluster_to_index: np.ndarray = None
  hsv_magnitude_table: np.ndarray = None

  contrast_cluster: int = None
  contrast_cluster_to_index: np.ndarray = None
  contrast_magnitude_table: np.ndarray = None

  blur_cluster: int = None
  blur_cluster_to_index: np.ndarray = None
  blur_magnitude_table: np.ndarray = None

  spatial_cluster: int = None
  spatial_cluster_to_index: np.ndarray = None
  spatial_magnitude_table: np.ndarray = None

  synthetic_proportion: Sequence[float] = None

  @staticmethod
  def load_from(path: str) -> 'RegularizationParams':
    """
    Loads the regularization params from the given path.

    Args:
      path: The full path to the regularization parameters to load.

    Returns:
      A new instance of :class:`masterful.regularization.RegularizationParams`.
    """
    raise RuntimeError(
        "Please call masterful.register() with your account ID and authorization key before using the API."
    )

  @staticmethod
  def save_to(params: 'RegularizationParams', path: str):
    """
    Saves the regularization params to the given path.

    Args:
      params: The instance of :class:`masterful.regularization.RegularizationParams` to save.
      path: The fully qualified path of the file to save the params into.
    """
    raise RuntimeError(
        "Please call masterful.register() with your account ID and authorization key before using the API."
    )


def learn_regularization_params(
    model: tf.keras.Model,
    model_params: "masterful.architecture.ArchitectureParams",
    optimization_params: "masterful.optimization.OptimizationParams",
    training_dataset: "masterful.data.DatasetLike",
    training_dataset_params: "masterful.data.DataParams",
    validation_dataset: Optional["masterful.data.DatasetLike"] = None,
    validation_dataset_params: Optional["masterful.data.DataParams"] = None,
    unlabeled_datasets: Optional[Sequence[Tuple[
        "masterful.data.DatasetLike", "masterful.data.DataParams"]]] = None,
    synthetic_datasets: Optional[Sequence[Tuple[
        "masterful.data.DatasetLike", "masterful.data.DataParams"]]] = None,
    **kwargs,
) -> RegularizationParams:
  """
  Learns the optimal set of regularization parameters for the model
  during training. This is dependent on having established the
  :class:`OptimizationParams` to be used during training before
  calling this function.

  This function can take awhile to complete. The expensive part
  of this algorithm is the augmentation learner. In general, this
  function will take around 1.5x the amount of time it takes to
  train your model, in order to learn the optimal set of augmentations
  to use as part of the regularization strategy.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    model_params: masterful.architecture.params.ArchitectureParams = ...
    optimization_params: masterful.optimization.params.OptimizationParams = ...
    training_dataset: tf.data.Dataset = ...
    training_dataset_params: masterful.data.params.DataParams = ...
    regularization_params = masterful.regularization.learn_regularization_params(
        model=model,
        model_params=model_params,
        optimization_params=optimization_params,
        training_dataset=training_dataset,
        training_dataset_params=training_dataset_params)

  Args:
    model: The model to learn the optimal set of regularization
      parameters for.
    model_params: The parameter of the model.
    optimization_params: The optimization parameters to use during training.
    training_dataset: The labeled dataset to use for learning.
    training_dataset_params: The parameters of the labeled dataset.
    validation_dataset: The optional validation dataset used to measure
      progress. If not validation dataset is specified, a small portion
      of the training dataset will be used as the validation set.
    validation_dataset_params: The parameters of the validation dataset.
    unlabeled_datasets: Optional sequence of unlabled datasets and their
      parameters, to use during training. If an unlabeled dataset is
      specified, then a set of algorithms must be specified in `ssl_params`
      otherwise this will have no effect.
    synthetic_datasets: Optional sequence of synthetic data and parameters
      to use during training. The amount of synthetic data used during
      training is controlled by
      :class:`masterful.regularization.RegularizationParams.synthetic_proportion`.

  Returns:
    An instance of :class:`RegularizationParams` describing the
    optimal regularization strategy to use during training.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


parameters = type('', (), {})()

# These parameters were learned using a ResNet-20
# on CIFAR-10.
parameters.CIFAR10_SMALL = RegularizationParams(
    mirror=1.0,
    rot90=0.0,
    rotate=17,
    mixup=0.0,
    cutmix=0.0,
    label_smoothing=0,
    hsv_cluster=3,
    hsv_cluster_to_index=np.array(
        [[2, 4, 7, 11, 11, 11], [2, 5, 7, 11, 11, 11], [1, 2, 3, 4, 6, 11],
         [2, 4, 5, 6, 8, 11], [2, 2, 2, 3, 8, 11]],
        dtype=np.int32),
    hsv_magnitude_table=np.array([[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                  [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                  [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                  [0, 20, 10, 30, 40, 50, 60, 70, 80, 90, 100],
                                  [0, 100, 90, 10, 80, 20, 30, 70, 60, 50, 40]],
                                 dtype=np.int32),
    contrast_cluster=3,
    contrast_cluster_to_index=np.array(
        [[3, 7, 11, 11, 11, 11], [1, 1, 1, 1, 4, 11], [4, 5, 6, 6, 9, 11],
         [1, 2, 5, 8, 11, 11], [1, 2, 4, 6, 11, 11], [2, 4, 5, 6, 7, 11]],
        dtype=np.int32),
    contrast_magnitude_table=np.array(
        [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 10, 20, 50, 40, 30, 60, 70, 100, 80, 90],
         [10, 0, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 20, 10, 30, 40, 50, 60, 70, 80, 90, 100]],
        dtype=np.int32),
    blur_cluster=3,
    blur_cluster_to_index=np.array(
        [[1, 2, 6, 11, 11, 11], [2, 8, 10, 11, 11, 11]], dtype=np.int32),
    blur_magnitude_table=np.array(
        [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 70, 10, 60, 20, 80, 50, 30, 40, 90, 100]],
        dtype=np.int32),
    spatial_cluster=1,
    spatial_cluster_to_index=np.array(
        [[2, 5, 8, 11, 11, 11], [2, 4, 6, 7, 9, 11], [2, 5, 8, 11, 11, 11],
         [1, 2, 3, 4, 6, 11], [3, 5, 7, 9, 11, 11], [1, 1, 1, 2, 7, 11]],
        dtype=np.int32),
    spatial_magnitude_table=np.array(
        [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 100, 10, 90, 20, 80, 30, 70, 60, 40, 50],
         [0, 10, 20, 30, 40, 50, 100, 90, 60, 80, 70],
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
         [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
        dtype=np.int32),
    synthetic_proportion=[0.0])
