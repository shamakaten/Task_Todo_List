from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Company, Todo


# Create your views here.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail')
    password = serializers.CharField(max_length=200, label='Пароль', style={'input_type': 'password'})
    companies = serializers.PrimaryKeyRelatedField(label='Компании', queryset=Company.objects.all(), many=True)

    class Meta:
        fields = ('email', 'password', 'companies')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail')
    companies = serializers.PrimaryKeyRelatedField(label='Компании', queryset=Company.objects.all(), many=True)

    class Meta:
        fields = ('email', 'companies')


class TodoListSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id','text','complete', 'company')


class TodoElementCreateSerializer(serializers.ModelSerializer):
    text = serializers.EmailField(label='New todo task')
    def create(self, validated_data):
        pass

    class Meta:
        model = Todo
        fields = ('text')