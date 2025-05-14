"""
Configuration settings for YouTube to Odoo eLearning import
"""

# YouTube API settings
YOUTUBE_API_KEY = "AIzaSyCBib-5NGrBt-b0EZ-d6s5l-_xxnCaJPpI"  # Replace with your actual API key

# Database connection settings
ODOO = {
    "host": "localhost",
    "port": 5432,
    "db": "playground",
    "username": "odoo",
    "password": "bismillah"
}

# Odoo eLearning module tables
SLIDE_CHANNEL_TABLE = "slide_channel"  # Course table
SLIDE_SLIDE_TABLE = "slide_slide"      # Slide/video table

# Odoo default language code
DEFAULT_LANG = "en_US"

# Logging settings
LOG_LEVEL = "INFO"