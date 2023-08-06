from dataclasses import dataclass
from typing import Dict, List, Tuple

from .constants import LINE_TYPE_MAP, LineType


@dataclass
class UID:
    """
    Represents a CoolMasterNet strict UID.
    """

    line_number: int
    indoor_number_x: int
    indoor_number_yy: int

    @classmethod
    def from_string(cls, s: str):
        if not s.startswith("L"):
            raise ValueError('UIDs should always start with "L"')

        line, unit = s.split(".")

        return cls(line_number=int(line[1]), indoor_number_x=int(unit[0]), indoor_number_yy=int(unit[1:3]))

    def __str__(self):
        return f"L{self.line_number}.{self.indoor_number_x}{self.indoor_number_yy:02d}"

    def __hash__(self):
        return str(self).__hash__()


@dataclass
class Line:
    """
    Represents a CoolMasterNet HVAC data line.
    """

    number: int
    type: LineType
    properties: List[str]
    link_stats: Dict[str, Tuple[int, int]]

    @classmethod
    def from_heading_meta(cls, heading: str, meta: str):
        number, _type, props = cls.parse_line_heading(heading.strip())
        stats = cls.parse_line_meta(meta.strip())

        return cls(number=number, type=_type, properties=props, link_stats=stats)

    @staticmethod
    def parse_line_heading(heading: str) -> Tuple[int, LineType, List[str]]:
        # L3: CLMB Modbus Address:0x50(80) 9600_8N1
        line_number = int(heading[1])

        props = heading[3:].split()
        line_type = props[0].strip()

        return line_number, LINE_TYPE_MAP[line_type], props[1:]

    @staticmethod
    def parse_line_meta(line: str) -> Dict[str, Tuple[int, int]]:
        # Tx:7679/9204 Rx:0/0 TO:0/0 CS:0/0 Col:0/0 NAK:0/0
        results = {}

        for grouping in line.split():
            key, counts = grouping.split(":")
            count_now, count_total = counts.split("/")

            results[key.strip()] = (int(count_now), int(count_total))

        return results
