#!/usr/bin/env python3
"""
Module to filter PII fields in log messages and connect to a database.
"""

import os
import mysql.connector
from mysql.connector import connection

# Define get_db to connect securely using environment variables
def get_db() -> connection.MySQLConnection:
    """
    Returns a connection to the database using environment variables for credentials.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish and return the database connection
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )