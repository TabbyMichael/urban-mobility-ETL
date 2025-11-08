import json
from datetime import datetime
from typing import Dict, Any

def format_response(data: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    """Format API response with consistent structure"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code,
        "data": data
    }

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> tuple[bool, str]:
    """Validate that required fields are present in data"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, ""

def parse_date_range(start_date: str, end_date: str) -> tuple[datetime, datetime]:
    """Parse date range strings into datetime objects"""
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        return start, end
    except ValueError as e:
        raise ValueError(f"Invalid date format: {str(e)}")