from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CloudTrailStatusResponse(BaseModel):
    IsLogging: bool
    LatestDeliveryError: Optional[str]
    LatestNotificationError: Optional[str]
    LatestDeliveryTime: datetime
    LatestNotificationTime: Optional[datetime]
    StartLoggingTime: datetime
    StopLoggingTime: Optional[datetime]
    LatestCloudWatchLogsDeliveryError: Optional[str]
    LatestCloudWatchLogsDeliveryTime: Optional[datetime]
    LatestDigestDeliveryTime: Optional[datetime]
    LatestDigestDeliveryError: Optional[str]
    LatestDeliveryAttemptTime: str
    LatestNotificationAttemptTime: str
    LatestNotificationAttemptSucceeded: str
    LatestDeliveryAttemptSucceeded: str
    TimeLoggingStarted: str
    TimeLoggingStopped: str


class CloudTrailDescriptionResponse(BaseModel):
    Name: str
    TrailARN: str
    S3BucketName: str
    S3KeyPrefix: Optional[str]
    SnsTopicName: Optional[str]
    SnsTopicARN: Optional[str]
    IncludeGlobalServiceEvents: bool
    IsMultiRegionTrail: bool
    HomeRegion: str
    LogFileValidationEnabled: bool
    CloudWatchLogsLogGroupArn: Optional[str]
    CloudWatchLogsRoleArn: Optional[str]
    KmsKeyId: Optional[str]
    HasCustomEventSelectors: bool
    HasInsightSelectors: bool
    IsOrganizationTrail: bool


class CloudTrailTrailEntry(BaseModel):
    status: CloudTrailStatusResponse
    description: CloudTrailDescriptionResponse


class LogPath(BaseModel):
    date: date
    prefix: str


class BucketContentEntry(BaseModel):
    ETag: str
    Key: str
    LastModified: datetime
    Owner: dict[str, str]
    Size: int
    StorageClass: str
