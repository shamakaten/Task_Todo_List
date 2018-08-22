from django.conf.urls import url, include
from django.urls import path

from . import view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todolist', view.TodoListViewSet, base_name='todolist-list')

urlpatterns = [
    url(r'^', include(router.urls)),
    path('login/', view.LoginAPIView.as_view(), name='api_login'),
    path('logout/', view.LogoutAPIView.as_view(), name='logout'),
    path('register/', view.RegisterAPIView.as_view(), name='api_register'),
    path('todolist/<int:pk>', view.TodoListViewSet.as_view({'list'}), name='list_info'),
]