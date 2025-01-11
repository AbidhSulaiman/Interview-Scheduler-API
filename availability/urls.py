from django.urls import path
from .views import RegisterAvailabilityView, GetInterviewSlotsView

urlpatterns = [
    path('register-availability/', RegisterAvailabilityView.as_view(), name='register_availability'),
    path('get-interview-slots/', GetInterviewSlotsView.as_view(), name='get_interview_slots'),
]
