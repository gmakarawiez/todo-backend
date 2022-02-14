from rest_framework import viewsets
from todos.models.models import ToDo
from .serializers import ToDoCreateSerializer, ToDoListSerializer
from rest_framework.response import Response
from .models.models import ToDo
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.serializers import UserSerializer

class ToDoViewSet(viewsets.ViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    #queryset = ToDo.objects.all()
    #permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = []
    pagination_class = None


    def create(self, request):
        print(request.__dict__)
        data = request.data
        #user = UserSerializer(request.user)
        #print("user: ", user)
        serializer = ToDoCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        queryset = ToDo.objects.all()
        serializer = ToDoListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        todo = self.get_object(pk)
        serializer = ToDoListSerializer(todo, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        todo = self.get_object(pk)
        serializer = ToDoCreateSerializer(todo, data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save(last_editor=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        todo = self.get_object(pk)
        serializer = ToDoCreateSerializer(todo, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_200_OK)