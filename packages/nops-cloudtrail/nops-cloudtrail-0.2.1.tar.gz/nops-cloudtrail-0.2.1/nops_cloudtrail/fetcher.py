from datetime import datetime
from functools import cached_property

import boto3

from .bucket import CloudTrailBucket
from .data_types import CloudTrailTrailEntry
from .exceptions import CloudTrailTrailNotFound


class CloudTrailFetcher:
    def __init__(self, session: boto3.Session):
        self.session = session

    @cached_property
    def cloudtrail_trail(self) -> CloudTrailTrailEntry:
        trails_list = self._get_suitable_trails(self._list_trails())

        if trails_list:
            return trails_list[0]
        else:
            raise CloudTrailTrailNotFound

    # calls: describe_trails, get_trail_status, list_trails
    def _list_trails(self) -> list[CloudTrailTrailEntry]:
        client = self.session.client("cloudtrail", region_name="eu-central-1")
        available_trails = client.list_trails()
        trail_arns = [el["TrailARN"] for el in available_trails["Trails"]]

        enabled_trails = []
        trail_description = client.describe_trails(trailNameList=trail_arns)

        enabled_trails = []
        for trail_arn in trail_arns:
            status = client.get_trail_status(Name=trail_arn)
            description = [key for key in trail_description["trailList"] if key["TrailARN"] == trail_arn][0]
            item = {"status": status, "description": description}
            enabled_trails.append(CloudTrailTrailEntry(**item))

        return enabled_trails

    def _get_suitable_trails(self, trail_list: list[CloudTrailTrailEntry]) -> list[CloudTrailTrailEntry]:
        suitable_trails = []
        for trail in trail_list:
            if not trail.status.IsLogging:
                continue

            # Confirm that trail has full coverage.
            is_multi_region = trail.description.IsMultiRegionTrail
            is_global = trail.description.IncludeGlobalServiceEvents

            # TODO check bucket access
            bucket_name = trail.description.S3BucketName

            # NOTE: this library is not capable of reading encrypted trails as of now.
            is_encrypted = trail.description.KmsKeyId

            if (is_multi_region and is_global and bucket_name) and not is_encrypted:
                suitable_trails.append(trail)

        return suitable_trails

    def fetch(self, start: datetime, end: datetime, event_format="raw", threads_count: int = 30):
        bucket = CloudTrailBucket(session=self.session, trail=self.cloudtrail_trail, threads_count=threads_count)
        yield from bucket.get_events(
            start=start,
            end=end,
            event_format=event_format,
        )
