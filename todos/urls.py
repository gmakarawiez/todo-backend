from django.urls import  path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ToDoViewSet

todo_list = ToDoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
todo_detail = ToDoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

app_name = 'todos'
urlpatterns = [
    path('', todo_list, name='list'),
    path('<int:pk>/',todo_detail, name='detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)

