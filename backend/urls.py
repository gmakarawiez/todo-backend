from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from todos.views import ToDoViewSet

#router = routers.DefaultRouter()
#router.register(r'todos', ToDoViewSet, 'todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/', include('todos.urls')),
    path('users/', include('users.urls')),
 ]