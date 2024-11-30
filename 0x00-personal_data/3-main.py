#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()  # Get the database connection
cursor = db.cursor()  # Create a cursor to interact with the database
cursor.execute("SELECT COUNT(*) FROM users;")  # Execute the SQL query
for row in cursor:  # Fetch the result
    print(row[0])  # Print the count of users
cursor.close()  # Close the cursor
db.close()  # Close the database connection

