#!/usr/bin/env python3
"""
build.py - Full GSA020 pipeline starting from TX RRC source files.

Steps:
  1. Parse tx_rrc/gsa020.record.txt → clean COBOL copybook (never written to disk)
  2. Run cb2xml on the copybook → XML field layout (temp file, deleted after use)
  3. Decode gsf001l.ebc.gz record-by-record using the XML layout → CSV

Usage:
    python3 build.py [--ebcdic FILE] [--output PREFIX]

All intermediate files are temporary and cleaned up automatically.
"""

import argparse
import re
import tempfile
from pathlib import Path

from gsa020_to_csv import run_cb2xml, parse_copybook_xml, process_file

SCRIPT_DIR = Path(__file__).parent
RECORD_TXT = SCRIPT_DIR / "tx_rrc" / "gsa020.record.txt"

# These three fields are missing COMP-3 in gsa020.record.txt.
# gsa020.record.txt (the authoritative layout doc) shows them at packed-decimal
# storage sizes, confirming COMP-3 was intended.
_COMP3_FIXES = {
    "PER-WELL":   "PIC S9(7)   COMP-3.",
    "ACRG-FACT":  "PIC S9(8)V9(7) COMP-3.",
    "OTHER-FACT": "PIC S9(4)V9(7) COMP-3.",
}

# COBOL field names may not start with a digit. The record.txt uses "14B-DATE"
# etc. which must be prefixed.
_DIGIT_NAME_FIXES = {"14B-": "W14B-"}

# Matches a COBOL data item line: level-number, name, optional PIC clause.
# Used to identify and fix COMP-3 fields.
_ITEM_RE = re.compile(
    r'^(?P<level>\d+)\s+(?P<name>[\w-]+)(?P<rest>\s+PIC\s+.*)$', re.IGNORECASE
)


def record_txt_to_copybook(src: Path) -> str:
    """
    Read gsa020.record.txt and return a valid COBOL copybook string suitable
    for cb2xml.

    Transformations applied (in order):
    - Skips the file header — everything before the first 01-level item
    - Removes page-break markers ("II.1", bare "*" separator lines)
    - Strips trailing byte-position annotations ("PIC X. 42" → "PIC X.")
    - Strips the "POSITION" keyword from the 01-level line
    - Prefixes digit-starting field names with 'W' (COBOL syntax requirement)
    - Applies COMP-3 corrections for PER-WELL, ACRG-FACT, OTHER-FACT
    - Normalises all content to start at COBOL column 8 (7 leading spaces)
      so cb2xml can parse it as standard fixed-format COBOL
    """
    lines = src.read_text().splitlines()

    # Skip everything before the first 01-level item
    start = next(
        (i for i, ln in enumerate(lines) if re.match(r'\s*01\s', ln)),
        0,
    )

    result = []
    for raw in lines[start:]:
        s = raw.strip()

        # Skip blank lines and inter-section page markers
        if not s or re.match(r'^II\.\d+$', s) or s == '*':
            continue

        # Strip trailing position annotation: "PIC X. 42" → "PIC X."
        # The annotation is a bare integer at the end of a line after whitespace.
        s = re.sub(r'\s+\d+\s*$', '', s)

        # Strip "POSITION" keyword that appears only on the 01-level header line.
        s = re.sub(r'\s+POSITION\s*$', '', s, flags=re.IGNORECASE)

        # Fix digit-starting names (COBOL identifiers cannot begin with a digit)
        for old, new in _DIGIT_NAME_FIXES.items():
            s = s.replace(old, new)

        # Apply COMP-3 corrections. Match on the field name token (second word),
        # not the whole line, because the level number always comes first.
        m = _ITEM_RE.match(s)
        if m and m.group("name") in _COMP3_FIXES:
            s = f"{m.group('level')} {m.group('name')} {_COMP3_FIXES[m.group('name')]}"

        # Normalise to COBOL fixed format: everything starts at column 8
        # (7 leading spaces). cb2xml determines hierarchy from level numbers.
        result.append("       " + s)

    return "\n".join(result) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="GSA020 pipeline: tx_rrc/gsa020.record.txt → cb2xml → CSV"
    )
    parser.add_argument(
        "--record-txt",
        default=str(RECORD_TXT),
        help=f"TX RRC record layout file (default: {RECORD_TXT.relative_to(SCRIPT_DIR)})",
    )
    parser.add_argument(
        "--ebcdic",
        default=str(SCRIPT_DIR / "gsf001l.ebc.gz"),
        help="EBCDIC data file, plain or .gz (default: gsf001l.ebc.gz)",
    )
    parser.add_argument(
        "--output",
        default=str(SCRIPT_DIR / "gsa020"),
        help="Output CSV base path prefix (default: gsa020)",
    )
    args = parser.parse_args()

    record_txt = Path(args.record_txt)
    ebcdic = Path(args.ebcdic)
    out_prefix = Path(args.output)

    # ── Step 1: Generate copybook from record.txt ─────────────────────────────
    print("Step 1: Generating COBOL copybook from tx_rrc/gsa020.record.txt …")
    copybook_text = record_txt_to_copybook(record_txt)

    # Use a temp file for the copybook (cb2xml needs a path, not stdin)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".cbl", delete=False, dir=SCRIPT_DIR
    ) as tmp_cbl:
        tmp_cbl.write(copybook_text)
        tmp_cbl_path = Path(tmp_cbl.name)

    with tempfile.NamedTemporaryFile(
        suffix=".xml", delete=False, dir=SCRIPT_DIR
    ) as tmp_xml:
        tmp_xml_path = Path(tmp_xml.name)

    try:
        # ── Step 2: Run cb2xml ────────────────────────────────────────────────
        print("\nStep 2: Running cb2xml …")
        run_cb2xml(tmp_cbl_path, tmp_xml_path)

        # ── Step 3: Parse XML field layout ───────────────────────────────────
        print("\nStep 3: Parsing field layout from XML …")
        records_def = parse_copybook_xml(tmp_xml_path)

        # ── Steps 4-5: Decode EBCDIC → CSV ───────────────────────────────────
        print(f"\nSteps 4-5: Decoding {ebcdic.name} → CSV …")
        process_file(ebcdic, records_def, out_prefix)

    finally:
        tmp_cbl_path.unlink(missing_ok=True)
        tmp_xml_path.unlink(missing_ok=True)

    print("\nDone.")


if __name__ == "__main__":
    main()
