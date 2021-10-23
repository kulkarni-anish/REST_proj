
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserViewSet, todo_list, todo_view, NotesList, NotesDetail, registration_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet)    


# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })


urlpatterns = [
    path('login',obtain_auth_token),
    path('todo', todo_list),
    path('todo/<int:pk>/', todo_view),
    path('notes', NotesList.as_view()),
    path('notes/<int:pk>/', NotesDetail.as_view()),
    path('register', registration_view, name="register"),
    # path('users/', user_list, name='user-list'),
    # path('users/<int:pk>/', user_detail, name='user-detail')
    path('', include(router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)