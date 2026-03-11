#!/usr/bin/env python3
"""
gsa020_to_csv.py - Convert GSA020 EBCDIC file to CSV

Steps:
  1. Pre-process COBOL copybook (strip FD header, fix missing COMP-3 specs)
  2. Run cb2xml to generate XML field layout
  3. Parse XML to build field definitions (positions, types, scales)
  4. Read EBCDIC gz file record by record (fixed-length 2120 bytes)
  5. Decode each field (EBCDIC text, zoned decimal, or COMP-3 packed decimal)
  6. Write separate CSVs for FLD-REC (field/gas field records) and WELL-REC (well records)

Usage:
    python3 gsa020_to_csv.py [--copybook FILE] [--ebcdic FILE] [--output PREFIX]
"""

import argparse
import csv
import gzip
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RECORD_LENGTH = 2120
EBCDIC_ENCODING = "cp037"

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Pre-process copybook
# ─────────────────────────────────────────────────────────────────────────────

# These fields inside FLD-MONTH OCCURS 14 TIMES are incorrectly missing COMP-3
# in the available copybook.  gsa020.record.txt (the authoritative layout) shows
# them at packed-decimal storage sizes, confirming COMP-3 was intended.
COMP3_FIXES = {
    "PER-WELL":   "PIC S9(7)   COMP-3.",   # 4 bytes packed  (was 7 bytes display)
    "ACRG-FACT":  "PIC S9(8)V9(7) COMP-3.", # 8 bytes packed  (same storage but different picture/scale)
    "OTHER-FACT": "PIC S9(4)V9(7) COMP-3.", # 6 bytes packed  (was 4 bytes display)
}


def preprocess_copybook(src: Path) -> str:
    """
    Return a cleaned copybook string suitable for cb2xml:
      - Strips everything before the first 01-level item (removes FD block)
      - Applies COMP-3 corrections listed in COMP3_FIXES
    """
    text = src.read_text()
    lines = text.splitlines(keepends=True)

    # Find first line that starts a 01-level data record
    start = 0
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("01 ") or stripped.startswith("01  "):
            start = i
            break

    kept = lines[start:]

    # Apply COMP-3 fixes: match on the field-name token (second word on the line),
    # because the level number always comes first ("05  PER-WELL  PIC ...").
    _item_re = re.compile(
        r'^(?P<indent>\s*)(?P<level>\d+)\s+(?P<name>[\w-]+)(?P<rest>\s+PIC\s+.*)$',
        re.IGNORECASE,
    )
    result = []
    for line in kept:
        m = _item_re.match(line.rstrip('\n'))
        if m and m.group("name") in COMP3_FIXES:
            line = (
                f"{m.group('indent')}{m.group('level')}  {m.group('name')}"
                f"    {COMP3_FIXES[m.group('name')]}\n"
            )
        result.append(line)

    return "".join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Run cb2xml
# ─────────────────────────────────────────────────────────────────────────────

def run_cb2xml(copybook_path: Path, output_xml: Path):
    """Invoke cb2xml to convert the (pre-processed) copybook to XML."""
    jar = SCRIPT_DIR / "cb2xml" / "lib" / "cb2xml.jar"
    if not jar.exists():
        raise FileNotFoundError(f"cb2xml.jar not found: {jar}")
    cmd = [
        "java", "-jar", str(jar),
        "-cobol", str(copybook_path),
        "-xml", str(output_xml),
        "-indentXml", "true",
        "-XmlFormat", "2017",
        "-Dialect", "Mainframe",
    ]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not output_xml.exists():
        raise RuntimeError(f"cb2xml failed (rc={result.returncode}):\n{result.stderr}")
    print(f"  Generated: {output_xml}")


# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Parse XML → FieldDef list
# ─────────────────────────────────────────────────────────────────────────────

class FieldDef:
    """Describes one leaf field's layout and encoding."""

    __slots__ = ["name", "position", "storage_length", "is_comp3", "is_numeric",
                 "scale", "picture", "signed"]

    def __init__(self, name, position, storage_length, is_comp3, is_numeric, scale, picture):
        self.name = name
        self.position = position          # 0-based byte offset in the raw record
        self.storage_length = storage_length
        self.is_comp3 = is_comp3
        self.is_numeric = is_numeric
        self.scale = scale
        self.picture = picture or ""
        self.signed = self.picture.startswith("S")

    # ── decoding ──────────────────────────────────────────────────────────────

    def decode(self, record: bytes) -> str:
        data = record[self.position: self.position + self.storage_length]
        if len(data) < self.storage_length:
            return ""
        if self.is_comp3:
            return _decode_comp3(data, self.scale)
        elif self.is_numeric:
            return _decode_zoned(data, self.signed, self.scale)
        else:
            return _decode_alpha(data)


