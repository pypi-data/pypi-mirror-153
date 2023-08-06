"""Provides JupiterOne related constants."""

API_ENDPOINT = "https://api.us.jupiterone.io"
API_ENDPOINT_GRAPHQL = "/graphql"

# Status messages from deferred queries.
STATUS_QUERY_IN_PROG = "IN_PROGRESS"

# Queries submitted are actually encapsulated in the following GraphQL query.
QUERY_J1QL_DEFERRED = """
query J1QL(
  $query: String!,
  $variables: JSON,
  $cursor: String,
  $deferredResponse: DeferredResponseOption,
  $includeDeleted: Boolean
) {
  queryV1(
    query: $query,
    variables: $variables,
    deferredResponse: $deferredResponse,
    includeDeleted: $includeDeleted,
    cursor: $cursor
  ) {
    type
    url
  }
}
"""

QUERY_J1QL_ENTITY_RAW_DATA_LEGACY = """
query GetEntityRawData(
  $entity_id: String!,
  $source_id: String!,
  $name: String,
  $versionId: String
) {
  entityRawDataLegacy(
    entityId: $entity_id
    source: $source_id
    name: $name versionId:
    $versionId
  ) {
    entityId payload {
      ...on RawDataJSONEntityLegacy {
        contentType name JSONData: data __typename
      }...on RawDataTextEntityLegacy {
        contentType name TextData: data __typename
      }
      __typename
    }
    __typename
  }
}
"""

# Querying for
# The JMESPath of the node which contains the relevant data is defined as a constant
# here as the result from the API includes the 'scheduled' query name in the path:
# queryV1 below matches the 'queryV1' reference in QUERY_J1QL_*.
JMESPATH_J1QL_DATA = "data.queryV1"
