from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users_app.models import AbstractUserProfile, CustomerProfile, BusinessProfile
from users_app.utils_auth import split_username, get_auth_response_data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=63)
    password = serializers.CharField(max_length=63, write_only=True)
    
    def create(self, validated_data):
        user = authenticate(**validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return get_auth_response_data(user=user, token=token)              
        else:
            raise serializers.ValidationError('Invalid credentials.')


class RegistrationSerializer(LoginSerializer):
    repeated_password = serializers.CharField(max_length=63, write_only=True)
    email = serializers.EmailField(max_length=63)
    type = serializers.ChoiceField((BusinessProfile.TYPE, CustomerProfile.TYPE))
    
    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username already taken')
        validate_password(attrs['password'])
        if attrs['repeated_password'] != attrs['password']:
            raise serializers.ValidationError('Passwords do not match.')
        attrs.pop('repeated_password')
        return attrs
    
    def create(self, validated_data):
        type = validated_data.pop('type')
        first_name, last_name = split_username(validated_data['username'])
        created_user = User.objects.create_user(first_name=first_name, last_name=last_name, **validated_data)
        if type == CustomerProfile.TYPE:
            CustomerProfile.objects.create(user=created_user)
        elif type == BusinessProfile.TYPE:
            BusinessProfile.objects.create(user=created_user)
        token = Token.objects.create(user=created_user)
        return get_auth_response_data(user=created_user, token=token)
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Django User model, handling user creation and password protection.
    """
    password = serializers.CharField(write_only=True)
        
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'password']
        
class BaseProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model, linking to the related User model.
    """
    user = UserSerializer()
    type = serializers.SerializerMethodField()
    
    class Meta:
        model = AbstractUserProfile
        fields = ['user', 'type', 'created_at', 'file', 'uploaded_at']
        
    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user_serializer = UserSerializer(instance.user, user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError({
                    'user': user_serializer.errors
                })
        super().update(instance, validated_data)
        instance.save()
        return instance
    
    def get_type(self, obj):
        return None

class CustomerProfileSerializer(BaseProfileSerializer):
        
    def get_type(self, obj):
        return CustomerProfile.TYPE
    
    class Meta:
        model = CustomerProfile
        fields = BaseProfileSerializer.Meta.fields
        
class BusinessProfileSerializer(BaseProfileSerializer):
        
    class Meta:
        model = BusinessProfile
        fields = BaseProfileSerializer.Meta.fields + ['location', 'description', 'working_hours', 'tel']
        
    def get_type(self, obj):
        return BusinessProfile.TYPE