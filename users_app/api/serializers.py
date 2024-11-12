from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users_app.models import AbstractUserProfile, CustomerProfile, BusinessProfile
from users_app.utils.auth import split_username, get_auth_response_data

USER_FIELDS = ['username', 'first_name', 'last_name', 'email']
PROFILE_EXTRA_FIELDS = ['type', 'created_at', 'file', 'uploaded_at']
BUSINESS_EXTRA_FIELDS = ['location', 'description', 'working_hours', 'tel']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=63)
    password = serializers.CharField(max_length=63, write_only=True)
    
    def create(self, validated_data):
        validated_data['username'] = validated_data['username'].replace(" ", "_")
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
        if User.objects.filter(username=attrs['username']).exists() or User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('User already exists.')
        validate_password(attrs['password'])
        if attrs['repeated_password'] != attrs['password']:
            raise serializers.ValidationError('Passwords do not match.')
        attrs.pop('repeated_password')
        return attrs
    
    def create(self, validated_data):
        type = validated_data.pop('type')
        validated_data['username'] = validated_data['username'].replace(" ", "_")
        first_name, last_name = split_username(validated_data['username'])
        created_user = User.objects.create_user(first_name=first_name, last_name=last_name, **validated_data)
        if type == CustomerProfile.TYPE:
            CustomerProfile.objects.create(user=created_user)
        elif type == BusinessProfile.TYPE:
            BusinessProfile.objects.create(user=created_user)
        token = Token.objects.create(user=created_user)
        return get_auth_response_data(user=created_user, token=token)
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
        
    class Meta:
        model = User
        fields = ['pk'] + USER_FIELDS
        
class AbstractProfileDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    type = serializers.CharField(source='TYPE', read_only=True)
    file = serializers.FileField(source='file.file', read_only=True)
    uploaded_at = serializers.SerializerMethodField()
    
    class Meta:
        model = AbstractUserProfile
        fields = ['user'] + USER_FIELDS + PROFILE_EXTRA_FIELDS
    
    def get_uploaded_at(self, obj):
        return obj.file.uploaded_at if obj.file else None
    
class CustomerProfileDetailSerializer(AbstractProfileDetailSerializer):
    
    class Meta:
        model = CustomerProfile
        fields = AbstractProfileDetailSerializer.Meta.fields
    
class BusinessProfileDetailSerializer(AbstractProfileDetailSerializer):
    
    class Meta:
        model = BusinessProfile
        fields = AbstractProfileDetailSerializer.Meta.fields + BUSINESS_EXTRA_FIELDS

class BaseProfileListSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    type = serializers.CharField(source='TYPE', read_only=True)
    file = serializers.FileField(source='file.file', read_only=True)
    uploaded_at = serializers.SerializerMethodField()
    
    class Meta:
        model = AbstractUserProfile
        fields = ['user'] + PROFILE_EXTRA_FIELDS
    
    def get_uploaded_at(self, obj):
        return obj.file.uploaded_at if obj.file else None

class CustomerProfileListSerializer(BaseProfileListSerializer):
    
    class Meta:
        model = CustomerProfile
        fields = BaseProfileListSerializer.Meta.fields
        
class BusinessProfileListSerializer(BaseProfileListSerializer):
        
    class Meta:
        model = BusinessProfile
        fields = BaseProfileListSerializer.Meta.fields + BUSINESS_EXTRA_FIELDS