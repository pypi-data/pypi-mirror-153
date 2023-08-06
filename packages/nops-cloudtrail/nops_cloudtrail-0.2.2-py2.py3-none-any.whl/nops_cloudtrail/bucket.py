import gzip
import logging
from datetime import date
from datetime import datetime
from datetime import timedelta
from functools import cached_property
from multiprocessing.dummy import Pool
from queue import Empty
from queue import Queue
from threading import Thread
from typing import Any
from typing import Iterator
from typing import Union

import boto3
import botocore.exceptions
import orjson

from .data_types import BucketContentEntry
from .data_types import CloudTrailTrailEntry
from .data_types import LogPath
from .utils import convert_to_boto3
from .utils import day_chunks


class CloudTrailBucket:
    def __init__(self, session: boto3.Session, trail: CloudTrailTrailEntry, threads_count: int = 30):
        self.session: boto3.Session = session
        self.trail: CloudTrailTrailEntry = trail
        self.threads_count: int = threads_count

        self._tasks_queue = Queue()
        self._events_queue = Queue(maxsize=10_000)

    @cached_property
    def account_number(self) -> str:
        return self.session.client("sts").get_caller_identity().get("Account")

    @property
    def bucket(self) -> str:
        return self.trail.description.S3BucketName

    @property
    def s3_prefix(self) -> str:
        return self.trail.description.S3KeyPrefix or ""

    @cached_property
    def regions(self) -> list[str]:
        response = self.session.client("s3").list_objects(
            Bucket=self.bucket, Prefix=f"{self.logs_path}/", Delimiter="/"
        )
        regions = []
        for prefix in response["CommonPrefixes"]:
            region = prefix["Prefix"].replace(f"{self.logs_path}/", "").strip("/")
            regions.append(region)
        return regions
        # return ["us-west-2"] TODO debug debug debug

    @property
    def logs_path(self) -> str:
        """Returns absolute bucket path for CT folder"""
        return f"{self.s3_prefix}/AWSLogs/{self.account_number}/CloudTrail"

    def get_region_logs_path(self, region: str) -> str:
        """Returns absolute bucket path for region"""
        return f"{self.logs_path}/{region}"

    def get_logs_day_prefix(self, region: str, logs_date: date) -> str:
        logs_date_formatted = logs_date.strftime("%Y/%m/%d")
        return f"{self.get_region_logs_path(region)}/{logs_date_formatted}"

    def get_log_paths(self, start_date: date, delta: timedelta) -> list[LogPath]:
        paths = []
        for region in self.regions:
            for day in range(delta.days + 1):

                # Get prefix for that day
                current_date = start_date + timedelta(days=day)

                prefix = self.get_logs_day_prefix(region=region, logs_date=current_date)
                paths.append(LogPath(**{"date": current_date, "prefix": prefix}))
        return paths

    def get_objects(self, start: datetime, end: datetime) -> list[BucketContentEntry]:
        def _run(log_path: LogPath) -> list[BucketContentEntry]:
            paginator = self.session.client("s3").get_paginator("list_objects")
            operation_paramers = {
                "Bucket": self.bucket,
                "Prefix": log_path.prefix,
            }
            output = []
            for page in paginator.paginate(**operation_paramers):
                for item in page.get("Contents") or []:
                    if start <= item["LastModified"] <= end:
                        output.append(BucketContentEntry(**item))
            return output

        start_date = start.date()
        end_date = end.date()
        delta = end_date - start_date

        paths = self.get_log_paths(start_date=start_date, delta=delta)

        pool = Pool(10)
        response = pool.map(_run, paths)
        pool.close()
        pool.join()
        objects_list = []
        for element in response:
            objects_list += element
        return objects_list

    def _worker(self, event_format: str) -> bool:
        client = self.session.client("s3")
        while True:
            try:
                task = self._tasks_queue.get_nowait()
                events = _fetch_events_from_entry(
                    bucket=self.bucket, bucket_content=task, event_format=event_format, client=client
                )
                for event in events:
                    self._events_queue.put(event)

            except Empty:
                logging.debug("Worker exit.")
                return True

    def get_events(self, start: datetime, end: datetime, event_format: str) -> Iterator[dict]:
        for _start, _end in day_chunks(start=start, end=end):
            logging.debug(f"Pulling data from {_start} to {_end}")
            # Create threads
            worker_threads: list[Thread] = [
                Thread(target=self._worker, args=(event_format,), daemon=True) for _ in range(self.threads_count)
            ]

            # Fill the tasks queue
            tasks_counter = 0
            for bucket_content in self.get_objects(start=_start, end=_end):
                tasks_counter += 1
                self._tasks_queue.put(bucket_content)

            # Start threads after tasks are created.
            [t.start() for t in worker_threads]

            while True:
                try:
                    yield self._events_queue.get(block=True, timeout=0.1)
                except Empty:
                    any_alive = any([thread.is_alive() for thread in worker_threads])
                    if not any_alive:
                        for t in worker_threads:
                            t.join()
                        break


# TODO allow passing preferred bucket for trail usage
def _fetch_events_from_entry(bucket: str, bucket_content: BucketContentEntry, event_format: str, client: Any):
    events = []
    for try_num in range(0, 5):
        try:
            item_data = client.get_object(Bucket=bucket, Key=bucket_content.Key)
            events_json = gzip.decompress(item_data["Body"].read())
            events = orjson.loads(events_json).get("Records", [])
            break

        except botocore.exceptions.ReadTimeoutError:
            continue

    # Compatibility between S3 and API approaches
    for event in events:
        if event_format == "boto3":
            yield convert_to_boto3(event)
        elif event_format == "raw":
            yield event
        else:
            raise ValueError(f"Unsupported event format: {event_format}")
