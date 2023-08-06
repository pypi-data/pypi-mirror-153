class CloudTrailTrailNotFound(Exception):
    """Raised when CloudTrail Trail is not found within account"""


class CloudTrailTrailNoAccess(Exception):
    """Raised when CloudTrail access is not present"""
