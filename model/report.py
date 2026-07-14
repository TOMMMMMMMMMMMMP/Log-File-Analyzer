from collections import Counter
from datetime import datetime
from model.log_entry import LogEntry


class ReportGenerator:
    """Generates summary reports from parsed log entries."""

    def __init__(self, entries: list[LogEntry]):
        self.entries = entries

    def generate(self) -> dict:
        """
        Generate a full summary report.
        Returns a dict with total, first/last log, level counts, top errors.
        """
        if not self.entries:
            return {
                "total": 0,
                "first_log": None,
                "last_log": None,
                "counts": {"INFO": 0, "WARNING": 0, "ERROR": 0},
                "top_errors": [],
                "top_warnings": [],
            }

        sorted_entries = sorted(self.entries, key=lambda e: e.timestamp)

        errors = [e.message for e in self.entries if e.level == "ERROR"]
        warnings = [e.message for e in self.entries if e.level == "WARNING"]

        top_errors = Counter(errors).most_common(5)
        top_warnings = Counter(warnings).most_common(5)

        counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
        for e in self.entries:
            if e.level in counts:
                counts[e.level] += 1

        return {
            "total": len(self.entries),
            "first_log": sorted_entries[0].timestamp.isoformat(),
            "last_log": sorted_entries[-1].timestamp.isoformat(),
            "counts": counts,
            "top_errors": [{"message": msg, "count": n} for msg, n in top_errors],
            "top_warnings": [{"message": msg, "count": n} for msg, n in top_warnings],
        }

    def format_report(self) -> str:
        """Return a human-readable string version of the report."""
        r = self.generate()

        lines = [
            "=" * 50,
            "       LOG FILE ANALYSIS REPORT",
            "=" * 50,
            f"Total entries   : {r['total']}",
            f"First log       : {r['first_log']}",
            f"Last log        : {r['last_log']}",
            "",
            "--- Level Counts ---",
            f"  INFO    : {r['counts']['INFO']}",
            f"  WARNING : {r['counts']['WARNING']}",
            f"  ERROR   : {r['counts']['ERROR']}",
        ]

        if r["top_errors"]:
            lines.append("")
            lines.append("--- Top Errors ---")
            for item in r["top_errors"]:
                lines.append(f"  [{item['count']}x] {item['message']}")

        if r["top_warnings"]:
            lines.append("")
            lines.append("--- Top Warnings ---")
            for item in r["top_warnings"]:
                lines.append(f"  [{item['count']}x] {item['message']}")

        lines.append("=" * 50)
        return "\n".join(lines)
