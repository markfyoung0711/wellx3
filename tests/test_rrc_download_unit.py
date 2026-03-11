"""
Unit tests for rrc_download.py pure functions (no Selenium required).

Covers:
  - load_config
  - make_download_dir
  - wait_for_zip
  - extract_zip
"""

import textwrap
import threading
import time
import zipfile
from datetime import datetime
from pathlib import Path

import pytest

from rrc.rrc_download import extract_zip, load_config, make_download_dir, wait_for_zip


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------

def test_load_config_returns_dict(tmp_path):
    cfg = tmp_path / "sources.yaml"
    cfg.write_text(textwrap.dedent("""\
        rrc_files:
          gas_ledger:
            description: "Test"
    """))
    result = load_config(cfg)
    assert result == {"rrc_files": {"gas_ledger": {"description": "Test"}}}


def test_load_config_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nonexistent.yaml")


def test_load_config_real_config():
    config_path = Path(__file__).parent.parent / "rrc" / "rrc_sources.yaml"
    config = load_config(config_path)
    assert "rrc_files" in config
    assert "gas_ledger" in config["rrc_files"]
    dl = config["rrc_files"]["gas_ledger"]["download"]
    assert dl["source_url"].startswith("https://")
    assert dl["file_selector"]["pattern"]


# ---------------------------------------------------------------------------
# make_download_dir
# ---------------------------------------------------------------------------

def test_make_download_dir_creates_path(tmp_path, monkeypatch):
    monkeypatch.setenv("WAREHOUSE", str(tmp_path))
    result = make_download_dir()
    assert result.exists()
    assert result.is_dir()


def test_make_download_dir_structure(tmp_path, monkeypatch):
    monkeypatch.setenv("WAREHOUSE", str(tmp_path))
    result = make_download_dir()
    parts = result.parts
    rrc_idx = parts.index("rrc")
    datestamp = parts[rrc_idx + 1]
    assert datestamp == datetime.now().strftime("%Y%m%d")


def test_make_download_dir_no_warehouse(monkeypatch):
    monkeypatch.delenv("WAREHOUSE", raising=False)
    with pytest.raises(EnvironmentError, match="WAREHOUSE"):
        make_download_dir()


def test_make_download_dir_idempotent(tmp_path, monkeypatch):
    monkeypatch.setenv("WAREHOUSE", str(tmp_path))
    d1 = make_download_dir()
    d2 = make_download_dir()
    assert d1 == d2


# ---------------------------------------------------------------------------
# wait_for_zip
# ---------------------------------------------------------------------------

def test_wait_for_zip_finds_existing_zip(tmp_path):
    (tmp_path / "documents_20260311.zip").touch()
    result = wait_for_zip(tmp_path, timeout=5)
    assert result.suffix == ".zip"
    assert result.name == "documents_20260311.zip"


def test_wait_for_zip_ignores_crdownload(tmp_path):
    (tmp_path / "documents_20260311.zip.crdownload").touch()
    with pytest.raises(TimeoutError):
        wait_for_zip(tmp_path, timeout=2)


def test_wait_for_zip_waits_for_completion(tmp_path):
    zip_path = tmp_path / "documents_20260311.zip"
    crdownload = tmp_path / "documents_20260311.zip.crdownload"

    def complete_download():
        time.sleep(1)
        crdownload.unlink()
        zip_path.touch()

    crdownload.touch()
    t = threading.Thread(target=complete_download)
    t.start()
    result = wait_for_zip(tmp_path, timeout=10)
    t.join()
    assert result == zip_path


def test_wait_for_zip_timeout(tmp_path):
    with pytest.raises(TimeoutError, match="No zip file"):
        wait_for_zip(tmp_path, timeout=2)


# ---------------------------------------------------------------------------
# extract_zip
# ---------------------------------------------------------------------------

def _make_zip(zip_path: Path, members: dict[str, bytes]) -> Path:
    """Helper: create a zip with given {name: content} members."""
    with zipfile.ZipFile(zip_path, "w") as zf:
        for name, content in members.items():
            zf.writestr(name, content)
    return zip_path


def test_extract_zip_extracts_matching(tmp_path):
    zip_path = _make_zip(tmp_path / "docs.zip", {
        "gsf001l.ebc.gz": b"data1",
        "gsf002l.ebc.gz": b"data2",
        "readme.txt": b"ignore me",
    })
    extracted = extract_zip(zip_path, r"gsf\d+l\.ebc\.gz")
    names = {f.name for f in extracted}
    assert names == {"gsf001l.ebc.gz", "gsf002l.ebc.gz"}


def test_extract_zip_ignores_non_matching(tmp_path):
    zip_path = _make_zip(tmp_path / "docs.zip", {
        "gsf001l.ebc.gz": b"data",
        "readme.txt": b"ignore",
    })
    extracted = extract_zip(zip_path, r"gsf\d+l\.ebc\.gz")
    assert not any(f.name == "readme.txt" for f in extracted)


def test_extract_zip_deletes_zip(tmp_path):
    zip_path = _make_zip(tmp_path / "docs.zip", {"gsf001l.ebc.gz": b"data"})
    extract_zip(zip_path, r".*\.ebc\.gz")
    assert not zip_path.exists()


def test_extract_zip_file_contents(tmp_path):
    zip_path = _make_zip(tmp_path / "docs.zip", {"gsf001l.ebc.gz": b"hello"})
    extracted = extract_zip(zip_path, r".*\.ebc\.gz")
    assert extracted[0].read_bytes() == b"hello"


def test_extract_zip_no_matches_returns_empty(tmp_path):
    zip_path = _make_zip(tmp_path / "docs.zip", {"readme.txt": b"nothing"})
    extracted = extract_zip(zip_path, r".*\.ebc\.gz")
    assert extracted == []
    assert not zip_path.exists()
