# Get the version from the package's version, so the version can be defined in
# setup.py alone.
API_VERSION = (
    "1."
    "10."
    "7"
    ""
)  # type: str
"""The semantic version of this API."""

PROTOBUF_VERSION = 3  # type: int
"""The version of Protobuf this API can read and write from.
Attempts to load old Protobuf versions will raise a ``ValueError``.
"""
