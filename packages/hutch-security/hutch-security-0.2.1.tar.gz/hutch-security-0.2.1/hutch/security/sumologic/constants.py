"""Provides SumoLogic related constants."""

API_ENDPOINT = "https://api.sumologic.com/api"

# How many results we should request per page when paging over results.
PAGE_SIZE = 1000

# Search states are strings, so we map them to constants to remove string literals from
# being scattered around the place.
SEARCH_STATE_DONE = "DONE GATHERING RESULTS"
SEARCH_STATE_CANCELLED = "CANCELLED"
