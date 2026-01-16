from datetime import datetime
from rest_framework import serializers


class FeedbackSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=10)
    user_id = serializers.IntegerField()
    flight_id = serializers.CharField(max_length=10)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    message = serializers.CharField(max_length=500, required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    created_at = serializers.DateTimeField(default=datetime.now)
