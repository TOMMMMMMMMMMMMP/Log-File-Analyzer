import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from model.log_parser import LogParser
from model.report import ReportGenerator


SAMPLE_FILE = "samples/sample.log"


def test_parse():
    parser = LogParser()
    entries = parser.parse_file(SAMPLE_FILE)
    assert len(entries) == 20, f"Expected 20 entries, got {len(entries)}"
    assert parser.skipped == 0
    print("test_parse ✔")


def test_count_by_level():
    parser = LogParser()
    parser.parse_file(SAMPLE_FILE)
    counts = parser.count_by_level()
    assert counts["INFO"] == 10
    assert counts["WARNING"] == 4
    assert counts["ERROR"] == 6
    print("test_count_by_level ✔")


def test_filter_by_level():
    parser = LogParser()
    parser.parse_file(SAMPLE_FILE)
    errors = parser.filter_by_level("ERROR")
    assert len(errors) == 6
    assert all(e.level == "ERROR" for e in errors)
    print("test_filter_by_level ✔")


def test_filter_by_keyword():
    parser = LogParser()
    parser.parse_file(SAMPLE_FILE)
    results = parser.filter_by_keyword("connection")
    assert len(results) > 0
    assert all("connection" in e.message.lower() for e in results)
    print("test_filter_by_keyword ✔")


def test_filter_by_date():
    parser = LogParser()
    parser.parse_file(SAMPLE_FILE)
    start = datetime(2024, 1, 15, 8, 0, 0)
    end = datetime(2024, 1, 15, 8, 5, 0)
    results = parser.filter_by_date(start, end)
    assert len(results) > 0
    assert all(start <= e.timestamp <= end for e in results)
    print("test_filter_by_date ✔")


def test_report():
    parser = LogParser()
    entries = parser.parse_file(SAMPLE_FILE)
    report = ReportGenerator(entries)
    r = report.generate()
    assert r["total"] == 20
    assert r["first_log"] is not None
    assert r["last_log"] is not None
    assert r["counts"]["ERROR"] == 6
    print("test_report ✔")


def test_malformed_lines():
    parser = LogParser()
    # Write a temp file with malformed lines
    with open("samples/malformed.log", "w") as f:
        f.write("2024-01-15 08:00:01 INFO Valid line\n")
        f.write("this is not a valid log line\n")
        f.write("2024-01-15 08:01:00 ERROR Another valid line\n")
        f.write("GARBAGE DATA @@##\n")
    entries = parser.parse_file("samples/malformed.log")
    assert len(entries) == 2
    assert parser.skipped == 2
    os.remove("samples/malformed.log")
    print("test_malformed_lines ✔")


if __name__ == "__main__":
    test_parse()
    test_count_by_level()
    test_filter_by_level()
    test_filter_by_keyword()
    test_filter_by_date()
    test_report()
    test_malformed_lines()
    print("\nAll tests passed ✔")
