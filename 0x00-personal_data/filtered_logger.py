#!/usr/bin/env python3
"""obfuscates certain data fields"""

import logging
from typing import List
import re
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a MySQLConnection object for accessing a db"""
    db_config = {
        "user": os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        "host": os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        "password": os.getenv("PERSONAL_DATA_DB_PASSWORD", "root"),
        "database": os.getenv("PERSONAL_DATA_DB_NAME", ""),
    }
    # host = os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
    # user = os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
    # password = os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    # database = os.getenv("PERSONAL_DATA_DB_NAME"),

    cnx = mysql.connector.connection.MySQLConnection(**db_config)
    return cnx


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """obfuscates certain parameters"""
    for f in fields:
        message = re.sub(f"{f}=.*?{separator}",
                         f"{f}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """returns a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format method"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
