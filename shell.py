# python -i shell.py
# noqa: F401
from app.models.mysql import User, UserNotification, Notification
from app.db.connection import MySqlSession


session = MySqlSession()
