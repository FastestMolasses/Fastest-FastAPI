from datetime import datetime
from app.db.connection import MySQLTableBase

from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column


class User(MySQLTableBase):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                    primary_key=True,
                                    autoincrement=True)
    lastActive: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())
    joinDate: Mapped[datetime] = mapped_column(DateTime,
                                               server_default=func.now())

    # One-to-many relationship with UserNotification
    notifications: Mapped[list['UserNotification']] = relationship(secondary='UserNotification',
                                                                   back_populates='users',
                                                                   lazy='select',
                                                                   cascade='all, delete')
    # One-to-many relationship with Post
    posts: Mapped[list['Post']] = relationship(secondary='Post',
                                               back_populates='user',
                                               lazy='select')
    # One-to-one relationship with Profile
    profile: Mapped['Profile'] = relationship(secondary='Profile',
                                              back_populates='user',
                                              uselist=False,
                                              lazy='select')

    def __repr__(self) -> str:
        return f'<User UserID={self.id} LastActive={self.lastActive}>'


class UserNotification(MySQLTableBase):
    """
        Association Table for User and Notification.
        Represents the notifications received by a user.
    """
    __tablename__ = 'UserNotification'

    userID: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                        ForeignKey(
                                            'User.id', ondelete='CASCADE'),
                                        primary_key=True)
    notificationID: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                                ForeignKey(
                                                    'Notification.id', ondelete='CASCADE'),
                                                primary_key=True)
    read: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f'<UserNotification UserID={self.userID} NotificationID={self.notificationID}>'


class Notification(MySQLTableBase):
    """
        Notification class representing the notifications sent to the users.
    """
    __tablename__ = 'Notification'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                    primary_key=True,
                                    autoincrement=True)
    message: Mapped[str] = mapped_column(String(length=256), primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users: Mapped[list['UserNotification']] = relationship(secondary='UserNotification',
                                                           back_populates='notifications',
                                                           lazy='select',
                                                           passive_deletes=True)

    def __repr__(self) -> str:
        return f'<Notification ID={self.id}>'


class Post(MySQLTableBase):
    """
        Post class representing the posts created by the users.
    """
    __tablename__ = 'Post'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                    primary_key=True,
                                    autoincrement=True)
    content: Mapped[str] = mapped_column(String(length=1024))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), ForeignKey('User.id'))

    # Relationship with User
    user: Mapped['User'] = relationship('User', back_populates='posts')

    def __repr__(self) -> str:
        return f'<Post ID={self.id}>'


class Profile(MySQLTableBase):
    """
        Profile class representing the profile of each user.
    """
    __tablename__ = 'Profile'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True),
                                    primary_key=True,
                                    autoincrement=True)
    bio: Mapped[str] = mapped_column(String(length=256))
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), ForeignKey('User.id'), unique=True)

    # Relationship with User
    user: Mapped['User'] = relationship(
        'User', back_populates='profile', uselist=False)

    def __repr__(self) -> str:
        return f'<Profile ID={self.id}>'
