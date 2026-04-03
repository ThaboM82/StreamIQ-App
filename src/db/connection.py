"""
Database Connection Utility
===========================

Provides a helper function to establish and manage
connections to the StreamIQ MySQL database.
"""

import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Create and return a MySQL database connection.

    Environment Variables Required
    ------------------------------
    DB_HOST : str
        Database host (e.g., 'localhost' or AWS RDS endpoint)
    DB_USER : str
        Database username
    DB_PASSWORD : str
        Database password
    DB_NAME : str
        Database name

    Returns
    -------
    mysql.connector.connection.MySQLConnection
        Active database connection object
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "streamiq")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        raise RuntimeError(f"Database connection failed: {e}")
