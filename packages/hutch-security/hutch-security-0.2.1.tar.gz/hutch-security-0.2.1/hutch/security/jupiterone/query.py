"""Provides JupiterOne query wrappers."""

import json
import time
from typing import Any, Dict, Iterable, Optional

import jmespath
import requests

from hutch.security.jupiterone.constants import (
    API_ENDPOINT,
    API_ENDPOINT_GRAPHQL,
    JMESPATH_J1QL_DATA,
    QUERY_J1QL_DEFERRED,
    QUERY_J1QL_ENTITY_RAW_DATA_LEGACY,
    STATUS_QUERY_IN_PROG,
)
from hutch.security.jupiterone.exceptions import QueryException, QueryTimeout
from hutch.security.jupiterone.models import (
    DeferredQuery,
    DeferredQueryStatus,
    QueryResponse,
    RawDataLegacy,
)


class Client:
    """Provides a JupiterOne query client."""

    def __init__(self, account: str, token: str, api_url: str = API_ENDPOINT):
        """Initialise a JupiterOne query client.

        :param account: The JupiterOne account ID to authenticate with.
        :param token: The JupiterOne token to authenticate with.
        :param api_url: The JupiterOne API endpoint to interact with.
        """
        self.api = api_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "LifeOmic-Account": account,
        }

    def _parse_graphql_errors(self, body: str) -> str:
        """Parses errors from a GraphQL response, returning a string.

        This method accepts a string, rather than JSON, as it may be called in exception
        handlers where attempts to call .json() on a response object would also need
        to be handled.

        :param response: The response from the API as a string.

        :return: A string containing errors encountered.
        """
        try:
            response = json.loads(body)
            errors = response.get("errors", [])
        except json.JSONDecodeError:
            return ""

        return ", ".join(error.get("message") for error in errors)

    def _get(
        self,
        uri: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Performs an HTTP GET request.

        This method wraps requests to ensure application / GraphQL errors are returned
        as part of the exception.

        :param url: URL to perform the HTTP GET against.
        :param headers: Dictionary of headers to add to the request.
        :param payload: Dictionary of data to pass as JSON in the request.
        :param params: HTTP parameters to add to the request.

        :return: A requests Response object.
        """
        try:
            response = requests.get(uri, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise QueryException(err) from None

        # Parse out any application errors and raise an exception if present.
        errors = self._parse_graphql_errors(response.text)
        if errors:
            raise QueryException(errors) from None

        return response

    def _post(
        self,
        uri: str,
        headers: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Performs an HTTP POST request.

        This method wraps requests to ensure application / GraphQL errors are returned
        as part of the exception.

        :param url: URL to perform the HTTP GET against.
        :param headers: Dictionary of headers to add to the request.
        :param payload: Dictionary of data to pass as JSON in the request.
        :param params: HTTP parameters to add to the request.

        :return: A requests Response object.
        """
        try:
            response = requests.post(uri, headers=headers, json=payload, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise QueryException(err) from None

        # Parse out any application errors and raise an exception if present.
        errors = self._parse_graphql_errors(response.text)
        if errors:
            raise QueryException(errors) from None

        return response

    def deferred_status(self, status_url: str) -> DeferredQueryStatus:
        """Returns the status of a deferred query.

        :param status_url: The status URL of the deferred query.

        :return: A deferred query status object.
        """
        try:
            status = self._get(status_url)
        except QueryException as err:
            raise QueryException(f"Failed to get results for query: {err}") from None

        # Return the deferred query status.
        return DeferredQueryStatus(status_url=status_url, **status.json())

    def deferred(
        self,
        query: str,
        cursor: str = "",
        include_deleted: bool = False,
    ) -> DeferredQuery:
        """Performs a deferred query, returning a deferred query object.

        :param query: The JupiterOne query to execute.
        :param cursor: The cursor for the next page of results to fetch, returned from
            a previous query.
        :param include_deleted: Whether to include 'recently deleted' objects from
            JupiterOne.

        :return: A deferred query object.
        """
        endpoint = f"{self.api}{API_ENDPOINT_GRAPHQL}"

        # It's a little confusing, but the query provided by the user is actually a
        # variable passed to the canned J1QL_DEFERRED GraphQL query. Additionally,
        # all original parameters must be provided when cursing / paging over results.
        payload = {
            "query": QUERY_J1QL_DEFERRED,
            "variables": {
                "query": query,
                "cursor": cursor,
                "includeDeleted": include_deleted,
                "deferredResponse": "FORCE",
            },
        }

        # Schedule the query.
        try:
            schedule = self._post(endpoint, headers=self.headers, payload=payload)
        except QueryException as err:
            raise QueryException(f"Failed to submit query to J1: {err}") from None

        # Return a deferred query object, rather than querying for status and returning
        # a status object. This is done as the J1 API doesn't appear to allow returning
        # the original query as part of a GraphQL response, and requires that the
        # original query be specified when paging over results.
        status = jmespath.search(JMESPATH_J1QL_DATA, schedule.json())

        return DeferredQuery(
            query=query,
            include_deleted=include_deleted,
            status_url=status.get("url"),
        )

    def query(
        self,
        query: str,
        cursor: str = "",
        interval: int = 5,
        timeout: int = 300,
        include_deleted: bool = False,
    ) -> QueryResponse:
        """Syncronously performs a JupiterOne search, returning a response object.

        :param query: The JupiterOne query to execute.
        :param cursor: The cursor to use when retrieving results, used for pagination.
        :param timeout: The maximum time to wait for results (in seconds).
        :param interval: The time to wait between requests to the API to check query
            status, in seconds.
        :param include_deleted: Whether to include 'recently deleted' objects from
            JupiterOne.

        :return: A Query response object.
        """
        time_start = time.time()

        # Schedule the query, and poll for status change. All queries use the deferred
        # API, as otherwise long queries will timeout.
        scheduled = self.deferred(query, cursor=cursor, include_deleted=include_deleted)

        while True:
            try:
                status = self.deferred_status(scheduled.status_url)
            except QueryException as err:
                raise QueryException(f"Failed to get status for query: {err}") from None

            # Check if the query has complete.
            if status.status != STATUS_QUERY_IN_PROG:
                break

            # Wait and check for timeout.
            time.sleep(interval)
            if time.time() - time_start > timeout:
                message = "Search did not complete before a client timeout was reached."
                raise QueryTimeout(message) from None

        # Fetch and return a results object. Note: this final request falls outside
        # of the timeout block, as the results are ready, we just need to get them.
        try:
            results = self._get(status.url)
        except QueryException as err:
            raise QueryException(f"Failed to get results for query: {err}") from None

        # Generate results and return to the caller. Note: It's up to the caller to
        # paginate, to reduce memory footprint.
        data = results.json()

        return QueryResponse(
            query=query,
            count=data.get("totalCount"),
            cursor=data.get("cursor", None),
            results=data.get("data", []),
            include_deleted=include_deleted,
        )

    def raw(self, entity_id: str, source_id: str):
        """Perform a query to request Raw entity data.

        :param entity_id: The id of the J1 entity to fetch raw data for.
        :param source_id: The id of the source / integration that the entity was fetched
            by. This is usually the value of the '_integrationInstanceId' from an entity
            which has been retrieved previously.

        :return: A legacy raw data object.
        """
        endpoint = f"{self.api}{API_ENDPOINT_GRAPHQL}"

        # It's a little confusing, but the query provided by the user is actually a
        # variable passed to the canned J1QL_DEFERRED GraphQL query. Additionally,
        # all original parameters must be provided when cursing / paging over results.
        payload = {
            "query": QUERY_J1QL_ENTITY_RAW_DATA_LEGACY,
            "variables": {
                "entity_id": entity_id,
                "source_id": source_id,
            },
        }

        # Execute the query synchronously, as this API does not appear to support async.
        try:
            results = self._post(endpoint, headers=self.headers, payload=payload)
        except QueryException as err:
            raise QueryException(f"Failed to submit query to J1: {err}") from None

        try:
            data = results.json()["data"]["entityRawDataLegacy"]
        except KeyError as err:
            raise QueryException(f"No results were returned by J1: {err}") from None

        # We can unzip straight into the native object as the field mapping matches the
        # defined schema. Pydantic will handle unwinding any nested objects for us. It's
        # great!
        return RawDataLegacy(**data)

    def perform(
        self,
        query: str,
        interval: int = 5,
        timeout: int = 300,
        include_deleted: bool = False,
    ) -> Iterable[QueryResponse]:
        """Perform a query and page over results until there are none left.

        :param query: The JupiterOne query to execute.
        :param timeout: The maximum time to wait for results (in seconds).
        :param interval: The time to wait between requests to the API to check query
            status, in seconds.
        :param include_deleted: Whether to include 'recently deleted' objects from
            JupiterOne.

        This is the simplest way to use this library, as results will be returned until
        no more results are available.
        """
        # Query for the first page of results, and then loop until no more pages are
        # returned.
        result = self.query(
            query=query,
            timeout=timeout,
            interval=interval,
            include_deleted=include_deleted,
        )

        while result.cursor:
            yield result

            # Grab the next page.
            result = self.query(
                cursor=result.cursor,
                query=query,
                timeout=timeout,
                interval=interval,
                include_deleted=include_deleted,
            )

        # Yield the final page.
        yield result
