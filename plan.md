# East Texas Oil Well Data — Research & Data Planning

To find unexplored insights in East Texas oil well data using machine learning, pivot from standard production forecasting toward environmental, infrastructure, and historical data gaps. While major companies have optimized drilling for decades, there is significant "white space" in analyzing legacy records for new modern needs.

---

## Research Frontiers

- **Locating Undocumented Orphaned Wells (UOWs):** There are between 310,000 and 800,000 undocumented wells in the U.S. not in official databases. Use Computer Vision (U-Net models) on historical topographic maps and satellite imagery to find well symbols or surface disturbances that don't match existing RRC records. [1, 2, 3, 4]
- **Predicting Missing Well Log Data:** Many older East Texas wells have incomplete digital records. Build models to reconstruct missing log responses (shear sonic, density) by training on nearby "high-fidelity" wells with similar geophysical properties. [5]
- **Seismic Risk and Disposal Well Correlation:** Use ML to find patterns between fluid injection in disposal wells and localized seismic activity. The RRC is already using AI to clear backlogs, but independent research on East Texas long-term trends remains a high-value niche. [6]
- **Stranded Gas for AI Power Infrastructure:** Analyze gas production data to identify where stranded natural gas could power on-site AI data centers, correlating well flow data with proximity to fiber corridors and power grid gaps. [7, 8, 9]

---

## Dev Environment Setup

Build and run the Docker image that packages all required tools.

- **Tools included:** Java (cb2xml), cb2xml (COBOL copybook parser), Python 3.12, JupyterLab, Kaggle CLI, pandas, geopandas, scikit-learn, xgboost
- **Build:** `docker build -t wellx3 .`
- **Run:** `docker run -p 8888:8888 -v ~/.kaggle:/root/.kaggle:ro -v $(pwd):/wellx3 wellx3`
- **JupyterLab:** http://localhost:8888
- **cb2xml in container:** `cb2xml <copybook.cbl>`

**Kaggle CLI setup (local):**
```sh
pip install kaggle
# Place kaggle.json at ~/.kaggle/kaggle.json, then:
chmod 600 ~/.kaggle/kaggle.json
kaggle datasets list                                      # verify access
kaggle datasets download -d afrniomelo/3w-dataset        # 3W anomaly benchmark
```

---

## Data Sources

| Source | What You Get | Cost |
|---|---|---|
| RRC OGSR Database | All Texas well locations, operator records, production data | Free |
| RRC Digital Map Shapefiles | Well locations, pipeline routes, field boundaries (GIS) | Free |
| ERCOT Grid Data | Transmission lines, substation locations, interconnect queue | Free |
| FCC Broadband Maps | Fiber and broadband infrastructure by location | Free |
| County Appraisal Records | Land ownership, acreage, industrial site availability | Free–Low |
| 3W Dataset (Kaggle) | Anomaly detection benchmark for oil well events | Free |
| IHS Markit / Enverus | Enhanced well production history, operator intelligence | $20K–$60K/yr *(defer to Phase 2)* |

**Download steps:**
1. RRC Digital Map Data — well locations in Shapefile format, merge with Geopandas
2. 3W Dataset — `kaggle datasets download -d afrniomelo/3w-dataset`
3. FCC broadband maps and ERCOT transmission data — public GIS downloads

---

## Database and Storage Architecture — Phase 1 Free Stack

The database and storage choices at the start can either save you money or lock you in.

### Two-Layer Architecture

#### Layer 1: Raw / Source Data (Cold Storage — Data Lake)
**Google Cloud Storage or AWS S3** — both have free tiers (5 GB). Store raw RRC shapefiles, CSV production downloads, FCC broadband GeoJSON, and ERCOT data here as **Parquet files**. Parquet is columnar, compressed, and can be queried directly by DuckDB or BigQuery without loading into a database first.

Think of this as your filing cabinet — everything goes in here in its original form, versioned by quarter as new RRC data drops.

#### Layer 2: Processed / Scored Data (Hot Storage)
**Supabase (PostGIS)** — your cleaned, scored, and geocoded well assets live here. This is what your eventual client dashboard queries. The free tier (500 MB, unlimited API calls) handles Phase 1 easily; upgrade to their $25/month Pro plan when you have paying subscribers.

### Database Tool Comparison

**Supabase** — strongest recommendation for spatial/GIS work. Runs PostgreSQL + PostGIS under the hood with a web dashboard, no server to manage. Free tier handles all of Phase 1.

**DuckDB** — sleeper pick. In-process analytical database (runs inside Python, no server) that queries Parquet files, CSVs, and RRC shapefiles directly. Handles hundreds of millions of rows on a laptop. For Phase 1, DuckDB + cloud file storage may be all you need.

**Google BigQuery** — free tier: 10 GB storage, 1 TB queries/month. Integrates directly with Colab and Vertex AI. Strong option for tabular RRC data.

**PlanetScale** — no spatial extension support. Skip for this use case.

**Snowflake** — gets expensive fast. Skip until Phase 2.

### Recommended Phase 1 Stack (Free)

