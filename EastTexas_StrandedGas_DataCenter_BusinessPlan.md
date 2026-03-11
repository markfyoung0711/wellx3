# East Texas Stranded Gas — AI Data Center Power Business Plan
### Identifying, Mapping, and Monetizing Stranded Natural Gas for the Haynesville / East Texas AI Power Revolution

*Confidential — March 2026*

---

## Executive Summary

Texas is in the middle of the largest energy-infrastructure build-out in a generation. Demand for data center power is projected to grow from 8 GW today to over 40 GW by 2028 — and East Texas, sitting atop the Haynesville Shale, is uniquely positioned to capture that wave.

This business plan outlines a data analytics and site-intelligence company whose product is a single, high-value deliverable: a machine-learning-powered map of stranded natural gas assets in East Texas, correlated with fiber infrastructure, water access, land availability, and grid proximity — the exact data that data center developers and gas producers need to make billion-dollar siting decisions.

> **THE GAP:** West Texas Permian producers lack the pipeline and grid infrastructure to compete for data center customers. The Haynesville/East Texas fields already have transmission lines, a more robust fiber network, and proximity to LNG hubs — but no one has systematically mapped which stranded gas assets are most "data-center ready." This company fills that gap.

The immediate revenue model is a paid intelligence report and data subscription sold to gas producers, data center developers, and infrastructure investors. Phase 2 is a co-development brokerage matching stranded gas assets with data center site developers for a success fee. Phase 3 is optional equity participation in physical co-located power-and-compute developments.

| Factor | Detail |
|---|---|
| **Business Type** | Data analytics, site intelligence, energy-tech brokerage |
| **Target Geography** | East Texas / Haynesville Shale — Gregg, Rusk, Panola, Nacogdoches, Angelina, Sabine counties |
| **Primary Product** | Stranded Gas Intelligence Report + data subscription |
| **Phase 2 Revenue** | Transaction brokerage — matching gas assets to data center developers |
| **Target Customers** | Independent gas producers, data center developers, infrastructure investors |
| **Key Advantage** | Haynesville is confirmed superior to Permian for data center proximity |
| **Anchor Deal in Market** | AmpZ Project LufKin — 2.1 GW campus actively seeking onsite self-generation by 2029 |
| **Startup Capital Needed** | ~$150,000–$300,000 (Phase 1 lean-start); $1M–$3M for full build-out |

---

## Section 1: Market Opportunity

### 1.1 The National Picture

The AI infrastructure build-out is creating unprecedented demand for reliable, co-located natural gas power. Several major trends converge to make this the right moment:

- Texas is on track to become the largest data center market in the U.S., surpassing Virginia by 2030.
- Data center power demand in Texas is projected to jump from 8 GW (2025) to over 40 GW by 2028.
- Nearly half of all new data center power plants being built in Texas will operate off-grid, using direct natural gas — they will not connect to ERCOT.
- The U.S. will need 400 terawatt-hours of additional power within five years just to support AI — roughly enough to power France for a year.

### 1.2 Why East Texas / Haynesville Wins

> **KEY FINDING:** A September 2025 report directly concluded that Haynesville and Eagle Ford producers are far better positioned than Permian Basin operators to supply AI data centers — due to superior fiber, transmission infrastructure, and proximity to LNG hubs.

| Infrastructure Factor | East Texas / Haynesville | West Texas / Permian |
|---|---|---|
| Fiber Optic Network | Robust — close to I-20 corridor and DFW hubs | Sparse — limited routes |
| Power Transmission Lines | Well-equipped, less congested | Underdeveloped, congested |
| LNG Export Proximity | Close to Gulf Coast export terminals | Far — pipeline bottleneck |
| Stranded Gas Volume | Significant legacy and Haynesville production | Massive but landlocked |
| Water Availability | Abundant — Sabine River basin | Scarce — drought risk |
| Data Center Activity | AmpZ 2.1 GW Project LufKin announced 2026 | Several projects but power-constrained |

### 1.3 The AmpZ / Lufkin Anchor Deal

The single most important market signal for this business is the February 2026 announcement of AmpZ's **Project LufKin** — a gigawatt-scale data center campus in Angelina County, East Texas, at the former Southland Paper Mill site:

- 1,041 acres acquired; expandable to 4,000 acres
- 55 MW of live grid capacity today; 175 MW by late 2026; 1.1 GW by 2028
- **1 GW of planned onsite self-generation capacity needed by 2029 — this is the gap your company fills**
- Mayor of Lufkin called it "a once-in-a-lifetime project" worth billions in investment

