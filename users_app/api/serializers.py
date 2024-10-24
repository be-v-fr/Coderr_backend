from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import UserProfile, BusinessUserProfile


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

  
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model, linking to the related User model.
    """
    user = UserSerializer(read_only=True)
        
    
    class Meta:
        model = UserProfile
        fields = ['user', 'type', 'created_at', 'file', 'uploaded_at']
        
        
class BusinessUserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model, linking to the related User model.
    """
    user = UserSerializer(read_only=True)
        
    
    class Meta:
        model = BusinessUserProfile
        fields = UserProfileSerializer.Meta.fields + ['location', 'description', 'working_hours', 'tel']




# UserProfileSerializer
# falls type = BUSINESS: BusinessInfo-Objekt abfragen und, falls vorhanden, ohne Verschachtelung dem Serializer hinzufügen
# {
# "user": {
# "pk": 1,
# "username": "max_mustermann",
# "first_name": "Max",
# "last_name": "Mustermann"
# },
# "file": "profile_picture.jpg",
# "location": "Berlin",
# "tel": "123456789",
# "description": "Business description",
# Dokumentation für die Backend-Endpunkte: Coderr 2024
# "working_hours": "9-17",
# "type": "business",
# "email": "max@business.de",
# "created_at": "2023-01-01T12:00:00"
# }