#!/usr/bin/env python3
"""This module provides tools to filter and format log messages."""

import os
import re
import logging
from typing import List
import mysql.connector
from mysql.connector import MySQLConnection

# Define the PII_FIELDS constant
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields, redaction, message, separator):
    """Obfuscates specified fields in a log message."""
    escaped_fields = '|'.join(re.escape(field) for field in fields)
    pattern = f"({escaped_fields})=.*?{re.escape(separator)}"
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record to obfuscate sensitive information.
        """
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR
                )
        return super().format(record)


def get_logger() -> logging.Logger:
    """Create and configure a logger that obfuscates PII data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create and configure the StreamHandler
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    """Connect to MySQL database using credentials from
    environment variables
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
    return connection


def main() -> None:
    """Main function to log user data from the database"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    logger = get_logger()

    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        log_message = (
            f"name={row['name']}; email={row['email']}; phone={row['phone']}; "
            f"ssn={row['ssn']}; password={row['password']}; ip={row['ip']}; "
            f"last_login={row['last_login']}; user_agent={row['user_agent']};"
        )
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