> **YOUR ENTRY POINT:** AmpZ needs 1 GW of onsite self-generation by 2029. They need a partner who can identify which nearby stranded gas assets — wells, gathering systems, or pipeline taps — can supply that generation at the lowest cost and fastest timeline. That intelligence product is what this business delivers.

---

## Section 2: The Business — What You Are Building

### 2.1 Core Product: The East Texas Stranded Gas Intelligence Platform

Your company's core product is a machine-learning-enhanced database and report series that answers one question for clients:

> *"Which East Texas gas assets are closest to being data-center-ready, and what would it take to connect them?"*

To answer that question, you correlate five data layers using RRC production data, satellite imagery, GIS mapping, and public infrastructure records:

| Data Layer | What It Contains | Source |
|---|---|---|
| Gas Production | Well-level flow rates, shut-in wells, gathering lines, historical output declines | RRC Digital Map Data (public, free) |
| Power Grid | Transmission line locations, substation capacity, ERCOT interconnect queue data | ERCOT, RRC, public GIS |
| Fiber Optic Corridors | Existing fiber routes, ISP infrastructure, latency zones near I-20 and DFW corridors | FCC broadband maps, NTIA data |
| Land & Water | Available industrial acreage, water rights/availability, floodplain risk, site access | County appraisal records, TWDB |
| Regulatory Status | P-5 operator status, pipeline permits, environmental flags, RRC compliance history | RRC OGSR database (public) |

### 2.2 The ML Layer — How You Create Defensible Competitive Advantage

Raw data correlation is a commodity. Your moat is the scoring model. You build a **"Data Center Readiness Score"** for every gas-producing asset in the East Texas / Haynesville zone:

- Train a gradient-boosted model (XGBoost or Random Forest) on known successful behind-the-meter gas-to-power projects nationally
- Score each East Texas asset on proximity to fiber, grid headroom, water access, gas pressure/volume adequacy, and land availability
- Output a tiered ranking: **Tier 1** (ready now), **Tier 2** (ready in 12–18 months), **Tier 3** (longer-term)
- Update quarterly as new RRC production data is published

> **YOUR MOAT:** Once you have 12–18 months of scored data and client feedback built into the model, the scoring algorithm becomes a defensible proprietary asset that competitors cannot replicate quickly. The data is public; the model trained on outcomes is yours.

---

## Section 3: The Key Players — Who You Need

### 3.1 Customer #1: Data Center Developers (Your Highest-Value Buyer)

These companies will pay the most for your intelligence because they are making billion-dollar land and power decisions right now:

| Company | What They're Building | Your Pitch to Them |
|---|---|---|
| **AmpZ (Project LufKin)** | 2.1 GW campus, Angelina County — needs 1 GW onsite self-generation by 2029 | You identify the nearest, highest-volume stranded gas assets that can supply their onsite generation. Most urgent opportunity. |
| **Crusoe Energy** | Behind-the-meter gas-to-compute nationally; actively seeking East Texas assets | Your Tier 1 scored assets are exactly what Crusoe's site team needs to evaluate new locations. |
| **Titus Low Carbon Ventures** | Building half a dozen data center parks across Texas using modular gas engines | Site selection intelligence — which East Texas counties have the right gas + fiber + land combo |
| **Energy Transfer (CloudBurst JV)** | 1,200 MW gas-fired private data center campus in Texas | Pipeline and gathering optimization for future East Texas expansion |
| **PowerBridge (Five Point)** | Data center parks in Texas with dedicated gas-fired plants | East Texas site scoring for expansion beyond Permian |

### 3.2 Customer #2: East Texas Gas Producers (Your Local Data Sellers and Buyers)

These operators own the stranded gas. They want to know if their shut-in or low-value wells can suddenly become highly valuable power assets. They are also your data partners — their cooperation on well-level flow data (beyond RRC public records) gives you proprietary input.

- **XTO Energy** (ExxonMobil subsidiary) — major Haynesville operator; Tyler/Longview footprint
- **Chesapeake Energy** — significant Haynesville acreage; actively seeking new revenue streams for low-margin gas
- **Mewbourne Oil Company** — East Texas and Oklahoma; privately held; receptive to new monetization models
- **Navidad Resources** — East Texas-focused independent; smaller and more accessible as a first conversation
- **Faulconer Energy** (Tyler, TX) — local independent, acquisition-focused; excellent network into smaller operators
- **East Texas Producers and Royalty Owners group** — the organized body of local producers; the annual symposium at Kilgore College is your best single networking event

