from rest_framework import serializers

from crm_cubedots.model.task import Tasks

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tasks
        fields='__all__'
