#!/usr/bin/env python3
"""
Main file
"""

import logging
from filtered_logger import get_logger, PII_FIELDS

logger = get_logger()
logger.info("name=Alice;email=alice@example.com;ssn=123-45-6789;phone=555-1234;date_of_birth=1990-01-01;")

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS:", len(PII_FIELDS))