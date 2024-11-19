from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users_app.models import AbstractUserProfile, CustomerProfile, BusinessProfile
from users_app.utils.auth import split_username, get_auth_response_data

USER_NAME_FIELDS = ['username', 'first_name', 'last_name']
USER_FIELDS = USER_NAME_FIELDS + ['email']
PROFILE_EXTRA_FIELDS = ['type', 'created_at', 'file', 'uploaded_at']
BUSINESS_EXTRA_FIELDS = ['location', 'description', 'working_hours', 'tel']

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login, handling username and password validation.

    Fields:
        username: The user's username.
        password: The user's password, write-only.
        
    Methods:
        validate(attrs): Validates user data using the Django 'authenticate' method.
        create(validated_data): Creates a new user and associated profile based on type.
    """
    username = serializers.CharField(max_length=63)
    password = serializers.CharField(max_length=63, write_only=True)
    
    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Invalid credentials.')            
        return attrs
    
    def create(self, validated_data):
        validated_data['username'] = validated_data['username'].replace(" ", "_")
        user = User.objects.get(username=validated_data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return get_auth_response_data(user=user, token=token)              

class RegistrationSerializer(LoginSerializer):
    """
    Serializer for user registration, with password validation and profile type selection.

    Fields:
        repeated_password: The repeated password for confirmation, write-only.
        email: The user's email address.
        type: The profile type, either 'business' or 'customer'.
    
    Methods:
        validate(attrs): Validates user data, ensuring uniqueness and matching passwords.
        create(validated_data): Creates a new user and associated profile based on type.
    """
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
    
class UserDetailsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for user names.
    """  
    class Meta:
        """
        fields: User name fields including 'username', 'first_name' and 'last_name'.
        """
        model = User
        fields = USER_NAME_FIELDS    
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for basic user information.
    """  
    class Meta:
        """
        fields: The primary key and user fields.
        """
        model = User
        fields = ['pk'] + USER_FIELDS
        
class AbstractProfileDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    Base serializer for user profile details, to be inherited by both Customer and Business profiles.

    Fields:
        user: The associated user.
        username, first_name, last_name, email: Basic user information, read-only.
        type: The profile type.
        file: The associated file upload, if any.
        uploaded_at: The upload date of the file, if any.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    type = serializers.CharField(source='TYPE', read_only=True)
    file = serializers.SerializerMethodField()
    uploaded_at = serializers.SerializerMethodField()
    
    class Meta:
        """
        fields: The primary key (named 'user'), the user fields and the additional fields from the user profile model.
        """
        model = AbstractUserProfile
        fields = ['user'] + USER_FIELDS + PROFILE_EXTRA_FIELDS + ['uploaded_at']
        
    def get_file(self, obj):
        return obj.file.file if obj.file else None
    
    def get_uploaded_at(self, obj):
        return obj.file.uploaded_at if obj.file else None
    
class CustomerProfileDetailSerializer(AbstractProfileDetailSerializer):
    """
    Serializer for detailed Customer profile information, inheriting from AbstractProfileDetailSerializer.
    """
    class Meta:
        model = CustomerProfile
        fields = AbstractProfileDetailSerializer.Meta.fields
    
class BusinessProfileDetailSerializer(AbstractProfileDetailSerializer):
    """
    Serializer for detailed Business profile information, inheriting from AbstractProfileDetailSerializer, 
    with additional business-specific fields.
    """
    class Meta:
        """
        fields: Includes business-specific fields such as location, description, working_hours, and tel.
        """
        model = BusinessProfile
        fields = AbstractProfileDetailSerializer.Meta.fields + BUSINESS_EXTRA_FIELDS

class BaseProfileListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Base serializer for listing user profiles, including user and profile details.

    Fields:
        user: The associated user.
        type: The profile type, read-only.
        file: The associated file upload, if any.
        uploaded_at: The upload date of the file, if any.
    """
    user = UserSerializer()
    type = serializers.CharField(source='TYPE', read_only=True)
    file = serializers.SerializerMethodField()
    uploaded_at = serializers.SerializerMethodField()
    
    class Meta:
        """
        fields: Includes additional fields from the user profile model.
        """
        model = AbstractUserProfile
        fields = ['user'] + PROFILE_EXTRA_FIELDS
    
    def get_file(self, obj):
        return obj.file.file if obj.file else None

    def get_uploaded_at(self, obj):
        return obj.file.uploaded_at if obj.file else None

class CustomerProfileListSerializer(BaseProfileListSerializer):
    """
    Serializer for listing Customer profiles, inheriting from BaseProfileListSerializer.
    """
    class Meta:
        model = CustomerProfile
        fields = BaseProfileListSerializer.Meta.fields
        
class BusinessProfileListSerializer(BaseProfileListSerializer):
    """
    Serializer for listing Business profiles, inheriting from BaseProfileListSerializer, with additional business-specific fields.
    """
    class Meta:
        """
        fields: Includes business-specific fields such as location, description, working_hours, and tel.
        """
        model = BusinessProfile
        fields = BaseProfileListSerializer.Meta.fields + BUSINESS_EXTRA_FIELDS