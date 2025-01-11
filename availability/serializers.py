import datetime
from rest_framework import serializers
from .models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for Availability model to validate and serialize availability data.

    Methods:
        validate(self, data):
            Validates the input data to ensure business rules are adhered to.
    """
    
    class Meta:
        model = Availability
        fields = ['id', 'date', 'start_time', 'end_time']
    
    def validate(self, data):
        """
        Custom validation to ensure the availability data meets the business requirements.

        This method performs the following validations:
        - Ensures that the date is not in the past.
        - Ensures that the end time is after the start time.
        """

        if data['date'] < datetime.date.today():
            raise serializers.ValidationError("The date cannot be in the past.")

        start_time = data.get('start_time')
        end_time = data.get('end_time')


        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time.")

        return data
