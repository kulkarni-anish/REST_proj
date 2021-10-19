
from django.urls import path
from .views import todo_list, todo_view

urlpatterns = [
    path('todo/', todo_list),
    path('view/<int:pk>/', todo_view),
]

