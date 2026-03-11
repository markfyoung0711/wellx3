#!/usr/bin/env python3
"""
rrc_download.py — Download RRC EBCDIC files via Selenium, driven by rrc_sources.yaml.

Usage:
    python3 rrc_download.py [--config rrc_sources.yaml] [--source gas_ledger] [--all]

Output:
    $WAREHOUSE/rrc/<YYYYMMDD>/<filename>
"""

import argparse
import os
import re
import sys
import time
import yaml
import zipfile
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DEFAULT_CONFIG = Path(__file__).parent / "rrc_sources.yaml"
DOWNLOAD_WAIT_SECS = 120  # max seconds to wait for file to appear


def load_config(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)


def make_download_dir():
    warehouse = os.environ.get("WAREHOUSE")
    if not warehouse:
        raise EnvironmentError("WAREHOUSE environment variable is not set")
    datestamp = datetime.now().strftime("%Y%m%d")
    download_dir = Path(warehouse) / "rrc" / datestamp
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir


def make_driver(download_dir: Path):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("prefs", {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    })
    driver = webdriver.Chrome(options=options)
    # Enable downloads in headless mode via CDP
    driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": str(download_dir),
    })
    return driver


def find_link(driver, row_text_pattern, link_text):
    """
    Find an <a> whose visible link text matches link_text, within a row whose
    full text matches row_text_pattern (regex).
    """
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    rows = driver.find_elements(By.XPATH, "//tr")
    pattern = re.compile(row_text_pattern, re.IGNORECASE)
    for row in rows:
        row_text = row.text
        if pattern.search(row_text):
            links = row.find_elements(By.LINK_TEXT, link_text)
            if links:
                return links[0]
    raise RuntimeError(
        f"Could not find link '{link_text}' in any row matching '{row_text_pattern}'"
    )


def wait_for_zip(download_dir: Path, timeout: int = DOWNLOAD_WAIT_SECS) -> Path:
    """Wait for GoDrive's documents_*.zip to finish downloading."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        all_files = list(download_dir.iterdir())
        zips = [f for f in all_files if f.suffix == ".zip" and not f.name.endswith(".crdownload")]
        in_progress = [f for f in all_files if f.name.endswith(".crdownload")]
        if in_progress:
            print(f"  [download] In progress: {[f.name for f in in_progress]}")
        if zips:
            return zips[0]
        time.sleep(2)
    raise TimeoutError(f"No zip file downloaded within {timeout}s in {download_dir}")


def extract_zip(zip_path: Path, file_pattern: str) -> list[Path]:
    """Extract files matching file_pattern from zip into the same directory."""
    pat = re.compile(file_pattern)
    dest = zip_path.parent
    extracted = []
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.namelist():
            name = Path(member).name
            if pat.match(name):
                zf.extract(member, dest)
                extracted.append(dest / member)
    zip_path.unlink()
    return extracted


def _handle_goanywhere(driver, source_name, file_pattern):
    """Interact with the GoAnywhere GoDrive web UI to trigger the file download.

    Flow:
      1. Wait for file table to load
      2. Find the row whose filename matches file_pattern
      3. Select it via the row image (selectRow JS call)
      4. Click the Download button via JS (bypasses any overlay)
    """
    wait = WebDriverWait(driver, 30)

    # Wait for file table rows to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fileTable_data tr")))

    # Find all rows matching file_pattern and select them
    pat = re.compile(file_pattern)
    rows = driver.find_elements(By.CSS_SELECTOR, "#fileTable_data tr")
    matched = []
    for row in rows:
        links = row.find_elements(By.CSS_SELECTOR, "td.NameColumn a")
        if links and pat.match(links[0].text.strip()):
            matched.append((links[0].text.strip(), row))

    if not matched:
        raise RuntimeError(
            f"No files matching '{file_pattern}' found in GoDrive file table"
        )

    # Select all matching files
    for filename, row in matched:
        print(f"[{source_name}] Selecting: {filename}")
        chkbox = row.find_element(By.CSS_SELECTOR, "td.rowCheckbox .ui-chkbox-box")
        driver.execute_script("arguments[0].click();", chkbox)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return PrimeFaces.ajax.Queue.isEmpty();")
        )

    # Wait for overlay, then click Download once
    WebDriverWait(driver, 15).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ui-dialog[aria-hidden='false']"))
    )
    download_btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Download')]]")
    print(f"[{source_name}] Clicking Download ({len(matched)} file(s)) ...")
    download_btn.click()
    time.sleep(3)

    return len(matched)


def download_source(source_name, source_cfg, download_dir):
    dl = source_cfg["download"]
    source_url = dl["source_url"]
    file_pattern = dl["file_selector"]["pattern"]
    record_modified_date = dl["file_selector"].get("record_modified_date", False)

    print(f"[{source_name}] Opening {source_url}")
    driver = make_driver(download_dir)
    try:
        driver.get(source_url)

        for step in dl["navigate"]:
            if step["action"] == "click_link":
                link = find_link(driver, step["row_text"], step["link_text"])
                print(f"[{source_name}] Clicking '{step['link_text']}' ...")
                link.click()
                time.sleep(3)
                print(f"[{source_name}] Current URL: {driver.current_url}")
                print(f"[{source_name}] Page title: {driver.title}")
                print(f"[{source_name}] Window handles: {driver.window_handles}")
            else:
                raise ValueError(f"Unknown navigate action: {step['action']}")

        # Switch to any new tab that opened
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            print(f"[{source_name}] Switched to new tab: {driver.current_url}")

        # Handle GoAnywhere GoDrive intermediate page
        if "mft.rrc.texas.gov" in driver.current_url:
            _handle_goanywhere(driver, source_name, file_pattern)

        # GoDrive always delivers a zip — wait for it, then extract
        print(f"[{source_name}] Waiting for zip download ...")
        zip_path = wait_for_zip(download_dir)
        print(f"[{source_name}] Extracting: {zip_path.name}")
        downloaded = extract_zip(zip_path, file_pattern)

        for f in downloaded:
            print(f"[{source_name}] Extracted: {f.name}")
            if record_modified_date:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                print(f"[{source_name}] File modification time: {mtime:%Y-%m-%d %H:%M:%S}")

        return downloaded

    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Download RRC EBCDIC files via Selenium")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Path to rrc_sources.yaml")
    parser.add_argument("--source", help="Source key to download (e.g. gas_ledger)")
    parser.add_argument("--all", action="store_true", help="Download all sources in config")
    args = parser.parse_args()

    if not args.source and not args.all:
        parser.error("Specify --source <name> or --all")

    config = load_config(args.config)
    rrc_files = config["rrc_files"]
    download_dir = make_download_dir()
    print(f"Download directory: {download_dir}")

    sources = rrc_files.keys() if args.all else [args.source]
    for name in sources:
        if name not in rrc_files:
            print(f"ERROR: '{name}' not found in config", file=sys.stderr)
            sys.exit(1)
        download_source(name, rrc_files[name], download_dir)


if __name__ == "__main__":
    main()