def _decode_comp3(data: bytes, scale: int) -> str:
    """Decode COMP-3 (packed BCD) bytes into a decimal string."""
    hex_str = data.hex()
    digits_str = hex_str[:-1]       # all nibbles except the sign nibble
    sign_nibble = hex_str[-1].upper()
    try:
        value = int(digits_str)
    except ValueError:
        return ""
    if sign_nibble == "D":
        value = -value
    if scale:
        return f"{value / (10 ** scale):.{scale}f}"
    return str(value)


def _decode_zoned(data: bytes, signed: bool, scale: int) -> str:
    """Decode EBCDIC zoned decimal (display numeric) bytes."""
    digits = []
    sign = 1
    for i, byte in enumerate(data):
        zone = (byte >> 4) & 0x0F
        digit = byte & 0x0F
        if digit > 9:
            return ""   # invalid nibble
        if i == len(data) - 1 and signed:
            if zone == 0xD:
                sign = -1
            # zone C or F → positive
        digits.append(str(digit))
    try:
        value = int("".join(digits)) * sign
    except ValueError:
        return ""
    if scale:
        return f"{value / (10 ** scale):.{scale}f}"
    return str(value)


def _decode_alpha(data: bytes) -> str:
    """Decode EBCDIC alphanumeric bytes to a UTF-8 string (trailing spaces stripped)."""
    try:
        return data.decode(EBCDIC_ENCODING).rstrip()
    except Exception:
        return data.hex()


def _collect_fields(item: ET.Element, extra_offset: int = 0, prefix: str = "") -> list:
    """
    Recursively walk an XML <item> element and return a list of FieldDef objects.

    extra_offset: additional byte offset added to all positions (used for OCCURS expansion)
    prefix:       column-name prefix accumulated from parent group names
    """
    # Skip REDEFINES alternatives — we use the original (primary) field only
    if item.get("redefines"):
        return []

    name = item.get("name", "")
    if not name or name.upper() == "FILLER":
        return []

    occurs = int(item.get("occurs", 1))
    picture = item.get("picture")
    storage_length = int(item.get("storage-length", 0))
    position = int(item.get("position", 1)) - 1   # convert to 0-based

    children = [c for c in item if c.tag == "item"]
    full_name = f"{prefix}{name}" if prefix else name

    fields = []

    if picture and not children:
        # ── Leaf field ─────────────────────────────────────────────────────
        is_comp3 = item.get("usage") == "computational-3"
        is_numeric = item.get("numeric") == "COBOL_NUMERIC"
        scale = int(item.get("scale", 0))

        for i in range(occurs):
            col_name = f"{full_name}[{i + 1}]" if occurs > 1 else full_name
            # For leaf OCCURS, each occurrence is storage_length bytes apart
            field_pos = extra_offset + position + i * storage_length
            fields.append(FieldDef(
                name=col_name,
                position=field_pos,
                storage_length=storage_length,
                is_comp3=is_comp3,
                is_numeric=is_numeric,
                scale=scale,
                picture=picture,
            ))

    elif children:
        # ── Group field — recurse, expanding OCCURS ────────────────────────
        for i in range(occurs):
            # For group OCCURS, all children are shifted by i * group_storage_length
            child_extra = extra_offset + i * storage_length
            occ_name = f"{full_name}[{i + 1}]" if occurs > 1 else full_name
            child_prefix = f"{occ_name}."
            for child in children:
                fields.extend(_collect_fields(child, child_extra, child_prefix))

    return fields


