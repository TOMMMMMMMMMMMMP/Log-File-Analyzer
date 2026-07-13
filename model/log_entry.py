from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    """Represents a single parsed log line."""
    timestamp: datetime
    level: str      # INFO | WARNING | ERROR
    message: str
    raw: str        # original unparsed line

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
        }
