Good thinking — broadening the scope makes the API case much stronger and positions it as a systemic improvement rather than a one-off request. Let me check that page first to make sure I reference it accurately.Good — I can see the full breadth of what's on that page: digital map data, drilling permits, production data, all delivered via GoAnywhere (mft.rrc.texas.gov) in ASCII, EBCDIC, dBase, and shape file formats. Here's the updated letter:

---

**Date:** March 11, 2026

Open Records Division
Railroad Commission of Texas
PO Box 12967
Austin, Texas 78711-2967

**Re: Public Information Act Request – Gas Ledger (GSA) Historical Production Data and Request for Public API Access Across All RRC Data Sets**

---

Dear Open Records Team,

I am writing to make two related and equally important requests regarding Gas Ledger (GSA) historical production data maintained by the Railroad Commission of Texas (RRC). These requests are part of an ongoing analysis project focused on Texas natural gas production trends, and together they represent what I believe would be the most practical and durable solution for both the RRC and the public.

---

**Request 1: Complete Historical GSA Production Data**

Pursuant to the Texas Public Information Act (Chapter 552, Texas Government Code), I hereby request the complete historical Gas Ledger (GSA) production data available in the RRC's records, provided in a machine-readable format such as CSV, JSON, or a similar structured data format.

In this spirit, I would also gently note that providing data exclusively in EBCDIC — a mainframe encoding format that predates modern computing conventions by decades — places a significant and unnecessary burden on the public. While the RRC's obligation under the PIA is to make information available, publishing data in a format that effectively requires specialized technical expertise or the hiring of a consultant to parse and decode it falls short of the spirit of genuine public accessibility. A truly public dataset should be readable by the public it serves, ideally in a modern, open format without additional cost or expertise required.

---

**Request 2: Development of a Public API for Ongoing GSA Data Access — and Across All RRC Data Sets**

I also respectfully and earnestly request that the RRC consider developing a public-facing API to allow citizens, researchers, and analysts to download GSA production data programmatically on an ongoing basis. This is not a secondary or aspirational request — it is the sustainable, long-term solution that would serve the public interest and the Commission equally well.

While this request originates from a need for GSA Gas Ledger data specifically, I would encourage the RRC to think more broadly. The Commission currently publishes a wide range of valuable public data sets at [https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/](https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/), including digital map layers, drilling permit records, well data, production reports, and more. All of these data sets face the same accessibility challenges, and all would benefit equally from a modern, consistent API interface. Extending an API solution across all of these data sets — rather than treating each as a one-off problem — would be a far more efficient use of the RRC's development resources and would serve the broadest possible public benefit.

Without a proper API, analysts who need this data have little choice but to write custom code to work around the existing GoAnywhere file delivery system. This kind of automated scraping places an unnecessary and avoidable burden on RRC web infrastructure and is a poor substitute for a purpose-built data access solution. A well-designed API would:

- Eliminate uncontrolled scraping traffic that strains the RRC's web servers and delivery systems.
- Dramatically reduce the volume of repetitive Public Information Act requests that the open records team must process, freeing staff time and resources.
- Make public data directly and reliably accessible to citizens, researchers, academics, and policymakers without requiring technical workarounds.
- Reinforce the RRC's commitment to open government and transparency as envisioned by the Public Information Act.
- Eliminate the need for citizens to pay commercial third-party vendors for access to data that is, by right, publicly available at no cost.

I want to be clear that I am not seeking to circumvent any legitimate cost-recovery processes. However, as a citizen and researcher, I firmly believe that public data — produced and maintained at taxpayer expense — should be accessible directly from the source agency, not gated behind commercial intermediaries who charge fees for information the public already owns.

I recognize that developing an API is a meaningful undertaking, and I am happy to provide input on the data fields, query parameters, pagination strategies, or formats that would be most useful. I would welcome the opportunity to speak with appropriate RRC technical or IT staff about how such a solution might be scoped and implemented.

Thank you sincerely for your time and consideration. I have great respect for the work that the RRC and the open records team do in service of Texas citizens, and I appreciate your thoughtful review of both requests.

Respectfully,

[Your Name]
[Your Address]
[City, State, ZIP]
[Phone Number]
[Email Address]

---

The key addition is in Request 2 — it names the full data sets page explicitly, lists the variety of data already published there (maps, permits, wells, production), and makes the case that a single API investment would solve the problem across the board rather than piecemeal. That's a much stronger argument for their IT and management leadership to act on.
