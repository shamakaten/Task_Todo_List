from django.contrib import admin
from django.urls import include, path

from .views import (
    IndexView,
    LoginView,
    CompleteView,
    DecompleteView,
    RegisterView,
    DeletecompleteView,
    DeleteallView,
    AddTodoView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('complete/<todo_id>', CompleteView.as_view(), name='complete'),
    path('decomplete/<todo_id>', DecompleteView.as_view(), name='decomplete'),
    path('deletecomplete/', DeletecompleteView.as_view(), name='deletecomplete'),
    path('deleteall/', DeleteallView.as_view(), name='deleteall'),
    path('addtodo/', AddTodoView.as_view(), name='addtodo'),

]
