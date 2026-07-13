import json
import os
from model.log_entry import LogEntry


class Exporter:
    """Handles exporting parsed log data to JSON."""

    def export_to_json(self, entries: list[LogEntry], counts: dict, output_path: str) -> str:
        """
        Export log entries and level counts to a JSON file.
        Returns the output path on success.
        """
        data = {
            "summary": {
                "total": len(entries),
                "counts": counts,
            },
            "entries": [e.to_dict() for e in entries],
        }

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return output_path
