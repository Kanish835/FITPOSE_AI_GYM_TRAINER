"""
Database connector for the Smart AI Gym Trainer application.

This module provides functions to connect to the MySQL database
and perform CRUD operations on the user data and workout logs.
"""

import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create a connection to the MySQL database.
    
    Returns:
        connection: MySQL database connection object if successful, None otherwise
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='smart_gym_trainer'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def execute_query(connection, query, params=None):
    """
    Execute a SQL query on the database.
    
    Args:
        connection: MySQL database connection
        query: SQL query string
        params: Parameters for the query (for prepared statements)
        
    Returns:
        bool: True if query executed successfully, False otherwise
    """
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()

def execute_read_query(connection, query, params=None):
    """
    Execute a read query on the database.
    
    Args:
        connection: MySQL database connection
        query: SQL query string
        params: Parameters for the query (for prepared statements)
        
    Returns:
        list: Result of the query as a list of tuples, None if error occurs
    """
    cursor = connection.cursor()
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()