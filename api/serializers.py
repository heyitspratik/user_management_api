from datetime import datetime
from rest_framework import serializers
from django.core.exceptions import ValidationError
import re

class UserSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=False)  # MongoDB will generate this
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    dob = serializers.DateField()
    address = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=["Male", "Female", "Other"])
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        # Custom validation for phone number
        if len(value) < 10 or len(value) > 15:
            raise ValidationError("Phone number must be between 10 and 15 digits.")
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise ValidationError("Invalid phone number format.")
        return value

    def create(self, validated_data):
        validated_data['status'] = "Active"
        return validated_data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

