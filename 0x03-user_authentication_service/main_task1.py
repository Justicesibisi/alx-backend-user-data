#!/usr/bin/env python3
"""
Main file to test add_user method in the DB class.
"""

from db import DB

my_db = DB()

# Adding the first user
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

# Adding the second user
user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

