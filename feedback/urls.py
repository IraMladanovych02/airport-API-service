from django.urls import path

from feedback.views import (
    FeedbackListCreateView,
    FeedbackDetailView
)

urlpatterns = [
    path("", FeedbackListCreateView.as_view(), name="feedback-list"),
    path("<int:pk>/", FeedbackDetailView.as_view(), name="feedback-detail"),
]

app_name = "feedback"
