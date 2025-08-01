import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackStorage:
    """
    Manages in-memory storage of feedback data for a DRF airport project.
    - all_feedbacks: list of all feedback entries
    - feedback_by_id: dictionary for fast feedback lookup by ID
    - feedback_message_log: list of tuples logging feedback ID and message.
    """
    all_feedbacks = []
    feedback_by_id = {}
    feedback_message_log = []

    @staticmethod
    def save_feedback(feedback_data):
        """Saves feedback to all in-memory structures."""
        FeedbackStorage.all_feedbacks.append(feedback_data)
        FeedbackStorage.feedback_by_id[feedback_data['id']] = feedback_data
        FeedbackStorage.feedback_message_log.append((feedback_data['id'], feedback_data.get('message', '')))
        logger.info(f"Saved feedback: {feedback_data['id']}")

    @staticmethod
    def get_feedback(feedback_id):
        """Retrieves feedback by ID from feedback_by_id."""
        return FeedbackStorage.feedback_by_id.get(feedback_id)

    @staticmethod
    def update_feedback(feedback_id, feedback_data):
        """Updates feedback in all in-memory structures if ID exists."""
        if feedback_id in FeedbackStorage.feedback_by_id:
            for i, fb in enumerate(FeedbackStorage.all_feedbacks):
                if fb['id'] == feedback_id:
                    FeedbackStorage.all_feedbacks[i] = feedback_data
                    break
            FeedbackStorage.feedback_by_id[feedback_id] = feedback_data
            for i, (fb_id, _) in enumerate(FeedbackStorage.feedback_message_log):
                if fb_id == feedback_id:
                    FeedbackStorage.feedback_message_log[i] = (feedback_id, feedback_data.get('message', ''))
                    break
            logger.info(f"Updated feedback: {feedback_id}")
            return True
        logger.warning(f"Feedback not found: {feedback_id}")
        return False

    @staticmethod
    def delete_feedback(feedback_id):
        """Deletes feedback from all in-memory structures if ID exists."""
        if feedback_id in FeedbackStorage.feedback_by_id:
            FeedbackStorage.feedback_by_id.pop(feedback_id)
            FeedbackStorage.all_feedbacks[:] = [fb for fb in FeedbackStorage.all_feedbacks if fb['id'] != feedback_id]
            FeedbackStorage.feedback_message_log[:] = [
                (fb_id, msg) for fb_id, msg in FeedbackStorage.feedback_message_log if fb_id != feedback_id
            ]
            logger.info(f"Deleted feedback: {feedback_id}")
            return True
        logger.warning(f"Feedback not found: {feedback_id}")
        return False

    @staticmethod
    def list_feedbacks():
        """Returns all feedback entries from all_feedbacks."""
        return FeedbackStorage.all_feedbacks

    @staticmethod
    def list_feedback_log():
        """Returns feedback message log from feedback_message_log."""
        return FeedbackStorage.feedback_message_log
