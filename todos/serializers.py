from rest_framework import serializers
from todos.models.models import ToDo



class ToDoListSerializer(serializers.HyperlinkedModelSerializer):

    creator = serializers.StringRelatedField(many=False)
    created = serializers.DateTimeField()
    last_editor = serializers.StringRelatedField(many=False)
    last_edited = serializers.DateTimeField()

    class Meta:
        model = ToDo
        fields = ('id', 'title', 'description', 'completed', 'creator', 'created', 'last_editor', 'last_edited')


class ToDoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ('title', 'description', 'completed')