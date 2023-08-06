<img src="./docs/images/hutch.png" alt="Hutch" width="450px" />

## Hutch - Security Engineering Toolkit.

This toolkit provides a collection of widgets commonly used by the HashiCorp Security
Engineering team.

Why Hutch? Hutch provides a home for smaller tools which aren't large enough for a home
of their own.

### Documentation

Documentation for this toolkit is provided by Sphinx. As long as docstrings are defined
using [reST](https://en.wikipedia.org/wiki/ReStructuredText), Sphinx will generate API
documentation - including type annotations - directly from modules in this toolkit.

This documentation can be regenerated at any time using `make documentation`.

Please ensure to push code changes and documentation updates as separate commits to
enable reviewers to more easily identify relevant code changes during review.

### Dependencies

All dependencies must be pinned. To simplify this process, new dependencies should be
added to `requirements.txt` and `make requirements` run. This will generate new version
pins for all dependencies.

### Getting Started

To begin developing a new module in this toolkit the following steps should be followed:

1. Clone the repository to your workstation.
2. Create a new virtual environment for use during development.
```
python3 -m venv env
source env/bin/activate
```
3. Install required development dependencies.
```
pip install -e .[tests]
```

### Quick Start

The following sections provide examples of how to use Hutch for common use cases - such
as querying JupiterOne, or SumoLogic for information.

#### SumoLogic

An example of querying SumoLogic for all EC2 instances run in the last hour can be
found below:

```python
import getpass

from hutch.security import sumologic

# Setup the client / authentiate with Sumo.
sumo = sumologic.search.Client("<SUMO_CLIENT_ID>", getpass.getpass())
now = datetime.datetime.now(tz=datetime.timezone.utc)

# Perform the query against SumoLogic. This returns a job identifier, which must be used
# when querying for results.
query = sumo.query(
    f'_sourceCategory=aws/cloudtrail/o-* "RunInstances"',
    start=now - datetime.timedelta(hours=1),
    end=now,
)

# As this is a non-aggregated query, we use `sumo.messages` to get the raw messages. If
# this was an aggregation, we'd need to use `sumo.records` instead.
for messages in sumo.messages(query.id):
    for message in messages:
        # Print the user (`src_user` who executed the "RunInstances" operation. This
        # field is extracted using an FER in SumoLogic, which is automatically mapped
        # to the Python object by Hutch.
        print(message.src_user)

```
#### JupiterOne

An example of querying JupiterOne for a list of all resources with internet facing
sockets can be found below:

```python
import getpass

from hutch.security import jupiterone

# Use the Hutch provided "canned" queries for internet facing socket listeners.
queries = [
    jupiterone.queries.INTERNET_LISTENERS_GCP_COMPUTE,
    jupiterone.queries.INTERNET_LISTENERS_AWS_EC2,
    jupiterone.queries.INTERNET_LISTENERS_AZURE_VM,
    jupiterone.queries.INTERNET_LISTENERS_AWS_ALB,
    jupiterone.queries.INTERNET_LISTENERS_AWS_ELB,
    jupiterone.queries.INTERNET_LISTENERS_AWS_NLB,
    jupiterone.queries.INTERNET_LISTENERS_AZURE_LB,
]

# Setup the client / authenticate with JupiterOne
jone = jupiterone.query.Client("<JUPITERONE_ACCOUNT>", getpass.getpass())

# Perform queries for all resources, and store for processing.
for query in queries:
    search = jone.perform(query)

    # Page over results printing all known and extracted information about internet
    # facing socket listeners.
    for page in search:
        for resource in page.results:
            print(resource.properties)
```