def parse_copybook_xml(xml_path: Path) -> dict:
    """
    Parse cb2xml output XML.

    Returns a dict mapping record-type name → list[FieldDef].
    e.g. {"FLD-REC": [...], "WELL-REC": [...]}
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    records = {}
    for top_item in root.findall("item"):
        rec_name = top_item.get("name")
        if not rec_name:
            continue
        fields = []
        for child in top_item:
            if child.tag == "item":
                fields.extend(_collect_fields(child, extra_offset=0, prefix=""))
        records[rec_name] = fields
        print(f"  {rec_name}: {len(fields)} fields")
    return records


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 & 5: Read EBCDIC file and decode records
# ─────────────────────────────────────────────────────────────────────────────

# First byte of a record in EBCDIC encodes the record type:
#   0xF1 = '1' → FLD-REC   (gas field record)
#   0xF5 = '5' → WELL-REC  (well record)
# (The copybook defines codes for two 01-level items; confirmed from actual data.)
_REC_TYPE_MAP = {0xF1: "FLD-REC", 0xF5: "WELL-REC"}


def process_file(ebcdic_gz: Path, records_def: dict, out_prefix: Path):
    """
    Read the EBCDIC gz file, decode every record, write to CSV.
    Separate CSV files are produced for each record type found in records_def.
    """
    type_writers = {}
    type_fields = {}
    out_files = {}

    for rec_name, fields in records_def.items():
        suffix = rec_name.lower().replace("-", "_")
        csv_path = out_prefix.parent / f"{out_prefix.name}_{suffix}.csv"
        f = open(csv_path, "w", newline="", encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow([fd.name for fd in fields])
        type_writers[rec_name] = writer
        type_fields[rec_name] = fields
        out_files[rec_name] = (f, csv_path)
        print(f"  Writing: {csv_path}")

    counts: dict = {}
    record_num = 0

    opener = gzip.open if str(ebcdic_gz).endswith(".gz") else open
    with opener(ebcdic_gz, "rb") as infile:
        while True:
            raw = infile.read(RECORD_LENGTH)
            if not raw:
                break
            if len(raw) < RECORD_LENGTH:
                print(f"Warning: short record #{record_num + 1} ({len(raw)} bytes) — skipped",
                      file=sys.stderr)
                break

            rec_type = _REC_TYPE_MAP.get(raw[0], "UNKNOWN")
            counts[rec_type] = counts.get(rec_type, 0) + 1
            record_num += 1

            if rec_type in type_writers:
                row = [fd.decode(raw) for fd in type_fields[rec_type]]
                type_writers[rec_type].writerow(row)

            if record_num % 10_000 == 0:
                print(f"  ... {record_num:,} records processed")

    for f, _ in out_files.values():
        f.close()

    print(f"\n  Total records: {record_num:,}")
    for rec_type, count in sorted(counts.items()):
        print(f"    {rec_type}: {count:,}")
    for rec_name, (_, csv_path) in out_files.items():
        print(f"  Output → {csv_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert GSA020 EBCDIC data file to CSV using cb2xml for layout")
    parser.add_argument("--copybook", default="gsa020_copybook.cbl",
                        help="COBOL copybook (default: gsa020_copybook.cbl)")
    parser.add_argument("--xml", default=None,
                        help="Path to write/read the cb2xml-generated XML "
                             "(default: <copybook>.gen.xml)")
    parser.add_argument("--ebcdic", default="gsf001l.ebc.gz",
                        help="EBCDIC data file, plain or .gz (default: gsf001l.ebc.gz)")
    parser.add_argument("--output", default="gsa020",
                        help="Output CSV base name prefix (default: gsa020)")
    parser.add_argument("--skip-cb2xml", action="store_true",
                        help="Reuse an existing XML file instead of running cb2xml again")
    args = parser.parse_args()

    copybook = (SCRIPT_DIR / args.copybook).resolve()
    xml_path = Path(args.xml).resolve() if args.xml else copybook.with_suffix(".gen.xml")
    ebcdic = (SCRIPT_DIR / args.ebcdic).resolve()
    out_prefix = (SCRIPT_DIR / args.output).resolve()

    # ── Step 1: Pre-process copybook ─────────────────────────────────────────
    print("Step 1: Pre-processing copybook …")
    cleaned = preprocess_copybook(copybook)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".cbl", delete=False) as tmp:
        tmp.write(cleaned)
        tmp_path = Path(tmp.name)

    try:
        # ── Step 2: Run cb2xml ────────────────────────────────────────────────
        if not args.skip_cb2xml or not xml_path.exists():
            print("\nStep 2: Running cb2xml …")
            run_cb2xml(tmp_path, xml_path)
        else:
            print(f"\nStep 2: Skipping cb2xml, using existing XML: {xml_path}")
    finally:
        tmp_path.unlink(missing_ok=True)

    # ── Step 3: Parse XML ─────────────────────────────────────────────────────
    print("\nStep 3: Parsing copybook XML …")
    records_def = parse_copybook_xml(xml_path)

    # ── Steps 4 & 5: Read EBCDIC → CSV ───────────────────────────────────────
    print(f"\nSteps 4-5: Decoding EBCDIC file → CSV …")
    process_file(ebcdic, records_def, out_prefix)

    print("\nDone.")


if __name__ == "__main__":
    main()
