"""
This file consists of settings needed to run Flask application along with Database configuration Details
"""

MONGO_URI = "mongodb://localhost:27017/ScienceAlerts"
JWT_SECRET_KEY = "I dont know man".encode('utf-8')
CORS_HEADERS = "Content-Type"
CSRF_ENABLED = True
USER_ENABLE_EMAIL = True