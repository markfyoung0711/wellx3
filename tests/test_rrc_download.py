"""
End-to-end test: download the RRC gas ledger EBCDIC file from the live RRC website.

Requires:
- Network access to rrc.texas.gov and mft.rrc.texas.gov
- Chrome + chromedriver available
- $WAREHOUSE set, or a temp directory is used

Run:
    pytest tests/test_rrc_download.py -v -s
"""

import re
from pathlib import Path

import pytest

from rrc.rrc_download import load_config, download_source, make_download_dir

CONFIG_PATH = Path(__file__).parent.parent / "rrc" / "rrc_sources.yaml"


@pytest.fixture()
def warehouse(tmp_path, monkeypatch):
    """Use a temp directory as WAREHOUSE for the test."""
    monkeypatch.setenv("WAREHOUSE", str(tmp_path))
    return tmp_path


def test_gas_ledger_download(warehouse):
    config = load_config(CONFIG_PATH)
    source_cfg = config["rrc_files"]["gas_ledger"]
    file_pattern = source_cfg["download"]["file_selector"]["pattern"]

    download_dir = make_download_dir()
    downloaded_files = download_source("gas_ledger", source_cfg, download_dir)

    assert len(downloaded_files) > 0, "No files were downloaded"

    for downloaded in downloaded_files:
        # File exists and is non-empty
        assert downloaded.exists(), f"Downloaded file not found: {downloaded}"
        assert downloaded.stat().st_size > 0, f"Downloaded file is empty: {downloaded}"

        # Filename matches expected pattern
        assert re.match(file_pattern, downloaded.name), (
            f"Filename '{downloaded.name}' does not match pattern '{file_pattern}'"
        )

        # Landed in the right place: <warehouse>/rrc/<YYYYMMDD>/
        parts = downloaded.parts
        rrc_idx = parts.index("rrc")
        datestamp = parts[rrc_idx + 1]
        assert re.match(r"\d{8}$", datestamp), f"Expected YYYYMMDD dir, got '{datestamp}'"

        print(f"\nDownloaded: {downloaded} ({downloaded.stat().st_size:,} bytes)")
