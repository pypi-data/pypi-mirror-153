from django.db import models


class PolicySearchTask(models.Model):
  """The main PolicySearchTask model.
  
  The model mirrors the PolicySearchTask proto. Scalar fields are assigned
  similaer fields in the model, everything else is assigned JSON fields.
  """
  # The name of the policy. This is the primary key of the model.
  policy_name = models.CharField(primary_key=True, max_length=250)

  # The name of the approach.
  approach_name = models.CharField(max_length=120)

  # Node search tasks performed in the policy search task.
  node_search_tasks = models.JSONField(default=dict)

  # Metrics specific to the customer model without any Masterful improvements.
  presearch_model_val_metrics = models.JSONField(default=dict)

  # The version of the policy engine that produced this policy.
  engine_version = models.CharField(default="", max_length=100)

  # Whether fit results were captured.
  fit_was_captured = models.BooleanField(default=False)

  # Results of training the model with Masterful's learned policy.
  learned_policy_val_metrics = models.JSONField(default=dict)

  # The type of the ML task the policy is used for.
  task_type = models.CharField(default="COMPUTER_VISION_TASK_UNKNOWN",
                               max_length=250)


class Dataset(models.Model):
  """A model that represents a dataset.
  
  The model mirros the Dataset proto. For full documentation, see proto
  definition.
  """
  # The id of the dataset. This is the primary key of the model.
  dataset_id = models.CharField(primary_key=True, max_length=250)

  # The title of the dataset.
  title = models.CharField(max_length=250)

  # Train split. This is a Split proto.
  train_dataset = models.JSONField(default=dict)

  # Val split. This is a Split proto.
  val_dataset = models.JSONField(default=dict)

  # Test split. This is a Split proto.
  test_dataset = models.JSONField(default=dict)

  # Full dataset. This is a Split proto.
  full_dataset = models.JSONField(default=dict)

  # Cardinality of the whole dataset.
  cardinality = models.IntegerField(default=0)

  # Maps each label to its count in the full dataset.
  label_count = models.JSONField(default=dict)

  # Maps labels numeric format to their text format.
  labels_map = models.JSONField(default=dict)

  # Computer visiion task. This is a ComputerVisionTask proto.
  task = models.JSONField(default=dict)

  # Number of classes in the dataset.
  num_classes = models.IntegerField(default=0)

  # Duration it took to complete the dataset analysis, in minutes.
  analysis_duration_mins = models.FloatField(default=0.)