### 3.3 Customer #3: Infrastructure Investors and Energy Finance

These players provide capital for the physical build-out phase (Phase 2/3) and are also buyers of your intelligence reports as deal-sourcing tools:

- **Five Point Infrastructure** — already backing PowerBridge's Texas gas-to-data-center play; would pay for East Texas deal flow
- **Carlyle Group** — backed AmpZ/Amp Energy; actively seeking additional sites in the region
- **East Daley Analytics** — energy intelligence firm that has explicitly forecast the gas-to-data-center market; a potential acquirer or white-label partner
- **Houston-based energy PE firms** — your intelligence report is a direct input to their investment theses

### 3.4 Government and Regulatory Partners (Non-Paying but Critical)

| Partner | Role |
|---|---|
| **Railroad Commission of Texas (RRC)** | Primary source for all well and operator data via OGSR database. A working relationship with RRC District 5 (Longview) gives you access to staff who know the local field intimately. |
| **Kilgore College / East Texas Oil Museum** | Hosts the annual East Texas Energy Symposium — the best single event to meet every producer in the region. Their petroleum tech program is also a talent pipeline. |
| **Kilgore EDC** | Actively recruiting industrial tenants; will connect you to land and utility contacts across the region. |
| **East Texas Economic Development District (ETEDD)** | Regional planning body. Their infrastructure data (broadband, water, industrial land) complements your gas data. |
| **UT Tyler — CS / Data Analytics** | Research partnership potential for ML model development; access to graduate students as low-cost analysts. |
| **Angelina County / City of Lufkin** | Direct relationship with officials managing AmpZ Project LufKin; your data may directly inform their economic development planning. |

### 3.5 Technical and Data Partners

- **Novi Labs** (novilabs.com) — Houston-based, specializes in ML for O&G well performance. Either a competitor to monitor or a white-label data partner for the gas production analytics layer.
- **Open Subsurface Data Universe (OSDU)** — open-source platform standardizing O&G data globally. Joining this ecosystem gives you interoperability with major operator data systems.
- **Logix Fiber Networks** — Houston-based, 300,000+ fiber miles in Texas; their expansion maps are a direct input to your fiber proximity scoring layer.
- **ERCOT** — interconnect queue data reveals exactly where grid headroom exists near gas-producing areas.

---

## Section 4: Business Model and Revenue

### 4.1 Three-Phase Revenue Progression

#### Phase 1: Intelligence Product (Months 1–12)

Build and sell the East Texas Stranded Gas Intelligence Report and accompanying GIS data subscription. This is a lean, capital-efficient start.

- **Flagship Report:** "East Texas Stranded Gas to Data Center Readiness: 2026 Analysis" — a 60–100 page PDF/interactive report with ranked asset maps, scoring methodology, and Tier 1/2/3 asset lists
- **Price:** $15,000–$25,000 per report license for operators/investors; $5,000–$8,000 for smaller independents
- **Data Subscription:** Quarterly updated scoring dashboard — $2,000–$5,000/month per subscriber
- **Target:** 10–20 paying customers in Year 1; $200K–$500K revenue

#### Phase 2: Transaction Brokerage (Months 12–30)

Leverage your intelligence platform to broker introductions and deals between gas asset owners and data center developers. You earn a success fee on completed transactions.

- **Structure:** 1–3% brokerage fee on the value of a gas supply agreement or site development deal
- A single 100 MW behind-the-meter deal (~$150–200M in infrastructure value) generates **$1.5M–$6M in fees**
- Target: 2–4 transactions in Year 2–3

#### Phase 3: Equity Co-Development (Year 3+)

Take equity stakes in specific behind-the-meter gas-to-power projects you help identify and broker.

- **Structure:** Contribute your intelligence and deal origination as "sweat equity" for a 5–15% stake in a project SPV
- A single 50 MW gas-to-compute project at $1,500/kW replacement cost implies $75M in project value; 10% equity = **$7.5M**

### 4.2 Revenue Projections

