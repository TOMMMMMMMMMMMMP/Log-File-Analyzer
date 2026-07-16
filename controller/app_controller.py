from model.log_parser import LogParser
from model.report import ReportGenerator
from utils.exporter import Exporter
from utils.visualizer import Visualizer


class AppController:
    """Bridges the GUI and the Model."""

    def __init__(self):
        self.parser = LogParser()
        self.exporter = Exporter()
        self.visualizer = Visualizer()
        self.current_file: str | None = None

    def load_file(self, filepath: str) -> tuple[bool, str]:
        """Load and parse a log file. Returns (success, message)."""
        try:
            self.parser.parse_file(filepath)
            self.current_file = filepath
            count = len(self.parser.entries)
            skipped = self.parser.skipped
            return True, f"Loaded {count} entries ({skipped} skipped)."
        except FileNotFoundError as e:
            return False, str(e)
        except PermissionError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {e}"

    def get_entries(self, level: str = "ALL", keyword: str = "") -> list:
        """Return filtered entries based on level and keyword."""
        entries = self.parser.entries

        if level != "ALL":
            entries = [e for e in entries if e.level == level]

        if keyword.strip():
            kw = keyword.strip().lower()
            entries = [e for e in entries if kw in e.message.lower()]

        return entries

    def get_report(self) -> str:
        """Return a formatted summary report."""
        report = ReportGenerator(self.parser.entries)
        return report.format_report()

    def get_counts(self) -> dict:
        """Return level counts."""
        return self.parser.count_by_level()

    def export_json(self, output_path: str) -> tuple[bool, str]:
        """Export entries to JSON. Returns (success, message)."""
        try:
            counts = self.parser.count_by_level()
            self.exporter.export_to_json(self.parser.entries, counts, output_path)
            return True, f"Exported to {output_path}"
        except Exception as e:
            return False, str(e)

    def show_chart(self) -> None:
        """Display the bar chart of log levels."""
        counts = self.parser.count_by_level()
        self.visualizer.bar_chart_by_level(counts)

    def show_timeline(self) -> None:
        """Display the timeline of log frequency."""
        self.visualizer.timeline_chart(self.parser.entries)

    def has_data(self) -> bool:
        return len(self.parser.entries) > 0
