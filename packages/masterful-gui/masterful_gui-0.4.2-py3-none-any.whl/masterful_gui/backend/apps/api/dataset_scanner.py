"""Defines Visualize's dataset proto scanner functionality.

This module implements the functionality for Visualzie to scan for
serialized dataset_pb2.Dataset serialized protos produced by
Masterful.
"""

import os
import pathlib

import google.protobuf.json_format as json_format

from masterful_gui.backend.apps.api import models
from masterful_gui.backend.proto import dataset_pb2

# The location where the scanner should look for serialzed protos.
_SCAN_DIR = f'{os.path.expanduser("~")}/.masterful/datasets'

# The extension of a serialized policy proto file. The extension actually
# makes no difference, this is just to facilitate identifying the right files
# to read.
# WARNING: This matches the configuration of proto_serializer module in
# masterful_partners repo. You must change them both or you'll break
# assumptions and Visualize.
_EXTENSION = "dspb"


def scan():
  """Scans the configured directory for serlized dataset protos.
  
  This function deserializes dataset protos on disk, converts them
  to Django's owm dataset spec model, and persists them to the database
  (app model).
  If the database already had a record for that dataset, it updates
  that records with the values extracted from the serialized dataset. If
  it wasn't, this will persist it to the database.
  """
  pathlib.Path(_SCAN_DIR).mkdir(parents=True, exist_ok=True)

  if len(os.listdir(_SCAN_DIR)) == 0:
    #TODO(ray): Consider printing something to show in backend logs.
    return

  serialized_protos = []
  for file in os.listdir(_SCAN_DIR):
    if file.split('.')[-1] != _EXTENSION:
      continue
    serialized_protos.append(file)

  if len(serialized_protos) == 0:
    return

  for serialized_proto in serialized_protos:
    proto = dataset_pb2.Dataset()
    file_name = f'{_SCAN_DIR}/{serialized_proto}'
    with open(file_name, "rb") as f:
      proto.ParseFromString(f.read())

    proto_dict = json_format.MessageToDict(proto,
                                           use_integers_for_enums=False,
                                           including_default_value_fields=True,
                                           preserving_proto_field_name=True)

    model_exists = len(models.Dataset.objects.filter(pk=proto.id)) > 0
    if model_exists:
      existing_model = models.Dataset.objects.get(pk=proto.id)
      existing_model.title = proto.title
      existing_model.train_dataset = proto_dict.get("train_dataset", {})
      existing_model.val_dataset = proto_dict.get("val_dataset", {})
      existing_model.test_dataset = proto_dict.get("test_dataset", {})
      existing_model.full_dataset = proto_dict.get("full_dataset", {})
      existing_model.cardinality = proto.cardinality
      existing_model.label_count = proto_dict.get("label_count", {})
      existing_model.labels_map = proto_dict.get("labels_map", {})
      existing_model.task = proto_dict.get("task", {})
      existing_model.num_classes = proto.num_classes
      existing_model.analysis_duration_mins = proto.analysis_duration_mins

      existing_model.save()

    else:
      new_model = models.Dataset.objects.create(
          dataset_id=proto.id,
          title=proto.title,
          train_dataset=proto_dict.get("train_dataset", {}),
          val_dataset=proto_dict.get("val_dataset", {}),
          test_dataset=proto_dict.get("test_dataset", {}),
          full_dataset=proto_dict.get("full_dataset", {}),
          cardinality=proto.cardinality,
          label_count=proto_dict.get("label_count", {}),
          labels_map=proto_dict.get("labels_map", {}),
          task=proto_dict.get("task", {}),
          num_classes=proto.num_classes,
          analysis_duration_mins=proto.analysis_duration_mins)
      new_model.save()