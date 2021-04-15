from rest_framework import mixins
from rest_framework import generics
from .serializers import (
    TasksSerializer,
    TagsSerializer
)
from .models import (
    Tag,
    Task
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


class TagsAPIView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = TagsSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Tag.objects.filter(user=self.request.user)
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TagDetailAPIView(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    serializer_class = TagsSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


class TasksAPIView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    serializer_class = TasksSerializer
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def str2bool(value):
        return value.lower() in ("true", "1")

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        name = self.request.query_params.get("name")
        description = self.request.query_params.get("description")
        priority = self.request.query_params.get("priority")
        is_completed = self.request.query_params.get("is_completed")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if priority:
            queryset = queryset.filter(priority=priority)
        if is_completed:
            queryset = queryset.filter(is_completed=self.str2bool(is_completed))
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TasksDetailAPIView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    serializer_class = TasksSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)
