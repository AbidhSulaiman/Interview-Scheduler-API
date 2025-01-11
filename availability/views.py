import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import AvailabilitySerializer
from .models import Availability


class AvailabilityService:
    """
    Service class responsible for calculating common available slots between a candidate and an interviewer.
    """
    
    @staticmethod
    def get_common_slots(candidate_id, interviewer_id):
        """
        Compute common 1-hour slots for a candidate and an interviewer.

        Args:
            candidate_id (int): The ID of the candidate.
            interviewer_id (int): The ID of the interviewer.
        Returns:
            list: A list of dictionaries representing the common available slots with 'date', 'start_time', 
                  and 'end_time' for each slot.
        """
        candidate_slots = Availability.objects.filter(user_id=candidate_id)
        interviewer_slots = Availability.objects.filter(user_id=interviewer_id)

        if not candidate_slots.exists() or not interviewer_slots.exists():
            raise ValueError("No availability data found for given candidate or interviewer.")

        common_slots = []
        for candidate in candidate_slots:
            for interviewer in interviewer_slots:
                if candidate.date == interviewer.date:
                    max_start = max(candidate.start_time, interviewer.start_time)
                    min_end = min(candidate.end_time, interviewer.end_time)

                    # Generate 1-hour slots within the overlap
                    start = datetime.datetime.combine(candidate.date, max_start)
                    end = datetime.datetime.combine(candidate.date, min_end)

                    while start + datetime.timedelta(hours=1) <= end:
                        slot_end = start + datetime.timedelta(hours=1)
                        common_slots.append({
                            'date': candidate.date,
                            'start_time': start.time(),
                            'end_time': slot_end.time()
                        })
                        start = slot_end

        return common_slots


class RegisterAvailabilityView(APIView):
    """
    Endpoint to register or update availability for a user.

    Methods:
        GET:
            Retrieves the availability slots for a given candidate.

        POST:
            Registers or updates availability for a user on a specific date.
    """
    permission_classes = [IsAuthenticated]
        
    def post(self, request):
        """
        POST request handler to register or update availability for the authenticated user.

        Args:
            request (Request): The request object containing availability data.

        Returns:
            Response: A response indicating whether the availability was registered or updated.
        """
        serializer = AvailabilitySerializer(data=request.data)
        
        if serializer.is_valid():
            # Extract the date and time from the request data
            date = request.data.get('date')
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']

            # Check if a record already exists for the user on the given date
            record = Availability.objects.filter(user=request.user, date=date).first()

            if record:
                # Update the slot time if a record exists
                record.start_time = start_time
                record.end_time = end_time
                record.save()
                message = 'Availability updated successfully.'
            else:
                # Create a new record if no existing record is found
                serializer.save(user=request.user)
                message = 'Availability registered successfully.'
            
            return Response(
                {'message': message, 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetInterviewSlotsView(APIView):
    """
    Methods:
        GET:
            Retrieves common available interview slots between a candidate and an interviewer.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        GET request handler to retrieve common interview slots between a candidate and an interviewer.

        Args:
            request (Request): The request object containing the candidate_id and interviewer_id as query parameters.

        Returns:
            Response: A response containing a list of common interview slots or an error message.
        """
        candidate_id = request.query_params.get('candidate_id')
        interviewer_id = request.query_params.get('interviewer_id')

        # Check if both candidate_id and interviewer_id are provided
        if not candidate_id or not interviewer_id:
            return Response(
                {'error': 'Both candidate_id and interviewer_id are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            common_slots = AvailabilityService.get_common_slots(candidate_id, interviewer_id)
            if not common_slots:
                return Response({'message': 'No common slots available.'}, status=200)
            return Response({'common_slots': common_slots}, status=200)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
