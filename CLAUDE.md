# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Research environment for analyzing East Texas oil well data (RRC / GSA020 dataset) using machine learning. Focus areas include locating undocumented orphaned wells, predicting missing well log data, seismic risk correlation with disposal wells, and identifying stranded gas for AI power infrastructure.

## Dev Environment

The primary environment is Docker. All tools (Java/cb2xml, Python 3.12, JupyterLab, Kaggle CLI) run inside the container.

```sh
# Build
docker build -t wellx3 .

# Run (mounts Kaggle credentials and project files)
docker run -p 8888:8888 -v ~/.kaggle:/root/.kaggle:ro -v $(pwd):/wellx3 wellx3
```

JupyterLab is available at http://localhost:8888. The `/wellx3` directory inside the container maps to the project root.

## Key Scripts

**`gsa020_to_csv.py`** — Main data pipeline. Converts the GSA020 EBCDIC fixed-width file (`gsf001l.ebc.gz`) to CSVs using a COBOL copybook as the schema.

```sh
# Full run (inside container or with Java + cb2xml available)
python3 gsa020_to_csv.py

# Skip re-running cb2xml if XML already generated
python3 gsa020_to_csv.py --skip-cb2xml

# Custom paths
python3 gsa020_to_csv.py --copybook gsa020_copybook.cbl --ebcdic gsf001l.ebc.gz --output gsa020
```

Outputs: `gsa020_fld_rec.csv` (gas field records) and `gsa020_well_rec.csv` (well records).

## Architecture of `gsa020_to_csv.py`

The pipeline has 5 steps:

1. **Preprocess copybook** — Strips the FD header block and applies hardcoded `COMP3_FIXES` for three fields (`PER-WELL`, `ACRG-FACT`, `OTHER-FACT`) that are missing `COMP-3` in the available copybook but confirmed packed-decimal from the authoritative layout doc.
2. **Run cb2xml** — Invokes `cb2xml.jar` (Java) via subprocess to parse the COBOL copybook into XML field layout. Uses `cb2xml/lib/cb2xml.jar` relative to the script.
3. **Parse XML → FieldDef list** — `_collect_fields()` recursively walks the cb2xml XML tree, expanding `OCCURS` clauses into individual columns and skipping `REDEFINES` alternatives.
4. **Read EBCDIC gz file** — Fixed 2120-byte records. First byte determines record type: `0xF1` = FLD-REC, `0xF5` = WELL-REC.
5. **Decode fields → CSV** — Each `FieldDef.decode()` dispatches to `_decode_comp3`, `_decode_zoned` (EBCDIC display numeric), or `_decode_alpha` (EBCDIC text, `cp037` encoding).

## cb2xml Tool

cb2xml is a Java library/CLI that parses COBOL copybooks into XML. The jar is at `cb2xml/lib/cb2xml.jar`. Inside the Docker container it's also available as the `cb2xml` command.

```sh
# Parse a copybook to XML (inside container)
cb2xml myfile.cbl

# Direct jar invocation
java -jar cb2xml/lib/cb2xml.jar -cobol myfile.cbl -xml out.xml -XmlFormat 2017 -Dialect Mainframe
```

## Data Sources

- **GSA020 EBCDIC file**: `gsf001l.ebc.gz` — raw RRC data, 2120-byte fixed-length records
- **Copybook**: `gsa020_copybook.cbl` (not yet committed) — COBOL layout definition
- **Kaggle**: Mount `~/.kaggle/kaggle.json` for dataset access; the 3W dataset (`afrniomelo/3w-dataset`) is a benchmark for anomaly detection in oil wells
- **RRC Digital Map Data**: Shapefile format for well locations, mergeable with geopandas
