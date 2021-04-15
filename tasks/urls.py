from django.urls import (
    path
)
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .views import (
    TagsAPIView,
    TagDetailAPIView,
    TasksAPIView,
    TasksDetailAPIView
)

app_name = "tasks"


@api_view(["GET"])
@permission_classes((AllowAny,))
def health_check(request):
    return Response({"message": "It's Working"}, status=HTTP_200_OK)


urlpatterns = [
    # Auth
    path('auth/', obtain_auth_token, name='obtain_auth_token'),

    # Health check
    path("healthcheck/", health_check, name='health_check'),

    # Tags
    path('tags/', TagsAPIView.as_view(), name='tags_api'),
    path('tags/<str:pk>/', TagDetailAPIView.as_view(), name='tag_detail_api'),

    # Tasks
    path('tasks/', TasksAPIView.as_view(), name='tasks_api'),
    path('tasks/<str:pk>/', TasksDetailAPIView.as_view(), name='tasks_detail_api'),

    # Swagger
    path('swagger/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_static_path': 'v1/swagger.yml'}
    ), name='swagger'),
]
