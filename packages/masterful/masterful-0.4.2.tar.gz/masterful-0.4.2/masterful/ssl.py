"""Parameters and algorithms for semi-supervised learning."""
from typing import Optional, Sequence, Tuple
from dataclasses import dataclass, field

import tensorflow as tf


@dataclass
class SemiSupervisedParams:
  """Parameters which control the semi-supervised learning aspects of Masterful training.

  In this context, semi-supervised learning incorporates self training,
  self-supervised learning, and traditional semi-supervised learning
  (any learning with a combination of labeled and unlabeled data).

  Args:
    algorithms: An optional list of semi-supervised learning algorithms
      to use during training. Can be any combination of
      ["noisy_student", "barlow_twins"]. Defaults to `["noisy_student"]`
  """
  algorithms: Optional[Sequence[str]] = field(
      default_factory=lambda: ["noisy_student"])


def learn_ssl_params(
    training_dataset: "masterful.data.DatasetLike",
    training_dataset_params: "masterful.data.DataParams",
    unlabeled_datasets: Optional[Sequence[Tuple[
        "masterful.data.DatasetLike", "masterful.data.DataParams"]]] = None,
    synthetic_datasets: Optional[Sequence[Tuple[
        "masterful.data.DatasetLike", "masterful.data.DataParams"]]] = None,
) -> SemiSupervisedParams:
  """Learns the optimal set of semi-supervised learning parameters to use during training.

  Example:

  .. code-block:: python

    training_dataset: tf.data.Dataset = ...
    training_dataset_params: masterful.data.params.DataParams = ...
    ssl_params = masterful.ssl.learn_ssl_params(training_dataset,
                                                training_dataset_params)

  Args:
    training_dataset: The labeled dataset to use during training.
    training_dataset_params: The parameters of the labeled dataset.
    unlabeled_datasets: Optional sequence of unlabled datasets and their
      parameters, to use during training. If an unlabeled dataset is
      specified, then a set of algorithms must be specified in `ssl_params`
      otherwise this will have no effect.
    synthetic_datasets: Optional sequence of synthetic data and parameters
      to use during training. The amount of synthetic data used during
      training is controlled by
      :class:`masterful.regularization.RegularizationParams.synthetic_proportion`.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


def analyze_data_then_save_to(
    model: tf.keras.Model,
    labeled_training_data: tf.data.Dataset,
    unlabeled_training_data: tf.data.Dataset,
    path: str,
) -> None:
  """Analyze labeled and unlabeled data then save intermediate results to disk.

  See the Recipe for Simple SSL guide :doc:/notebooks/guide_simple_ssl
  for more details.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    training_dataset: tf.data.Dataset = ...
    unlabeled_dataset: tf.data.Dataset = ...
    masterful.ssl.analyze_data_then_save_to(
        model, training_dataset, unlabeled_dataset, path='/tmp/ssl')

  Args:
    model: A trained model. The output must be probabilities, in
      other words, your model's final layer should be a softmax
      or sigmoid activation.

      If your model finishes with a `tf.keras.layers.Dense` layer,
      without an activation, then it's said to be 'outputting logits'.
      In that case, typically you'll use a loss function initialized with
      `from_logits=True`. If this describes your model, you can simply
      attach an extra sigmoid or softmax activation to your model and pass
      the new model into this function. You do not need to change your original
      model, loss function, or training loop.
      For example, the model below outputs logits:
      ```python
      m = tf.keras.Sequential([tf.keras.Input((32,32,3)),
                               tf.keras.layers.Dense(10)])
      ```

      To use this model, attach a softmax activation:
      ```
      activated_model = tf.keras.Sequential([m, tf.keras.layers.Softmax()])
      masterful.ssl.save_data(activated_model, ...)
      ```

    architecture_params: Parameters about the model architecture.

    labeled_training_data: Labeled training data as a tf.data.Dataset.
      The data should be batched. Each example should have the
      following structure: `(original_images, original_labels)`.

    labeled_training_data_params: Params that describe the labeled training data.

    unlabeled_training_data: Unlabeled training data as a tf.data.Dataset.
      The data should be batched. Each example should be a tensor of
      images.

    unlabeled_training_data_params: Params that describe the unlabeled training data.

    path: The filepath to save to.

    Raises:
      ValueError:	If the path is empty or malformed.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


