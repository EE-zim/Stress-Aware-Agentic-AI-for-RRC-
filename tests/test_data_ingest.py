"""Tests for data_ingest module."""
from data_ingest import rrc_log_parser


def test_parse_csv_to_events(tmp_path):
    sample = tmp_path / "log.csv"
    sample.write_text("Time;Message name;Protocol\n")
    events = rrc_log_parser.parse_csv_to_events(str(sample))
    assert events == []
