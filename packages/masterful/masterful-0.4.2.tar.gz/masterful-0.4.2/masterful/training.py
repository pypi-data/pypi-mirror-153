"""Model training using the Masterful platform. """
import dataclasses
import tensorflow as tf
from typing import Dict, Optional, Sequence, Tuple


@dataclasses.dataclass
class TrainingReport:
  """Structure which holds the results of a training run.

  Args:
    validation_results: The final results from evaluating the model
      on the validation set.
    gpu_info: A list of GpuInfo objects, with relevant gpu usage information.
    history: The full training history report, containing the results at the
      end of each epoch for key metrics.
    model: A reference to the trained model. This will be different
      than the model passed in for training if `model_ensemble` is
      greater than 1.
  """
  validation_results: Dict[str, float] = None
  gpu_info: Sequence["masterful.utils.gpu.GpuInfo"] = None
  history: tf.keras.callbacks.History = None
  model: Optional[tf.keras.Model] = None


def train(
    model: tf.keras.Model,
    model_params: "masterful.architecture.ArchitectureParams",
    optimization_params: "masterful.optimization.OptimizationParams",
    regularization_params: "masterful.regularization.RegularizationParams",
    ssl_params: "masterful.ssl.SemiSupervisedParams",
    training_dataset: "masterful.data.DatasetLike",
    training_dataset_params: "masterful.data.DataParams",
    validation_dataset: Optional["masterful.data.DatasetLike"] = None,
    validation_dataset_params: Optional["masterful.data.DataParams"] = None,
    unlabeled_datasets: Optional[Sequence[Tuple[
        "masterful.data.DatasetLike", "masterful.data.DataParams"]]] = None,
    synthetic_datasets: Optional[Sequence[Tuple[
        "masterful.data.DatasetLike", "masterful.data.DataParams"]]] = None,
    **kwargs) -> TrainingReport:
  """Trains a model using the Masterful platform.

  The model passed into this function will be trained against
  the passed in datasets using the given parameters for
  regularization, optimization, and semi-supervised learning.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    model_params: masterful.architecture.params.ArchitectureParams = ...
    optimization_params: masterful.optimization.params.OptimizationParams = ...
    regularization_params: masterful.regularization.RegularizationParams = ...
    ssl_params: masterful.ssl.params.SemiSupervisedParams = ...
    training_dataset: tf.data.Dataset = ...
    training_dataset_params: masterful.data.params.DataParams = ...
    training_report = masterful.training.train(
        model=model,
        model_params=model_params,
        optimization_params=optimization_params,
        regularization_params=regularization_params,
        ssl_params=ssl_params,
        training_dataset=training_dataset,
        training_dataset_params=training_dataset_params)

  Args:
    model: The model to train.
    model_params: Parameters of the model to train.
    optimizer_params: Parameters to use for optimization. These
      can be created directly, or found automatically using
      :func:`masterful.optimization.learn_optimization_params`.
    regularization_params: Parameters to use for regularization.
      These can be created directly, or found automatically using
      :func:`masterful.regularization.learn_regularization_params`.
    ssl_params: Parameters to use for semi-supervised training.
      These can be created directly, or learned automatically
      using :func:`masterful.ssl.learn_ssl_params`.
    training_dataset: The labeled dataset to use during training.
    training_dataset_params: The parameters of the labeled dataset.
    validation_dataset: An optional validation dataset to use during
      training. If no validation set is specified, Masterful will
      autmoatically create one from the labeled dataset.
    validation_dataset_params: Optional parameters of the validation dataset.
    unlabeled_datasets: Optional sequence of unlabled datasets and their
      parameters, to use during training. If an unlabeled dataset is
      specified, then a set of algorithms must be specified in `ssl_params`
      otherwise this will have no effect.
    synthetic_datasets: Optional sequence of synthetic data and parameters
      to use during training. The amount of synthetic data used during
      training is controlled by
      :class:`masterful.regularization.RegularizationParams.synthetic_proportion`.

  Returns:
    An instance of :class:`TrainingReport` with the full results
    of training the model with the given parameters.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


def _ensemble(
    model: tf.keras.Model,
    model_params: "masterful.architecture.ArchitectureParams",
    optimization_params: "masterful.optimization.OptimizationParams",
    regularization_params: "masterful.regularization.RegularizationParams",
    ssl_params: "masterful.ssl.SemiSupervisedParams",
    training_dataset: tf.data.Dataset,
    training_dataset_params: "masterful.data.DataParams",
    validation_dataset: Optional[tf.data.Dataset] = None,
    validation_dataset_params: Optional["masterful.data.DataParams"] = None,
    unlabeled_datasets: Optional[Sequence[Tuple[
        tf.data.Dataset, "masterful.data.DataParams"]]] = None,
    synthetic_datasets: Optional[Sequence[Tuple[
        tf.data.Dataset, "masterful.data.DataParams"]]] = None,
    **kwargs,
) -> TrainingReport:
  """
  Similar to :py:func:`masterful.training.train`, trains the given model on the
  provided datasets using the policy provided. However,
  this function trains `model_parms.ensemble_multiplier`
  models in sequence, and returns an ensembled model
  which is the joint prediction from all child models.

  Args:
    model: The model to train.
    model_params: Parameters of the model to train.
    optimizer_params: Parameters to use for optimization. These
      can be created directly, or found automatically using
      :func:`masterful.optimization.learn`.
    regularization_params: Parameters to use for regularization.
      These can be created directly, or found automatically using
      :func:`masterful.regularization.learn`.
    ssl_params: Parameters to use for semi-supervised training.
      These can be created directly, or learned automatically
      using :func:`masterful.ssl.learn`.
    training_dataset: The labeled dataset to use during training.
    training_dataset_params: The parameters of the labeled dataset.
    validation_dataset: An optional validation dataset to use during
      training. If no validation set is specified, Masterful will
      autmoatically create one from the labeled dataset.
    validation_dataset_params: Optional parameters of the validation dataset.
    unlabeled_datasets: Optional sequence of unlabled datasets and their
      parameters, to use during training. If an unlabeled dataset is
      specified, then a set of algorithms must be specified in `ssl_params`
      otherwise this will have no effect.
    synthetic_datasets: Optional sequence of synthetic data and parameters
      to use during training. The amount of synthetic data used during
      training is controlled by
      :class:`masterful.regularization.RegularizationParams.synthetic_proportion`.

  Returns:
    An instance of :class:`TrainingReport` with the full results
    of training the model with the given parameters.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )
