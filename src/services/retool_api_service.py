import json
import requests
from src.utils.logger import get_logger
from src.settings.config_manager import ConfigManager

logger = get_logger()


class RetoolAPIService:
    """Service to handle communication with the Retool API"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.api_url = self.config_manager.api_url
        self.api_key = self.config_manager.api_key

    def send_request(self, user_name, user_id, file_name, image_data):
        """
        Send a request to the Retool API

        Args:
            user_name (str): User's name
            user_id (str): User's ID
            file_name (str): Name of the file being analyzed
            image_data (str): Base64 encoded image data

        Returns:
            dict: The JSON response from the API or error message
        """
        # Update URL and key from config manager in case they've changed
        self.api_url = self.config_manager.api_url
        self.api_key = self.config_manager.api_key

        # Prepare the request data
        payload = {
            "user_name": user_name,
            "user_id": user_id,
            "file_name": file_name,
            "data": image_data,  # This should include the 'data:image/png;base64,' prefix
        }

        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "X-Workflow-Api-Key": self.api_key,
        }

        logger.info(f"Sending API request for file: {file_name}")

        response = requests.post(
            self.api_url, data=json.dumps(payload), headers=headers
        )

        logger.info(f"{response.json() = }")
        logger.info(f"{response.status_code = }")
        return response.json()
