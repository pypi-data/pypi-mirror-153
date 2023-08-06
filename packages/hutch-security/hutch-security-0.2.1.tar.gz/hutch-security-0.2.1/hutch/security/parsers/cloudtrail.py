"""Provides parsers for extraction of fields from AWS cloudtrail data."""

import json

import jmespath

from hutch.security.parsers.exceptions import FieldNotFoundException


def user_identity(trail: str) -> str:
    """Attempts to extract a valid user identity from a trail.

    :param trail: An AWS CloudTrail trail as JSON.

    :return: The extracted user identity.
    """
    haystack = json.loads(trail)

    # If we have a source identity, we should preference it.
    source_identity = jmespath.search(
        "userIdentity.sessionContext.sourceIdentity",
        haystack,
    )
    if source_identity is not None:
        return source_identity

    # Otherwise, try and parse a user from the principal.
    principal_id = jmespath.search("userIdentity.principalId", haystack)
    if principal_id is not None:
        return principal_id.split(":")[1]

    raise FieldNotFoundException("Could not extract a user identity from trail")


def asg_name(trail: str) -> str:
    """Attempts to extract an Auto Scaling Group name from a trail.

    :param trail: An AWS CloudTrail trail as JSON.

    :return: The extracted ASG name.
    """
    haystack = json.loads(trail)

    # Auto Scaling group names are pulled from tags.
    tags = jmespath.search(
        "requestParameters.tagSpecificationSet.items[].tags[]",
        haystack,
    )

    if tags:
        for tag in tags:
            if tag["key"] == "aws:autoscaling:groupName":
                return tag["value"]

    raise FieldNotFoundException(
        "Could not extract an Auto Scaling Group name from trail"
    )
