from rest_framework.exceptions import ValidationError
from django.test import TestCase
from availability.models import Availability
from availability.serializers import AvailabilitySerializer
from authentication.models import User
from datetime import date, time

class AvailabilitySerializerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
    
    def test_availability_serializer_valid(self):
        data = {
            "date": "2025-01-12",
            "start_time": "10:00:00",
            "end_time": "13:00:00"
        }
        
        serializer = AvailabilitySerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_availability_serializer_invalid(self):
        data = {
            "date": "2025-01-12",
            "start_time": "13:00:00",
            "end_time": "10:00:00"
        }
        
        serializer = AvailabilitySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
    
    def test_availability_serializer_invalid_date(self):
        data = {
            "date": "2024-01-12",
            "start_time": "10:00:00",
            "end_time": "13:00:00"
        }
        
        serializer = AvailabilitySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
