#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


def get_db():
    # Retrieve credentials from environment variables with defaults
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish and return a connection to the database
    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return connection
