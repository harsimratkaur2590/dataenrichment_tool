"""
Configuration file for Apollo Data Enrichment Tool
"""
import os
from typing import Optional

def get_apollo_api_key() -> Optional[str]:
    """
    Get Apollo API key from environment variable or return None
    """
    return os.getenv('APOLLO_API_KEY')

def validate_api_key(api_key: str) -> bool:
    """
    Basic validation for API key format
    """
    if not api_key or len(api_key.strip()) < 10:
        return False
    return True

