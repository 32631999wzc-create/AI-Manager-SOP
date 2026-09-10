"""Stable validation error representation."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True, order=True)
class ValidationError:
    path: str
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)