| Revenue Stream | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Intelligence Reports | $150,000–$300,000 | $250,000–$500,000 | $400,000–$700,000 |
| Data Subscriptions | $50,000–$100,000 | $150,000–$300,000 | $300,000–$600,000 |
| Brokerage Fees | $0 | $500,000–$3,000,000 | $1,000,000–$6,000,000 |
| Equity / Co-Dev | $0 | $0 | Upside TBD |
| **TOTAL (Conservative)** | **$200,000** | **$650,000** | **$1,700,000** |
| **TOTAL (Aggressive)** | **$400,000** | **$3,800,000** | **$7,300,000** |

---

## Section 5: Marketing and Go-to-Market Strategy

### 5.1 The First 90 Days — Proof of Concept

Before selling anything, build a compelling demo. The goal of the first 90 days is to produce a free, public-facing "teaser report" — a 10–15 page preview of the full intelligence product — that demonstrates the methodology and generates inbound leads.

- **Month 1:** Download and process RRC Haynesville/East Texas well data. Build base GIS map. Identify top 20 Tier 1 candidates.
- **Month 2:** Overlay fiber (FCC maps), grid (ERCOT), and water data. Run initial scoring model. Produce the teaser report.
- **Month 3:** Distribute teaser at the East Texas Energy Symposium (Kilgore College), through LinkedIn to O&G executives, and directly to AmpZ's development team.

### 5.2 Sales Channels

| Channel | Strategy |
|---|---|
| **East Texas Energy Symposium (Kilgore College)** | Annual gathering of every significant producer in the East Texas field. Present a poster or sponsor a session. Highest-ROI marketing event. |
| **Direct Outreach to AmpZ Project LufKin** | They are actively seeking onsite self-generation partners. A cold email with your teaser report is a credible first contact. |
| **LinkedIn / Energy Executive Networks** | Target VP-level land, operations, and BD executives at Chesapeake, XTO, and midstream companies. The teaser report is the conversation starter. |
| **RRC / Texas Energy Council Events** | RRC hosts virtual listening sessions every other month — networking with regulators and industry insiders. |
| **Energy Intelligence Trade Press** | Submit a bylined article to Hart Energy or Oil & Gas Journal. Establishes thought leadership; generates inbound. |
| **Kilgore College / UT Tyler Research Partnership** | Academic credibility and access to grad student labor for data processing. Opens doors with operators who respect institutional relationships. |

### 5.3 Positioning Statement

> **YOUR BRAND:** You are not a consulting firm. You are not an oil and gas company. You are the "Bloomberg Terminal for East Texas stranded gas" — the authoritative, data-driven platform that tells producers, developers, and investors exactly where the value sits and how to unlock it.

---

## Section 6: Operational Build-Out

### 6.1 Team You Need

| Role | Description |
|---|---|
| **Founder / CEO (You)** | Business development, client relationships, deal brokerage. Local East Texas credibility — knowing people in Kilgore, Longview, and Tyler is worth more than any credential. |
| **Data Scientist / ML Engineer** | Builds and maintains the scoring model. Can be part-time contractor initially — UT Tyler or Texas A&M Commerce are local sources. Budget: $80K–$120K/yr or $50–100/hr contract. |
| **GIS / Data Analyst** | Processes RRC data, builds the maps, maintains the database. Kilgore College petroleum tech program is a pipeline. Budget: $50K–$70K/yr or contract. |
| **Energy Industry Advisor (Board)** | A retired XTO, Chesapeake, or pipeline executive with East Texas relationships. Equity compensation (1–3%). Their Rolodex is the fastest path to first revenue. |
| **Legal / Regulatory Counsel** | Energy attorney familiar with RRC filings, gas supply agreements, and land/mineral rights. Tyler or Longview-based; project basis initially. |

### 6.2 Technology Stack

- **Data Ingestion:** Python (Geopandas, Pandas) — processing RRC shapefiles and production CSVs
- **ML Modeling:** XGBoost / Random Forest via scikit-learn — building the readiness scoring model
- **GIS Visualization:** QGIS (open source) for internal analysis; Mapbox or ArcGIS Online for client-facing deliverables
- **Database:** PostgreSQL with PostGIS extension — spatial queries on well locations and infrastructure layers
- **Reporting:** Python (Matplotlib/Plotly) for charts; InDesign/Canva for final report packaging
- **Dashboard (Phase 2):** Streamlit or Dash for a web-based subscription data product; hosted on AWS

### 6.3 Data Sources and Costs

