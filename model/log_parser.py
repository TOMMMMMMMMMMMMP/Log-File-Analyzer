import re
from datetime import datetime
from model.log_entry import LogEntry

# Matches: 2024-01-15 08:00:01 INFO Some message here
LOG_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(INFO|WARNING|ERROR)\s+(.+)$"
)

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class LogParser:
    """Parses .log files and provides filtering and counting methods."""

    def __init__(self):
        self.entries: list[LogEntry] = []
        self.skipped: int = 0

    def parse_file(self, filepath: str) -> list[LogEntry]:
        """
        Parse a .log file and return a list of LogEntry objects.
        Malformed lines are skipped and counted in self.skipped.
        """
        self.entries = []
        self.skipped = 0

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    entry = self._parse_line(line)
                    if entry:
                        self.entries.append(entry)
                    else:
                        self.skipped += 1
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file not found: {filepath}")
        except PermissionError:
            raise PermissionError(f"Cannot read file: {filepath}")

        return self.entries

    def _parse_line(self, line: str) -> LogEntry | None:
        """Parse a single log line. Returns None if malformed."""
        match = LOG_PATTERN.match(line)
        if not match:
            return None
        try:
            timestamp = datetime.strptime(match.group(1), TIMESTAMP_FORMAT)
            level = match.group(2)
            message = match.group(3)
            return LogEntry(timestamp=timestamp, level=level, message=message, raw=line)
        except ValueError:
            return None

    def count_by_level(self) -> dict[str, int]:
        """Return a count of entries per log level."""
        counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
        for entry in self.entries:
            if entry.level in counts:
                counts[entry.level] += 1
        return counts

    def filter_by_level(self, level: str) -> list[LogEntry]:
        """Return only entries matching the given level (case-insensitive)."""
        level = level.upper()
        return [e for e in self.entries if e.level == level]

    def filter_by_keyword(self, keyword: str) -> list[LogEntry]:
        """Return entries whose message contains the keyword (case-insensitive)."""
        keyword = keyword.lower()
        return [e for e in self.entries if keyword in e.message.lower()]

    def filter_by_date(self, start: datetime, end: datetime) -> list[LogEntry]:
        """Return entries between start and end timestamps (inclusive)."""
        return [e for e in self.entries if start <= e.timestamp <= end]
