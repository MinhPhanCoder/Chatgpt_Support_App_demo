import os
import json
from src.settings.settings import Settings
from src.utils.logger import get_logger

logger = get_logger()


class ConfigManager:
    """Manages application configuration including theme, API URL, and API key"""

    def __init__(self):
        self.settings = Settings()
        self.current_theme = self.settings.DEFAULT_THEME
        self.api_url = self.settings.DEFAULT_API_URL
        self.api_key = self.settings.DEFAULT_API_KEY
        self.username = self.settings.DEFAULT_USERNAME
        self.user_id = self.settings.DEFAULT_USER_ID

        # Ensure config directory exists
        os.makedirs(self.settings.CONFIG_DIR, exist_ok=True)
        self.config_path = os.path.join(
            self.settings.CONFIG_DIR, self.settings.CONFIG_FILE
        )

        # Load existing configuration if available
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    self.current_theme = config.get(
                        "theme", self.settings.DEFAULT_THEME
                    )
                    self.api_url = config.get("api_url", self.settings.DEFAULT_API_URL)
                    self.api_key = config.get("api_key", self.settings.DEFAULT_API_KEY)
                    self.username = config.get(
                        "username", self.settings.DEFAULT_USERNAME
                    )
                    self.user_id = config.get("user_id", self.settings.DEFAULT_USER_ID)
                    logger.info(
                        f"Configuration loaded successfully from {self.config_path}"
                    )
            else:
                self.save_config()  # Create default config file
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            # Use defaults if config can't be loaded

    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                "theme": self.current_theme,
                "api_url": self.api_url,
                "api_key": self.api_key,
                "username": self.username,
                "user_id": self.user_id,
            }
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)
                logger.info(f"Configuration saved successfully to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")

    def set_theme(self, theme):
        """Set application theme"""
        if theme in self.settings.AVAILABLE_THEMES:
            self.current_theme = theme
            self.save_config()
            return True
        return False

    def set_api_url(self, url):
        """Set API URL"""
        self.api_url = url
        self.save_config()

    def set_api_key(self, key):
        """Set API Key"""
        self.api_key = key
        self.save_config()

    def set_user_info(self, username, user_id):
        """Set user information"""
        self.username = username
        self.user_id = user_id
        self.save_config()