| Data Source | What You Get | Cost |
|---|---|---|
| RRC OGSR Database | All Texas well locations, operator records, production data | **FREE** (public) |
| RRC Digital Map Shapefiles | Well locations, pipeline routes, field boundaries in GIS format | **FREE** (public) |
| ERCOT Grid Data | Transmission lines, substation locations, interconnect queue | **FREE** (public) |
| FCC Broadband Maps | Fiber and broadband infrastructure by location | **FREE** (public) |
| County Appraisal Records | Land ownership, acreage, industrial site availability | FREE–Low cost |
| IHS Markit / Enverus | Enhanced well production history, operator intelligence | $20K–$60K/yr *(defer to Phase 2)* |
| Operator Cooperation (direct) | Well-level flow data beyond RRC records — proprietary edge | Revenue share or report access |

### 6.4 Capital Requirements

| Item | Cost |
|---|---|
| **Phase 1 Lean Start (12 months)** | **$150,000–$300,000** |
| Founder salary / living expenses | $60,000–$100,000 |
| Contract data scientist (part-time) | $30,000–$50,000 |
| Data subscriptions and software | $10,000–$20,000 |
| Legal, travel, events, marketing | $20,000–$40,000 |
| Cloud infrastructure and tools | $5,000–$15,000 |
| **Full Build-Out (36 months)** | **$1,000,000–$3,000,000** |
| Full-time team of 4–6 | $500,000–$900,000/yr |
| Enverus/IHS data subscriptions | $40,000–$80,000/yr |
| Sales, marketing, events | $100,000–$200,000/yr |

---

## Section 7: Risks and Mitigation

| Risk | Description | Mitigation |
|---|---|---|
| Data center build slowdown | AI investment cycle could slow; projects could be cancelled or delayed | Focus Phase 1 on intelligence sales — these are needed even in a slower market for operators to plan |
| Large incumbents enter market | Enverus, IHS, or a major consultancy could build a competing product | Speed to market is key; get the first authoritative East Texas report published in 2026 before competitors |
| Operator data reluctance | Producers may not share proprietary production data beyond RRC records | Public RRC data is sufficient for Phase 1; operator data sharing becomes a Phase 2 upsell |
| Regulatory changes | Texas pipeline or power generation permitting could tighten | Monitor RRC and PUC proceedings; position as a regulatory intelligence asset, not just a data product |
| Capital access | Brokerage phase requires relationships before revenue | Target the annual East Texas Energy Symposium as the catalyst event for first paid relationships |

---

## Section 8: Your First 10 Actions

1. **Download RRC East Texas Haynesville well data** from rrc.texas.gov (free). Start with Gregg, Rusk, Panola, and Nacogdoches counties. Process in Python/Geopandas.

2. **Overlay FCC fiber maps and ERCOT transmission data** on your well map. Identify the top 20 gas-producing areas within 5 miles of both fiber and transmission lines.

3. **Contact AmpZ** (ampz.energy) with a one-page summary of your project and teaser findings. Ask for a 20-minute call with their development or site selection team.

4. **Register for the East Texas Energy Symposium** at Kilgore College. This is your most efficient single event for meeting producers.

5. **Reach out to Faulconer Energy** (Tyler, TX) and Navidad Resources as your first small-operator conversations. These are more accessible than majors and will validate your product concept.

6. **Identify one retired XTO, Chesapeake, or pipeline executive** in East Texas willing to serve as an advisory board member in exchange for equity (1–3%). Their network is the fastest path to first paying customers.

7. **Contact UT Tyler's Computer Science or Engineering department** about a research partnership or graduate student project. This gives you low-cost ML development resources and academic credibility.

8. **Publish the teaser report on LinkedIn** as a long-form article. Target VP-level O&G and data center executives. Goal: 5 inbound inquiries.

9. **File for an LLC in Texas** (Texas Secretary of State — ~$300). Open a business bank account. Establish the legal entity before any paid client engagements.

10. **Price your first report at $10,000** and offer 3 early clients a 50% "founding partner" discount ($5,000) in exchange for a testimonial and data sharing agreement. First revenue validates the model.

---

> **BOTTOM LINE:** The East Texas Haynesville is the most infrastructure-ready gas basin in Texas for the AI data center opportunity. AmpZ has already staked 1,000+ acres in Angelina County and needs 1 GW of self-generation by 2029. No one has built the intelligence product to connect stranded gas assets to that demand. That gap is your business.

---

*End of Business Plan*
