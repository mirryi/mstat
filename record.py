from __future__ import annotations

import enum
import re
from datetime import datetime as DateTime
from typing import Dict
from typing import List

from exception import ParseException


class RecordStatus(enum.Enum):
    JOINED = 1
    LEFT = 2

    @classmethod
    def from_str(cls, s: str) -> RecordStatus:
        if s == 'Joined':
            return cls.JOINED
        elif s == 'Left':
            return cls.LEFT
        else:
            raise ParseException()


class Record:
    def __init__(self, name: str, status: RecordStatus, timestamp: DateTime):
        self.name = name
        self.status = status
        self.timestamp = timestamp

    def __repr__(self):
        fmt = 'Record(name = \'{name}\', status = {status}, ' \
            'timestamp = \'{timestamp}\')'
        return fmt.format(name=self.name,
                          status=self.status,
                          timestamp=self.timestamp)

    @classmethod
    def from_row(cls, row: List[str]) -> Record:
        timestamp_split = re.split(' |, ', row[2])

        date_split = timestamp_split[0].split('/')
        month = int(date_split[0])
        day = int(date_split[1])
        year = int(date_split[2])

        time_split = timestamp_split[1].split(':')
        minute = int(time_split[1])
        second = int(time_split[2])
        hour = int(time_split[0])
        if timestamp_split[2] == 'PM':
            hour += 12

        timestamp = DateTime(year, month, day, hour, minute, second)
        status = RecordStatus.from_str(row[1])
        return cls(row[0], status, timestamp)


class UserRecord:
    def __init__(self, status: RecordStatus, timestamp: DateTime):
        self.status = status
        self.timestamp = timestamp

    def __repr__(self):
        fmt = 'UserRecord(status = {status}, timestamp = \'{timestamp}\')'
        return fmt.format(status=self.status,
                          timestamp=self.timestamp)

    @classmethod
    def from_record(cls, record: Record) -> UserRecord:
        return cls(record.status, record.timestamp)


class User:
    def __init__(self, name: str, records: List[UserRecord]):
        self.name = name
        self.records = records

    def __repr__(self):
        fmt = 'User(name = \'{name}\', records={records})'
        return fmt.format(name=self.name, records=self.records)

    @classmethod
    def from_record_list(cls, records: List[Record]) -> User:
        return cls(records[0].name,
                   [UserRecord.from_record(r) for r in records])

    @classmethod
    def from_mixed_record_list(cls, records: List[Record], name: str) -> User:
        return cls.from_record_list([r for r in records if r.name == name])

    @classmethod
    def from_multiple_record_list(cls, records: List[Record]) -> List[User]:
        m: Dict[str, User] = dict()
        for r in records:
            fnd = m.get(r.name)
            if fnd is None:
                m[r.name] = User(r.name, [UserRecord.from_record(r)])
            else:
                fnd.records.append(UserRecord.from_record(r))
        return list(m.values())
