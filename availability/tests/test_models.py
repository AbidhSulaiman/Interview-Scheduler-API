from django.test import TestCase
from django.db.utils import IntegrityError
from authentication.models import User
from availability.models import Availability
from datetime import date, time

class AvailabilityModelTest(TestCase):
    
    def setUp(self):
        # Creating a user for the availability model
        self.user = User.objects.create_user(username="testuser", password="password")
        
    def test_create_availability(self):
        # Create an availability record
        availability = Availability.objects.create(
            user=self.user,
            date=date(2025, 1, 12),
            start_time=time(10, 0),
            end_time=time(13, 0)
        )
        
        # Check if the availability is saved correctly
        self.assertEqual(availability.user.username, "testuser")
        self.assertEqual(availability.date, date(2025, 1, 12))
        self.assertEqual(str(availability), "testuser: 2025-01-12 (10:00:00 - 13:00:00)")

    def test_end_time_after_start_time_constraint(self):
        # Ensure the constraint is checked: end_time must be after start_time
        with self.assertRaises(IntegrityError):
            Availability.objects.create(
                user=self.user,
                date=date(2025, 1, 12),
                start_time=time(13, 0),
                end_time=time(10, 0)
            )
