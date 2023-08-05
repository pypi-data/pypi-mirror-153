# noqa: D100

from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class VesselType:
    """Type of vessel used for transport.

    Attributes:
        id: The vessel type ID.
        name: The vessel type name.
    """
    id: int
    name: str
