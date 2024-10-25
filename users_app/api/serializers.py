from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import AbstractUserProfile, CustomerProfile, BusinessProfile

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