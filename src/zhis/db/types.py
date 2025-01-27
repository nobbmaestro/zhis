from dataclasses import dataclass, field
from typing import List, NewType

from marshmallow import EXCLUDE

RegexPatternType = NewType("RegexPatternType", str)


@dataclass
class DbConfig:
    exclude_commands: List[RegexPatternType] = field(default_factory=list)

    class Meta:
        unknown = EXCLUDE
