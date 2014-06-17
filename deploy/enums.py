from enum import Enum


class CommitStatus(Enum):
    New = 0
    Build = 1
    Deployed = 2
    Error = 3
    BuildError = 4
    Used = 5


class ProjectType(Enum):
    CSharp = 0
    PHP = 1
    Python = 2
    Puppet = 3


class CSharpProjectTypes(Enum):
    Console = 0
    WebApp = 1
    Test = 2