import json
import logging
from datetime import datetime
from datetime import timedelta
from typing import Iterator

import dateutil.parser as dparser
import orjson


def _convert_resources_node(resources: list[dict[str, str]]) -> list[dict[str, str]]:
    output = []
    for resource in resources:
        output_resource = {
            "ResourceType": resource.get("type", ""),
            "ResourceName": resource["ARN"],
        }
        output.append(output_resource)

    return output


def convert_to_boto3(event):
    """
    Function to provide compatibility between Boto3 CT output from `.lookup_events()` and events
    fetched from the S3 bucket.
    """
    response = {}

    response["EventTime"] = dparser.parse(event["eventTime"])
    response["EventName"] = event["eventName"]
    response["EventId"] = event["eventID"]
    response["Region"] = event["awsRegion"]
    response["ReadOnly"] = json.dumps(event["readOnly"])

    response["Resources"] = _convert_resources_node(event.get("resources", []))
    response["EventSource"] = event["eventSource"]

    response["CloudTrailEvent"] = orjson.dumps(event)
    identity = event["userIdentity"]

    if (
        "sessionContext" in identity
        and "sessionIssuer" in identity["sessionContext"]
        and "userName" in identity["sessionContext"]["sessionIssuer"]
    ):
        response["Username"] = identity["sessionContext"]["sessionIssuer"]["userName"]

    elif "invokedBy" in identity and identity["invokedBy"] != "signin.amazonaws.com":
        response["Username"] = identity["invokedBy"]
    elif identity["type"] == "Root":
        response["Username"] = "root"
    elif "userName" in identity:
        response["Username"] = identity["userName"]
    elif "arn" in identity:
        response["Username"] = identity["arn"]
    elif "roleSessionName" in event.get("requestParameters") or {}:
        response["Username"] = event["requestParameters"]["roleSessionName"]
    else:
        logging.critical(f"Not handled event username {identity}")

    return response


def day_chunks(start: datetime, end: datetime) -> Iterator[list[datetime]]:
    """Splits interval in days"""

    if end < start:
        raise ValueError("Finishing date cannot be earlier than the starting one.")

    starting_date = start
    ending_date = end

    current_date = start

    while current_date < ending_date:
        # First loop
        if current_date == starting_date:
            yield [current_date, current_date.replace(hour=23, minute=59, second=59, microsecond=999999)]
            current_date = (
                datetime.combine(current_date.date(), datetime.min.time(), tzinfo=current_date.tzinfo)
                + timedelta(days=1)
                - timedelta(microseconds=1)
            )

        # Last loop
        elif (current_date + timedelta(microseconds=1)).date() == ending_date.date():
            yield [current_date + timedelta(microseconds=1), ending_date]
            current_date = ending_date

        else:
            chunk_start = current_date + timedelta(microseconds=1)
            chunk_end = (
                datetime.combine(chunk_start.date(), datetime.min.time(), tzinfo=current_date.tzinfo)
                + timedelta(days=1)
                - timedelta(microseconds=1)
            )
            yield [chunk_start, chunk_end]
            current_date = chunk_end
