import argparse
import sys
from model.log_parser import LogParser
from model.report import ReportGenerator
from utils.exporter import Exporter
from utils.visualizer import Visualizer


def main():
    parser = argparse.ArgumentParser(
        description="Log File Analyzer — parse and analyze .log files"
    )
    parser.add_argument("--file",    "-f", required=True,  help="Path to the .log file")
    parser.add_argument("--level",   "-l", default=None,   help="Filter by level: INFO, WARNING, ERROR")
    parser.add_argument("--filter",  "-k", default=None,   help="Filter by keyword in message")
    parser.add_argument("--report",  "-r", action="store_true", help="Print summary report")
    parser.add_argument("--export",  "-e", default=None,   help="Export results to JSON (provide output path)")
    parser.add_argument("--chart",   "-c", action="store_true", help="Show bar chart by level")
    parser.add_argument("--timeline","-t", action="store_true", help="Show timeline chart by hour")

    args = parser.parse_args()

    # Parse the file
    log_parser = LogParser()
    try:
        entries = log_parser.parse_file(args.file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\nParsed {len(entries)} entries, skipped {log_parser.skipped} malformed lines.")

    # Apply filters
    if args.level:
        entries = log_parser.filter_by_level(args.level)
        print(f"Filtered by level '{args.level}': {len(entries)} entries.")

    if args.filter:
        entries = log_parser.filter_by_keyword(args.filter)
        print(f"Filtered by keyword '{args.filter}': {len(entries)} entries.")

    # Print entries
    print()
    for e in entries:
        print(f"[{e.timestamp}] {e.level:<8} {e.message}")

    # Report
    if args.report:
        report = ReportGenerator(entries)
        print("\n" + report.format_report())

    # Export
    if args.export:
        counts = log_parser.count_by_level()
        exp = Exporter()
        path = exp.export_to_json(entries, counts, args.export)
        print(f"\nExported to {path}")

    # Charts
    viz = Visualizer()
    if args.chart:
        counts = log_parser.count_by_level()
        viz.bar_chart_by_level(counts)

    if args.timeline:
        viz.timeline_chart(entries)


if __name__ == "__main__":
    main()