| Purpose | Tool | Cost |
|---|---|---|
| Raw data lake | Google Cloud Storage (Parquet files) | Free (5 GB) |
| Spatial queries + client DB | Supabase (PostGIS) | Free tier |
| ML model training | Google Colab | Free (GPU included) |
| Ad-hoc analysis | DuckDB (in Python locally) | Free |
| Dashboarding / demo | Streamlit Community Cloud | Free |
| Version control | GitHub | Free |

> **One thing worth paying for early:** A **$10/month Supabase Pro** account once your PostGIS DB hits the free tier limit. Losing your scored asset database mid-client-demo would be a serious problem. Everything else stays free until revenue comes in.

---

## Notebook Environment — Kaggle vs. Colab

They're more complementary than competitive. Use both for different purposes.

### Where Kaggle Wins

- **3W Dataset lives there natively** — zero friction loading it; no downloading or uploading
- **Persistent storage** — Kaggle notebooks survive session timeouts; free Colab environments are wiped on disconnect. Critical for long RRC processing jobs.
- **Public notebooks as a marketing tool** — a well-crafted public notebook (e.g., *"East Texas Haynesville Gas Asset Scoring — ML Approach"*) functions as a portfolio piece that data-savvy clients (Crusoe Energy, AmpZ) can evaluate. Builds credibility a PDF report cannot.
- **Dataset hosting** — upload cleaned RRC data as a Kaggle dataset; collaborators (UT Tyler, contract data scientist) just fork it, no file transfers needed
- **Better free GPU** — ~30 hours/week, less interruption than free Colab

### Where Colab Wins

- **Google ecosystem** — connects to GCS and BigQuery with two lines of code using your Google account
- **Colab Pro ($10/month)** — more RAM, longer runtimes, background execution; no Kaggle equivalent
- **Proprietary / client work** — Colab notebooks live in your own Google Drive; cleaner data ownership than Kaggle's servers
- **Faster iteration** — more flexible for rapid exploratory work

### When to Use Which

| Task | Use |
|---|---|
| Loading and exploring the 3W Dataset | Kaggle |
| Building public-facing proof-of-concept notebook | Kaggle (marketing asset) |
| Processing raw RRC shapefiles from GCS | Colab |
| Training XGBoost scoring model on proprietary data | Colab (data ownership) |
| Sharing work with UT Tyler research partner | Kaggle (easiest collaboration) |
| Anything client-facing or revenue-generating | Colab + your own Google Drive |

**Short version:** Kaggle is better for early proof-of-concept and public credibility work. Colab becomes more important once you have proprietary data and paying clients. In Phase 1, Kaggle is the higher priority.

---

## ML Approach and Algorithms

- **Tree-Based Models:** Random Forest or XGBoost for well performance forecasting, readiness scoring, and identifying "geologic sweet spots" [10, 13]
- **Computer Vision:** U-Net models on satellite imagery for undocumented orphan well detection [1, 2]
- **Reinforcement Learning:** Reward-based algorithms for subsurface flow and pressure prediction — being pioneered at Texas A&M [14]
- **Anomaly Detection:** Use the 3W Dataset as a benchmark for rare undesirable event detection in oil wells [12, 15]

---

## Community and Ecosystem

- **Open Subsurface Data Universe (OSDU)** — open-source platform standardizing O&G data globally; joining gives interoperability with major operator data systems [11]
- **Novi Labs** (novilabs.com) — Houston-based ML for O&G well performance; monitor as a competitor or explore as a white-label data partner [10, 13]
- **Logix Fiber Networks** — 300,000+ fiber miles in Texas; their expansion maps are a direct input to the fiber proximity scoring layer
- **Kilgore College / East Texas Oil Museum** — annual East Texas Energy Symposium; best single networking event for meeting producers

---

## References

[1] https://www.sciencedirect.com/science/article/abs/pii/S092041052100262X
[2] https://developer.nvidia.com/blog/ai-uncovers-potentially-hazardous-forgotten-oil-and-gas-wells/
[3] https://pubs.acs.org/doi/10.1021/acs.est.4c04413
[4] https://www.houstonchronicle.com/news/investigations/article/orphan-old-oil-wells-undocumented-ai-texas-report-19954499.php
[5] https://pubs.aip.org/aip/pof/article/37/3/036615/3339260/Enhancing-reservoir-characterization-A-novel
[6] https://www.mrt.com/business/oil/article/Railroad-Commission-turns-to-AI-to-boost-seismic-17230700.php
[7] https://www.expressnews.com/business/article/texas-permian-eagle-ford-natural-gas-data-centers-21066591.php
[8] https://www.bisnow.com/national/news/data-center-power/go-where-the-gas-is-data-centers-follow-the-fracking-in-search-for-power-131552
[9] https://collinsresearchportal.com/2025/08/18/permian-basin-the-next-ai-data-center-frontier/
[10] https://novilabs.com/machine-learning-in-oil-and-gas-industry/
[11] https://www.linkedin.com/pulse/mapping-texas-wells-integrating-qgis-python-rrc-data-chen-bsezc
[12] https://www.kaggle.com/datasets/afrniomelo/3w-dataset
[13] https://novilabs.com/blog/oil-and-gas-well-data-analysis-for-wells-in-production/
[14] https://techxplore.com/news/2021-02-positive-algorithm-underground-natural-reserves.html
[15] https://www.kaggle.com/discussions/getting-started/316927
