from rest_framework import viewsets, status
from .models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView



class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserViewSet1(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    """
    @action(detail=False, methods=['get'], name="get_current_user")
    def get_current_user(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, context ={'request': request})
        return Response(serializer.data)
    """