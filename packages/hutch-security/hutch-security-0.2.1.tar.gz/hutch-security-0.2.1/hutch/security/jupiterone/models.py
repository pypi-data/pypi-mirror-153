"""Provides JupiterOne related models for data mapping."""

import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, Field, validator


class ResultEntities(BaseModel, extra=Extra.allow):
    """Maps result entities into native data types."""

    id: str = Field(None, alias="_id")
    deleted: bool = Field(None, alias="_deleted")
    created_on: datetime.datetime = Field(None, alias="_createdOn")
    deleted_on: Optional[datetime.datetime] = Field(None, alias="_endOn")


class QueryResult(BaseModel, extra=Extra.forbid):
    """Maps a query result into native data types.

    Properties in JupiterOne are not mapped, they're just put into a dictionary. This is
    as they may contain dot (.) characters, and are usually in camelCase.
    """

    id: Optional[str]
    entity: Optional[ResultEntities]
    properties: Dict[str, Any]


class QueryResponse(BaseModel, extra=Extra.forbid):
    """Maps a query response into native data types."""

    count: Optional[int]
    query: str
    cursor: Optional[str]
    results: List[QueryResult]
    include_deleted: bool

    @validator("results", each_item=True, pre=True)
    def remap_raw_properties(cls, v):  # noqa: B902
        """Remaps data returned by 'RETURNS' queries into the same properties model."""
        # Attempt to mitigate accidental match on RETURNS query with field names which
        # match 'entity' and 'properties'.
        if "entity" in v and "properties" in v:
            return v
        else:
            return {"properties": v}


class DeferredQuery(BaseModel, extra=Extra.forbid):
    """Maps a deferred query into native data types."""

    query: str
    status_url: str
    include_deleted: bool


class DeferredQueryStatus(BaseModel, extra=Extra.forbid):
    """Maps a deferred query status response into native data types."""

    url: Optional[str]
    status: str
    status_url: str
    correlation_id: str = Field(None, alias="correlationId")


class RawDataResult(BaseModel, extra=Extra.forbid):
    """Maps a "Raw Data" result into native data types."""

    name: str = Field(None, alias="name")
    type_name: str = Field(None, alias="__typename")
    content_type: str = Field(None, alias="contentType")

    # Text data is a field that contains the "raw" text/plain result of an entity, where
    # applicable.
    text: Optional[str] = Field(None, alias="TextData")

    # JSON data is a field that contains the "raw" JSON associated with an entity. We've
    # called this properties as 'json' cannot be used due to a conflict with BaseModel.
    # However, as "properties" is the same name as this data is referred to as in a
    # Query Response this isn't too bad.
    properties: Dict[str, Any] = Field(None, alias="JSONData")


class RawDataLegacy(BaseModel, extra=Extra.allow):
    """Maps a raw data legacy result into native data types."""

    entity_id: str = Field(None, alias="entityId")
    type_name: str = Field(None, alias="__typename")
    results: List[RawDataResult] = Field(None, alias="payload")
