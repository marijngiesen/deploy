from enum import Enum


class CommitStatus(Enum):
    New = 0
    Build = 1
    Deployed = 2
    Error = 3
    BuildError = 4
    Used = 5

