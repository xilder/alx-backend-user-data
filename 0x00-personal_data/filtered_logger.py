#!/usr/bin/env python3
"""obfuscates certain data fields"""


from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str, messages: str,
        separator: str
    ) -> str:
    """obfuscates certain parameters"""
    for field in fields:
        messages = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", messages)
    return messages
