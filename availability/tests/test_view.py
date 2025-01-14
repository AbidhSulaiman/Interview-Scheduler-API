from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import User
from ..models import Availability
from datetime import date, time

class AvailabilityViewTest(TestCase):
    
    def setUp(self):
        # Creating a user for testing
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_register_availability(self):
        # Registering new availability
        data = {
            "date": "2025-02-12",
            "start_time": "10:00:00",
            "end_time": "13:00:00"
        }
        response = self.client.post("/availability/register-availability/", data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Availability registered successfully.")
    
    def test_update_availability(self):
        # Create an initial availability record
        Availability.objects.create(
            user=self.user,
            date=date(2025, 2, 12),
            start_time=time(10, 0),
            end_time=time(13, 0)
        )
        
        # Updating availability
        data = {
            "date": "2025-02-12",
            "start_time": "11:00:00",
            "end_time": "14:00:00"
        }
        
        response = self.client.post("/availability/register-availability/", data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Availability updated successfully.")
    
    def test_get_interview_slots_with_normal_user(self):
        # Create availability for two users
        candidate = User.objects.create_user(username="candidate", password="password")
        interviewer = User.objects.create_user(username="interviewer", password="password")
        
        Availability.objects.create(
            user=candidate,
            date=date(2025, 1, 12),
            start_time=time(10, 0),
            end_time=time(13, 0)
        )
        Availability.objects.create(
            user=interviewer,
            date=date(2025, 1, 12),
            start_time=time(11, 0),
            end_time=time(14, 0)
        )
        
        # Trying to get common interview slots (only 1 hour slot should be available)
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/availability/get-interview-slots/", {
            'candidate_id': candidate.id,
            'interviewer_id': interviewer.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_get_interview_slots_with_admin_user(self):
        # Create availability for two users
        candidate = User.objects.create_user(username="candidate", password="password")
        interviewer = User.objects.create_user(username="interviewer", password="password")
        admin = User.objects.create_superuser(username="admin", password="password")
        
        Availability.objects.create(
            user=candidate,
            date=date(2025, 1, 12),
            start_time=time(10, 0),
            end_time=time(13, 0)
        )
        Availability.objects.create(
            user=interviewer,
            date=date(2025, 1, 12),
            start_time=time(11, 0),
            end_time=time(14, 0)
        )
        
        # Trying to get common interview slots (only 1 hour slot should be available)
        self.client.force_authenticate(user=admin)
        response = self.client.get("/availability/get-interview-slots/", {
            'candidate_id': candidate.id,
            'interviewer_id': interviewer.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_interview_slots_missing_parameters(self):
        # Trying to get interview slots without candidate or interviewer
        response = self.client.get("/availability/get-interview-slots/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
