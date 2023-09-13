"""
In this example, we use SQLAlchemy's ORM to create a MySQL tables *without* foreign keys.
Instead, we create relationships in place of foreign keys. There are many reasons why
someone might want to not use foreign keys:
1. Schema flexibility
2. Cross-database relationships
3. Performance
4. database agnostic code
"""

from datetime import datetime
from app.types.jwt import Role
from sqlalchemy.sql import func
from app.db.connection import MySQLTableBase
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import relationship, Session, mapped_column, Mapped

# TODO: CHECK IF THESE RELATIONSHIPS LOAD LAZILY OR EAGERLY
# TODO: FIX WARNING ABOUT RELATIONSHIP COPYING COLUMN


class User(MySQLTableBase):
    """
        User class representing the user.
    """
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                    primary_key=True,
                                    autoincrement=True)
    address: Mapped[str] = mapped_column(String(length=42),
                                         primary_key=True,
                                         unique=True)
    lastActive: Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=func.now(),
                                                 onupdate=func.now())
    joinDate: Mapped[datetime] = mapped_column(DateTime,
                                               server_default=func.now())
    role: Mapped[int] = mapped_column(TINYINT(unsigned=True),
                                      default=Role.USER.value)
    isBetaUser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    notifications: Mapped[list['UserNotification']] = relationship(
        primaryjoin='User.id == foreign(UserNotification.userID)',
    )

    def load(self, session: Session) -> 'User':
        """
            Load the user's data from the database and return the user instance.
        """
        return session.query(User).filter_by(address=self.address).scalar()

    def __repr__(self) -> str:
        return f'<User UserID={self.id} Address={self.address} LastActive={self.lastActive}>'


class UserNotification(MySQLTableBase):
    """
        Association Table for User and Notification.
        Represents the notifications received by a user.
    """
    __tablename__ = 'UserNotification'

    userID: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), primary_key=True)
    notificationID: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), primary_key=True)
    read: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped[User] = relationship(
        primaryjoin='UserNotification.userID == foreign(User.id)'
    )
    notification: Mapped['Notification'] = relationship(
        primaryjoin='UserNotification.notificationID == foreign(Notification.id)'
    )

    def __repr__(self) -> str:
        return f'<UserNotification UserID={self.userID} NotificationID={self.notificationID}>'


class Notification(MySQLTableBase):
    """
        Notification class representing the notification sent to the users.
    """
    __tablename__ = 'Notification'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                    primary_key=True,
                                    autoincrement=True)
    message: Mapped[str] = mapped_column(String(length=256), primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    users: Mapped[list['UserNotification']] = relationship(
        primaryjoin='Notification.id == foreign(UserNotification.notificationID)',
    )

    def __repr__(self) -> str:
        return f'<Notification ID={self.id}>'
