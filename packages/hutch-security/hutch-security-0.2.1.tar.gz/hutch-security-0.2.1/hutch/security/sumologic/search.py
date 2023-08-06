"""Provides SumoLogic search wrappers."""

import datetime
import time
from typing import Iterable

from hutch.security.sumologic import base
from hutch.security.sumologic.constants import (
    PAGE_SIZE,
    SEARCH_STATE_CANCELLED,
    SEARCH_STATE_DONE,
)
from hutch.security.sumologic.exceptions import SearchException, SearchTimeout
from hutch.security.sumologic.models import SearchJob, SearchJobMessage, SearchJobRecord


class Client(base.Client):
    """Provides a SumoLogic search client."""

    def records(self, job_id: str) -> Iterable[SearchJobRecord]:
        """Yields records until there are none left.

        :param job_id: The search job identifier to return records for.
        """
        offset = 0

        while True:
            result = self.client.search_job_records(
                {"id": job_id}, limit=PAGE_SIZE, offset=offset
            )

            # We can't deserialise directly into the model here as we want to unnest all
            # data from under 'map'.
            count = len(result.get("records", []))
            offset += count

            records = []
            for record in result.get("records", []):
                records.append(SearchJobRecord(**record["map"]))

            # Loop until we receive less results than we requested.
            if count == PAGE_SIZE:
                yield records
            else:
                break

        # Yield the final page.
        yield records

    def messages(self, job_id: str) -> Iterable[SearchJobMessage]:
        """Yields messages until there are none left.

        :param job_id: The search job identifier to return messages for.
        """
        offset = 0

        while True:
            result = self.client.search_job_messages(
                {"id": job_id},
                limit=PAGE_SIZE,
                offset=offset,
            )

            # We can't deserialise directly into the model here as we want to unnest all
            # data from under 'map'.
            count = len(result.get("messages", []))
            offset += count

            messages = []
            for message in result.get("messages", []):
                messages.append(SearchJobMessage(**message["map"]))

            # Loop until we receive less messages than we requested.
            if count == PAGE_SIZE:
                yield messages
            else:
                break

        # Yield the final page.
        yield messages

    def query(
        self,
        query: str,
        start: datetime.datetime,
        end: datetime.datetime,
        timeout: int = 600,
        interval: int = 10,
    ) -> SearchJob:
        """Syncronously execute a query and return the results.

        :param query: A search query to execute.
        :param start: A date stamp to constrain the query (from).
        :param end: A date stamp to constrain the query (to).
        :param timeout: The maximum duration to wait for results from the API, in
            seconds.
        :param interval: The time to wait between requests to the API to check query
            status, in seconds.

        :return: Search metadata.
        """
        time_start = time.time()
        epoch = datetime.datetime.utcfromtimestamp(0).replace(
            tzinfo=datetime.timezone.utc
        )

        # Queries are submitted with time components as miliseconds since epoch to avoid
        # the need to parse and pass a timezone to the API.
        job = self.client.search_job(
            query,
            fromTime=int((start - epoch).total_seconds() * 1000),
            toTime=int((end - epoch).total_seconds() * 1000),
        )

        # Poll the job status until timeout, or the API indicates the job is complete.
        while True:
            status = self.client.search_job_status(job)

            if status.get("state") == SEARCH_STATE_DONE:
                break

            if status.get("state") == SEARCH_STATE_CANCELLED:
                break

            # Wait and check for timeout.
            time.sleep(interval)

            if time.time() - time_start > timeout:
                raise SearchTimeout(
                    "Search did not complete before a client-side timeout was reached."
                )

        # Raise errors as exceptions.
        errors = status.get("pendingErrors", [])
        if len(errors) > 0:
            raise SearchException(f"Search query returned errors: {', '.join(errors)}")

        return SearchJob(id=job.get("id"), **status)
