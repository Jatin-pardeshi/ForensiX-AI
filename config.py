import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '7ca9e2f6bc4e1b8273641a9a8d3eef543b39d1b02130e9e1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///forensix_core.db')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '0a831e5fcdb2c938d94e1c20847f9eab23d0e2c8139aa920')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'storage', 'evidence')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024 
    RATELIMIT_DEFAULT = "100 per minute"
    
    # NEW: Threat Intelligence API Keys
    VT_API_KEY = os.environ.get('VT_API_KEY','4a4bf9867acd2f3012c13ac62d92723acdb004dfc00adfb1895fe8509c8f7bfa') # Get a free key at virustotal.com