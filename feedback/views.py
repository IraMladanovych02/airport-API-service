import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeedbackSerializer
from .storage import FeedbackStorage

logger = logging.getLogger(__name__)


class FeedbackListCreateView(APIView):
    def get(self, request):
        feedbacks = FeedbackStorage.list_feedbacks()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback_data = serializer.validated_data
            FeedbackStorage.save_feedback(feedback_data)
            logger.info(f"Feedback created: {feedback_data['id']}")
            return Response(feedback_data, status=status.HTTP_201_CREATED)
        logger.error(f"Feedback creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackDetailView(APIView):
    def get(self, request, pk):
        feedback_data = FeedbackStorage.get_feedback(pk)
        if not feedback_data:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = FeedbackSerializer(feedback_data)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            if FeedbackStorage.update_feedback(pk, serializer.validated_data):
                logger.info(f"Feedback updated: {pk}")
                return Response(serializer.validated_data)
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        logger.error(f"Feedback update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if FeedbackStorage.delete_feedback(pk):
            logger.info(f"Feedback deleted: {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
