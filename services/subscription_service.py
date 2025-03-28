# services/subscription_service.py
from utils.file_handler import load_json, save_json
from config import SUBSCRIBERS_FILE

class SubscriptionService:
    """
    Manages subscribers who will receive notifications.
    """
    def __init__(self):
        self.subscribers = load_json(SUBSCRIBERS_FILE)

    def add_subscriber(self, chat_id: str) -> None:
        """
        Add a subscriber if not already subscribed.
        """
        if chat_id not in self.subscribers:
            self.subscribers[chat_id] = True
            save_json(SUBSCRIBERS_FILE, self.subscribers)
            print(f"Subscriber {chat_id} added.")
        else:
            print(f"Subscriber {chat_id} is already subscribed.")

    def remove_subscriber(self, chat_id: str) -> None:
        """
        Remove a subscriber.
        """
        if chat_id in self.subscribers:
            del self.subscribers[chat_id]
            save_json(SUBSCRIBERS_FILE, self.subscribers)
            print(f"Subscriber {chat_id} removed.")

    def get_all_subscribers(self) -> list:
        """
        Return a list of all subscriber chat IDs.
        """
        return list(self.subscribers.keys())
