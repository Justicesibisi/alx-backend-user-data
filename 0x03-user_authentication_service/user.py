#!/usr/bin/env python3
"""
Defines the User model for a database table named users.
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model mapped to the 'users' table.

    Attributes:
        id (int): Primary key, auto-incremented.
        email (str): User's email, non-nullable.
        hashed_password (str): User's hashed password, non-nullable.
        session_id (str): Session ID, nullable.
        reset_token (str): Reset token, nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


# Uncomment the following if you need to create the table for testing:
# engine = create_engine('sqlite:///example.db')  # Replace with your DB URL
# Base.metadata.create_all(engine)