def load_from(path: str,
              unlabeled_weight: Optional[float] = 1.0) -> tf.data.Dataset:
  """Load data from disk into a tf.data.Dataset.

  Please see the Recipe for Simple SSL guide for more details.

  Example:

  .. code-block:: python

    ssl_training_dataset = masterful.ssl.load_from(path='/tmp/ssl')

  Args:
    path: The location on disk to load from.
    unlabeled_weight: A weighting for the unlabeled data.

  Returns:
    A dataset ready to be trained against. The dataset is unbatched. If unlabeled_weight
      is specified, and not set to 1.0, the dataset elements are (image, label, weight),
      where weight is 1.0 for labeled data unlabeled_weight for unlabeled data. Otherwise,
      the dataset elements are (image, label).

  Raises:
    ValueError:	If the path is empty or malformed.
    FileNotFound: If the path does not point to a valid file on disk.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


def distill(
    source_model: tf.keras.Model,
    source_model_params: "masterful.architecture.ArchitectureParams",
    target_model: tf.keras.Model,
    target_model_params: "masterful.architecture.ArchitectureParams",
    optimization_params: Optional["masterful.optimization.OptimizationParams"],
    training_dataset: Optional[tf.data.Dataset],
    training_dataset_params: Optional["masterful.data.DataParams"],
    unlabeled_datasets: Optional[Sequence[Tuple[
        tf.data.Dataset, "masterful.data.DataParams"]]] = None,
    synthetic_datasets: Optional[Sequence[Tuple[
        tf.data.Dataset, "masterful.data.DataParams"]]] = None,
    **kwargs,
) -> "masterful.training.TrainingReport":
  """Distills the knowledge from `source_model` into `target_model`.

  Example:

  .. code-block:: python

    teacher_model: tf.keras.Model = ...
    teacher_model_params: masterful.architecture.params.ArchitectureParams = ...
    student_model: tf.keras.Model = ...
    student_model_params: masterful.architecture.params.ArchitectureParams = ...
    optimization_params: masterful.optimization.params.OptimizationParams = ...
    training_dataset: tf.data.Dataset = ...
    training_dataset_params: masterful.data.params.DataParams = ...
    training_report = masterful.ssl.distill(
        source_model=teacher_model,
        source_model_params=teacher_model_params,
        target_model=student_model,
        target_model_params=student_model_params,
        optimization_params=optimization_params,
        training_dataset=training_dataset,
        training_dataset_params=training_dataset_params)

  Args:
    source_model: The source model that we are trying to match. This model
      is already trained.
    source_model_params: The parameters of the source model.
    target_model: The target model that we are training.
    target_model_params: The parameters of the target model.
    training_dataset: The labeled data to use for training the model. Labeled
      data must be unbatched, and use the Keras formulation of
      (image, label) for each mini-batch of data.
    training_dataset_params: The parameters of the training dataset.
    unlabeled_datasets: [Optional] A set of unlabeled datasets and their parameters
      which can be used to improve the training of the model through semi-supervised
      and unsupervised techniques.
    synthetic_datasets: [Optional] A set of labeled, synthetic data and their parameters
      that can be used to improve the performance of the model.

  Returns:
    An instance of :class:`masterful.training.TrainingReport`,
    containing the results of distilling `source_model` into `target_model`.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )


def learn_representation(
    model: tf.keras.Model,
    model_params: "masterful.data.DataParams",
    optimization_params: "masterful.optimization.OptimizationParams",
    ssl_params: "masterful.ssl.SemiSupervisedParams",
    training_dataset: Optional[tf.data.Dataset] = None,
    training_dataset_params: Optional["masterful.data.DataParams"] = None,
    validation_dataset: Optional[tf.data.Dataset] = None,
    validation_dataset_params: Optional["masterful.data.DataParams"] = None,
    unlabeled_datasets: Optional[Sequence[Tuple[
        tf.data.Dataset, "masterful.data.DataParams"]]] = None,
    synthetic_datasets: Optional[Sequence[Tuple[
        tf.data.Dataset, "masterful.data.DataParams"]]] = None,
    **kwargs,
) -> "masterful.training.TrainingReport":
  """
  Pretrain the weights of the given model using the provided datasets. The model
  is assumed to be the feature extractor (backbone) of a larger model, so there
  should be no classification heads (softmax output) in the model provided.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    model_params: masterful.architecture.params.ArchitectureParams = ...
    optimization_params: masterful.optimization.params.OptimizationParams = ...
    ssl_params: masterful.ssl.params.SemiSupervisedParams = ...
    training_dataset: tf.data.Dataset = ...
    training_dataset_params: masterful.data.params.DataParams = ...
    validation_dataset: tf.data.Dataset = ...
    validation_dataset_params: masterful.data.params.DataParams = ...
    training_report = masterful.ssl.learn_representation(
        model=model,
        model_params=model_params,
        optimization_params=optimization_params,
        ssl_params=ssl_params,
        training_dataset=training_dataset,
        training_dataset_params=training_dataset_params,
        validation_dataset=validation_dataset,
        validation_dataset_params=validation_dataset_params)

  Args:
    model: The model to pretrain. Models used here should have no classification
      head attached.
    model_params: The parameters of the model to train.
    training_dataset: The labeled data to use for training the model. Labeled
      data must be unbatched, and use the Keras formulation of
      (image, label) for each mini-batch of data.
    training_dataset_params: The parameters of the training dataset.
    validation_dataset: The labeled data to use for validating the model. Labeled
      data must be unbatched, and use the Keras formulation of
      (image, label) for each mini-batch of data.
    validation_dataset_params: The parameters of the validation dataset.
    unlabeled_datasets: [Optional] A set of unlabeled datasets and their parameters
      which can be used to improve the training of the model through semi-supervised
      and unsupervised techniques.
    synthetic_datasets: [Optional] A set of labeled, synthetic data and their parameters
      that can be used to improve the performance of the model.

  Returns:
    An instance of :class:`FitReport`, containing the results of pretraining
    the model. In order to measure the performance of pretraining, a small task
    specific head is temporarily attached and trained at the end to measure the
    performance of the pretraining task.
  """
  raise RuntimeError(
      "Please call masterful.register() with your account ID and authorization key before using the API."
  )
