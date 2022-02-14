from django.urls import  path
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include
from .views import UserViewSet1, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView



user_list = UserViewSet1.as_view({
    'get': 'list',
    'post': 'create',
})
current_user = UserViewSet1.as_view({
    'get': 'get_current_user',
})

user_detail = UserViewSet1.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


app_name = 'users'

urlpatterns = [
    path('', user_list, name='list'),
    path('current_user', current_user, name='current_user'),
    path('<int:pk>/', user_detail, name='detail'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    #path('tokens/get', LoginView.as_view(), name='login'),
    #path('tokens/refresh', TokenRefreshView.as_view(), name='refresh_tokens'),
    #path('tokens/verify', TokenVerifyView.as_view(), name='verify_token'),
    #path('tokens/blacklist', TokenBlacklistView.as_view(), name='blacklist_token'),
]
urlpatterns = format_suffix_patterns(urlpatterns)