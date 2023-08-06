from rest_framework import serializers

from masterful_gui.backend.apps.api import models


class PolicySearchTaskModelSerializer(serializers.ModelSerializer):

  class Meta:
    model = models.PolicySearchTask
    fields = '__all__'


class DatasetModelSerializer(serializers.ModelSerializer):

  class Meta:
    model = models.Dataset
    fields = '__all__'