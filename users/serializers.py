from rest_framework import serializers
from .models import CustomUser
#from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.db import transaction
from todos.models.models import ToDo

"""
class RegisterSerializer(RegisterSerializer):

    class Meta:
        model = CustomUser
        fields = ['email','password1', 'password2', 'username']
        extra_kwargs = {
            'password1': {
                'write_only':True
            },
            'password2': {
                'write_only': True
            }
        }

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        #user = super().save(request)
        user = CustomUser(
            email = self.validated_data['email'],
        )
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']

        if password1 != password2:
            raise serializers.ValidationError({'password2':'Passwords must match.'})
        user.set_password(password1)
        user.save()
        return user
"""


class LoginSerializer(LoginSerializer):

    username = None
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


    def validate(self, data):

        email = data["email"]
        password = data["password"]

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "invalid email"})

        user = CustomUser.objects.filter(email=email).first()
        if not user.check_password(password):
            raise serializers.ValidationError({"password": ["invalid password"]})

        data = super().validate(data)

        return data




class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="users:detail", lookup_url_kwarg = 'pk')
    #todos = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        #fields = ['email', 'id', 'password', 'url', 'username', 'todos']
        fields = ['email', 'id', 'password', 'url', 'username']

    def validate_email(self, email):
        if self.context["request"]._request.method == "POST":
            if CustomUser.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": "this email is already in use, please choose another one"})
        return email
