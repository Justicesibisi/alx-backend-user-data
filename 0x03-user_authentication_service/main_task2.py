#!/usr/bin/env python3
"""
Main file to test find_user_by method in the DB class.
"""
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# Add a user to the database
user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

# Find the user by email
find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

# Attempt to find a non-existent user
try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

# Attempt to query using an invalid filter
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")

