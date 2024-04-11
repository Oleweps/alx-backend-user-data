#!/usr/bin/env python3
""" obfuscate logs """

import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def create_pattern(fields: List[str], sep: str) -> str:
    """create regex pattern for fields"""
    return "|".join(
        [re.escape(field) + r"=[^" + sep + "]+(?=" + sep
         + ")" for field in fields]
    )


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """obfuscate log data"""
    return re.sub(
        create_pattern(fields, separator),
        lambda x: x.group(0).split("=")[0] + "=" + redaction,
        message,
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize classs """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the LogRecord into a string """
        return filter_datum(self._fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ get logger function """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    """get database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", default="root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", default="")
    host = os.getenv("PERSONAL_DATA_DB_HOST", default="localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return MySQLConnection(
        host=host, user=username, password=password, database=database
    )


def main():
    """ Read and filter data """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = ["name", "email", "phone", "ssn", "password",
              "ip", "last_login", "user_agent"]
    log = get_logger()

    for row in cursor:
        arr = []
        for idx in range(len(fields)):
            arr.append(f"{fields[idx]}={row[idx]}")
        message = "; ".join(arr)
        message += ";"
        record = logging.LogRecord("user_data", logging.INFO,
                                   None, None, message, None, None)
        log.handle(record)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
