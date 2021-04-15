from rest_framework import serializers
from .models import (
    Task,
    Tag
)


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "created_at", "updated_at")
        read_only = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context["request"]
        return Tag.objects.create(user=request.user, **validated_data)


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "tags", "description", "priority", "is_completed", "created_at", "updated_at")
        read_only = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context["request"]
        tags = []
        if "tags" in validated_data.keys():
            tags = validated_data.pop("tags")
        if "is_completed" in validated_data.keys():
            validated_data.pop("is_completed")
        instance = Task.objects.create(user=request.user, **validated_data)
        instance.tags.add(*tags)
        return instance
