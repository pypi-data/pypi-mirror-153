from datetime import datetime
from datetime import timedelta
from datetime import timezone

import boto3
import pytest

from nops_cloudtrail import CloudTrailFetcher


@pytest.fixture
def aws_session():
    return boto3.Session()


@pytest.fixture
def cloudtrail_fetcher(aws_session):
    return CloudTrailFetcher(session=aws_session)


@pytest.fixture
def fetcher_event_boto3(cloudtrail_fetcher):
    now = datetime.now(timezone.utc)
    before = now - timedelta(hours=1)
    event = next(cloudtrail_fetcher.fetch(start=before, end=now, event_format="boto3", threads_count=1))
    return event


@pytest.fixture
def fetcher_event_raw(cloudtrail_fetcher):
    now = datetime.now(timezone.utc)
    before = now - timedelta(hours=1)
    event = next(cloudtrail_fetcher.fetch(start=before, end=now, event_format="raw", threads_count=1))
    return event


def test_cloudtrail_trail_availability(cloudtrail_fetcher):
    assert cloudtrail_fetcher.cloudtrail_trail


def test_cloudtrail_get_events_raw_format(fetcher_event_raw):
    event = fetcher_event_raw
    assert event
    assert isinstance(event, dict)
    assert event["eventName"]
    assert "EventName" not in event


def test_cloudtrail_fetcher_is_s3_fetching_available(cloudtrail_fetcher):
    assert cloudtrail_fetcher.is_s3_fetching_available


def test_cloudtrail_get_events_boto3_format_matching(fetcher_event_boto3):
    event = fetcher_event_boto3

    lookup_attributes = [{"AttributeKey": "EventId", "AttributeValue": event["EventId"]}]
    boto3_response = boto3.client("cloudtrail", region_name=event["Region"]).lookup_events(
        LookupAttributes=lookup_attributes
    )

    assert len(boto3_response["Events"]) == 1
    boto3_event = boto3_response["Events"][0]

    # Some extra keys should be popped for comparison.
    event.pop("Region")
    event.pop("Username")

    boto3_event.pop("AccessKeyId", None)
    boto3_event.pop("Username", None)

    assert isinstance(boto3_event["CloudTrailEvent"], str)
    assert isinstance(event["CloudTrailEvent"], str)

    assert set(boto3_event.keys()) == set(event.keys())

    # Compare responses
    diff = {}
    for k, v in event.items():
        if k in ["CloudTrailEvent", "Resources"]:
            continue

        if boto3_event[k] != v:
            diff[k] = [v, boto3_event[k]]

    assert not diff
