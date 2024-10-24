from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import CustomerProfile, BusinessProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Django User model, handling user creation and password protection.
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        Custom create method to handle user creation with hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
    
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password']


class CustomerProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model, linking to the related User model.
    """
    user = UserSerializer(read_only=True)
    type = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerProfile
        fields = ['user', 'type', 'created_at', 'file', 'uploaded_at']
        
    def get_type(self, obj):
        return 'customer'
        
        
class BusinessProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model, linking to the related User model.
    """
    user = UserSerializer(read_only=True)
    type = serializers.SerializerMethodField()
        
    class Meta:
        model = BusinessProfile
        fields = CustomerProfileSerializer.Meta.fields + ['location', 'description', 'working_hours', 'tel']
        
    def get_type(self, obj):
        return 'business'