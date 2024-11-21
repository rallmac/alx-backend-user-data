#!/usr/bin/env python3
"""This function returns a log message obfuscated"""

import re


def filter_datum(fields, redaction, message, seperator):
    """Obfuscates specified fields in a log message"""
    escaped_fields = '|'.join(re.escape(field) for field in fields)
    pattern = f"({escaped_fields})=.*?{re.escape(seperator)}"
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}{seperator}", message)
