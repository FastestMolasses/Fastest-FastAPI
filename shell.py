"""
This file is used to run a shell with all the models and the session
loaded. This is useful for debugging and testing.
"""
# python -i shell.py
# noqa: F401
from app.models.mysql import User, UserNotification, Notification
from app.db.connection import MySqlSession


session = MySqlSession()
