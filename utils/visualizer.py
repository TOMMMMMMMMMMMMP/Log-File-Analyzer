import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from model.log_entry import LogEntry


class Visualizer:
    """Generates matplotlib charts from log entries."""

    LEVEL_COLORS = {
        "INFO": "#4CAF50",
        "WARNING": "#FF9800",
        "ERROR": "#F44336",
    }

    def bar_chart_by_level(self, counts: dict[str, int], title: str = "Log Entries by Level") -> None:
        """Display a bar chart showing count per log level."""
        levels = list(counts.keys())
        values = list(counts.values())
        colors = [self.LEVEL_COLORS.get(l, "#999") for l in levels]

        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(levels, values, color=colors, edgecolor="white", width=0.5)

        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                str(val),
                ha="center", va="bottom", fontweight="bold", fontsize=12
            )

        ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Log Level")
        ax.set_ylabel("Count")
        ax.set_ylim(0, max(values) * 1.2 if values else 1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.show()

    def timeline_chart(self, entries: list[LogEntry], title: str = "Log Frequency by Hour") -> None:
        """Display a timeline showing log frequency per hour."""
        if not entries:
            print("No entries to display.")
            return

        hour_counts: dict[str, Counter] = {}
        for entry in entries:
            hour = entry.timestamp.strftime("%H:00")
            if hour not in hour_counts:
                hour_counts[hour] = Counter()
            hour_counts[hour][entry.level] += 1

        hours = sorted(hour_counts.keys())
        info_vals    = [hour_counts[h].get("INFO", 0)    for h in hours]
        warning_vals = [hour_counts[h].get("WARNING", 0) for h in hours]
        error_vals   = [hour_counts[h].get("ERROR", 0)   for h in hours]

        x = range(len(hours))
        width = 0.25

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([i - width for i in x], info_vals,    width, label="INFO",    color=self.LEVEL_COLORS["INFO"])
        ax.bar([i         for i in x], warning_vals, width, label="WARNING", color=self.LEVEL_COLORS["WARNING"])
        ax.bar([i + width for i in x], error_vals,   width, label="ERROR",   color=self.LEVEL_COLORS["ERROR"])

        ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Count")
        ax.set_xticks(list(x))
        ax.set_xticklabels(hours, rotation=45)
        ax.legend()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.show()

    def save_bar_chart(self, counts: dict[str, int], output_path: str) -> None:
        """Save the bar chart to a file instead of displaying it."""
        levels = list(counts.keys())
        values = list(counts.values())
        colors = [self.LEVEL_COLORS.get(l, "#999") for l in levels]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(levels, values, color=colors, edgecolor="white", width=0.5)
        ax.set_title("Log Entries by Level", fontsize=14, fontweight="bold")
        ax.set_xlabel("Log Level")
        ax.set_ylabel("Count")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        print(f"Chart saved to {output_path}")
