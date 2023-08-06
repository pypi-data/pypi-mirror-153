"""Provides SumoLogic related models for data mapping."""

import datetime
from typing import List

from pydantic import BaseModel, Extra, Field, validator


class SearchJobField(BaseModel):
    """Maps message 'fields' returned by a search job into native data types."""

    name: str
    key_field: bool = Field(None, alias="keyField")
    field_type: str = Field(None, alias="fieldType")


class SearchJobMessage(BaseModel, extra=Extra.allow):
    """Maps message records returned by a search job into native data types."""

    raw: str = Field(None, alias="_raw")
    source_host: str = Field(None, alias="_sourcehost")
    source_name: str = Field(None, alias="_sourcename")
    receipt_time: datetime.datetime = Field(None, alias="_receipttime")
    message_time: datetime.datetime = Field(None, alias="_messagetime")
    source_category: str = Field(None, alias="_sourcecategory")

    @validator("receipt_time", "message_time")
    def convert_usec_to_native(cls, v):  # noqa: B902
        """Converts a miliseconds since epoch timestamp to a native object."""
        if type(v) == datetime.datetime:
            return v

        return datetime.datetime.fromtimestamp(int(v), tz=datetime.timezone.utc)


class SearchJobRecord(BaseModel, extra=Extra.allow):
    """Maps records returned by a search job into native data types."""


class SearchJobHistogramBucket(BaseModel, extra=Extra.allow):
    """Maps a search job's 'histogram bucket' entries into native data types."""

    length: int
    count: int
    start_timestamp: datetime.datetime = Field(None, alias="startTimestamp")

    @validator("start_timestamp")
    def convert_usec_to_native(cls, v):  # noqa: B902
        """Converts a miliseconds since epoch timestamp to a native object."""
        if type(v) == datetime.datetime:
            return v

        return datetime.datetime.fromtimestamp(int(v), tz=datetime.timezone.utc)


class SearchJob(BaseModel, extra=Extra.allow):
    """Maps a search job into native data types."""

    id: str
    state: str
    record_count: int = Field(None, alias="recordCount")
    message_count: int = Field(None, alias="messageCount")
    pending_errors: List[str] = Field(None, alias="pendingErrors")
    pending_warnings: List[str] = Field(None, alias="pendingWarnings")
    histogram_buckets: List[SearchJobHistogramBucket] = Field(
        None,
        alias="histogramBuckets",
    )
