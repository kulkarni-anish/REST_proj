
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import todo_list, todo_view, NotesList, NotesDetail, registration_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login',obtain_auth_token),
    path('todo', todo_list),
    path('todo/<int:pk>/', todo_view),
    path('notes', NotesList.as_view()),
    path('notes/<int:pk>/', NotesDetail.as_view()),
    path('register', registration_view, name="register"),
]

#urlpatterns = format_suffix_patterns(urlpatterns)