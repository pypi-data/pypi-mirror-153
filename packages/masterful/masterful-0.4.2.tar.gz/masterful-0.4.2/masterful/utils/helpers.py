"""Convenience functions."""
import tensorflow as tf
import typing


def learn_architecture_and_data_params(
    model: tf.keras.Model,
    datasets: typing.Sequence["masterful.data.DatasetLike"],
    task: "masterful.enums.Task",
    image_range: "masterful.enums.ImageRange",
    num_classes: int,
    prediction_logits: bool,
    backbone_only: bool = False,
    ensemble_multiplier: int = 1,
    sparse_labels: typing.Sequence[typing.Optional[bool]] = [],
    bounding_box_format: "masterful.enums.BoundingBoxFormat" = None,
) -> typing.Tuple["masterful.architecture.ArchitectureParams",
                  typing.Sequence["masterful.data.DataParams"]]:
  """Convenience function to jointly learn Architecture and Data Params.

  This function can help reduce the boilerplate necessary
  to learn the data and architecture parameters for your
  dataset(s) and models. In particular, you can jointly learn
  the data parameters for your training, test, unlabeled, and
  validation datasets in one function call. Importantly, they must
  all have the same image and label formats, and the
  model must also accept the same image format. If these
  conditions do not hold, then use the individual learners
  to find the correct parameters.

  Example:

  .. code-block:: python

    model: tf.keras.Model = ...
    training_dataset: tf.data.Dataset = ...
    unlabeled_dataset: td.data.Dataset = ...

    model_params, (training_dataset_params, unlabeled_dataset_params = masterful.training.learn_architecture_and_data_params(
        model=model,
        datasets=[training_dataset, unlabeled_dataset],
        task=masterful.enums.Task.CLASSIFICATION,
        image_range=masterful.enums.ImageRange.ZERO_255,
        num_classes=10,
        prediction_logits=True,
        sparse_labels=[False, None])

  Args:
    model: The model to learn the parameters for.
    datasets: A `tf.data.Dataset` instance to learn the parameters for.
    task: A semantic description of the a model's predictions or groundtruth
      labels, such as single-label classification (CIFAR10/Imagenet) and
      detection (COCO).
    image_range: The range of pixels in the input image space that
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
    ensemble_multiplier: The number of models to train as part of an ensemble.
      Defaults to 1, which disables ensembling and trains only a single model.
    sparse_labels: True if the labels are in sparse format, False
      for dense (one-hot) labels. Sequence of the same length as `datasets`.
    bounding_box_format: The format of bounding boxes in the label,
      if they exist.

  Returns:
    Tuple containing the model and a list containing the data parameters.
  """
  import masterful.architecture
  import masterful.data
  architecture_params = masterful.architecture.learn_architecture_params(
      model=model, task=task, input_range=image_range, num_classes=num_classes, prediction_logits=prediction_logits,
      backbone_only=backbone_only, ensemble_multiplier=ensemble_multiplier)

  # Learn all of the dataset parameters
  dataset_params = []
  if len(datasets) != len(sparse_labels):
    raise ValueError(
        "Arguments datasets and sparse_labels must have the same number of elements."
    )
  for i, dataset in enumerate(datasets):
    params = masterful.data.learn_data_params(dataset=dataset, image_range=image_range, task=task,
                                              num_classes=num_classes, sparse_labels=sparse_labels[i],
                                              bounding_box_format=bounding_box_format,)
    dataset_params.append(params)
  return architecture_params, dataset_params