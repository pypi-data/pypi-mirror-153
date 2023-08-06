"""Optimization focused parameters and learning algorithms. """
from dataclasses import dataclass
import tensorflow as tf
from typing import Dict, Optional, Sequence, Union


@dataclass
class OptimizationParams:
  """Parameters controlling the optimization of the model during training.

  Optimization means finding the best weights for a
  model and training data. Optimization is different from
  regularization because optimization does not consider
  generalization to unseen data. The central challenge of
  optimization is speed - find the best weights faster.

  Args:
    batch_size: Batch size of the features and labels to use
      during training.
    drop_remainder: True if any examples that do not fit evenly
      into a full batch should be dropped, False otherwise. If False,
      the last batch during training may or may not equal `batch_size`.
    epochs: The number of epochs to train for. An epoch is defined
      as one full sweep through the training data.
    learning_rate: The initial learning rate to use for training. This
      will also be the starting learning rate post-warmup, if warmup
      is specified.
    learning_rate_schedule: An instance if :class:`tf.keras.optimizers.schedules.LearningRateSchedule`
      which modulate how the learning rate of your optimizer changes over time.
      Only one of `learning_rate_schedule` or `learning_rate_callback`
      must be set.
    learning_rate_callback: An instance of :class:`tf.keras.callbacks.Callback`
      which modulate how the learning rate of your optimizer changes over time.
      Only one of `learning_rate_schedule` or `learning_rate_callback`
      must be set.
    warmup_learning_rate: The initial learning rate to use during warmup.
      If `warmup_epochs` is greater than zero, the learning rate will
      linearly grow from `warmup_learning_rate` to `learning_rate` over
      `warmup_epochs` training epochs, incrementing at each step in
      each epoch.
    warmup_epochs: The number of epochs to perform model warmup during
      training. An epoch is defined as one full sweep through the
      training data.
    optimizer: An instance of :class:`tf.keras.optimizers.Optimizer`,
      to use as the optimizer during training.
    loss: An instance of :class:`tf.keras.losses.Loss`, which is the
      function that will be optmized by the optimizer. If the model
      support multiple outputs, this can be a dictionary of loss functions.
    loss_weights: Optional list or dictionary specifying scalar
      coefficients (Python floats) to weight the loss
      contributions of different model outputs. The loss value
      that will be minimized by the model will then be the
      weighted sum of all individual losses, weighted by the
      loss_weights coefficients. If a list, it is expected to
      have a 1:1 mapping to the model's outputs. If a dict,
      it is expected to map output names (strings) to scalar
      coefficients.
    early_stopping_callback: An instance of :class:`tf.keras.callbacks.Callback`
      which can stop training before `total_steps` have been reached depending
      on certain conditions.
    metrics: An optional list of additional metrics that will be measured
      and reported during training.
    readonly_callbacks: An optional list of callbacks to pass to the
      training loop. These callbacks must be readonly. They must not
      attempt to modify any parameters of the training loop, other
      than entries in the logs.
  """
  batch_size: int = None
  drop_remainder: bool = False
  epochs: int = None

  learning_rate: float = None
  learning_rate_schedule: Optional[
      tf.keras.optimizers.schedules.LearningRateSchedule] = None
  learning_rate_callback: Optional[tf.keras.callbacks.Callback] = None

  warmup_learning_rate: float = None
  warmup_epochs: int = None

  optimizer: tf.keras.optimizers.Optimizer = None
  loss: Union[tf.keras.losses.Loss, Dict[str, tf.keras.losses.Loss]] = None
  loss_weights: Union[Sequence, Dict] = None
  early_stopping_callback: Optional[tf.keras.callbacks.Callback] = None

  metrics: Optional[Sequence[tf.keras.metrics.Metric]] = None
  readonly_callbacks: Optional[Sequence[tf.keras.callbacks.Callback]] = None


def learn_optimization_params(
    model: tf.keras.Model,
    model_params: "masterful.architecture.ArchitectureParams",
    dataset: "masterful.data.DatasetLike",
    dataset_params: "masterful.data.DataParams",
    **kwargs,
) -> OptimizationParams:
  """Learns the optimal set of optimization parameters for training.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    model_params: masterful.architecture.params.ArchitectureParams = ...
    training_dataset: tf.data.Dataset = ...
    training_dataset_params: masterful.data.params.DataParams = ...
    optimization_params = masterful.optimization.learn_optimization_params(
        model, model_params, training_dataset, training_dataset_params)

  Args:
    model: The model to learn the optimal set of parameters for.
    model_params: The parameters of the given model.
    dataset: The dataset to learn the optimization parameters for.
    dataset_params: Parameters of the dataset used.

  Returns:
    An instance of :class:`OptimizationParams` that can be used during
    training.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )
