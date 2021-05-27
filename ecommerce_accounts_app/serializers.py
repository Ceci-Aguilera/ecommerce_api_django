from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name','stripe_customer_id','phone']
        extra_kwargs = {'password':{'witre_only':True, 'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
