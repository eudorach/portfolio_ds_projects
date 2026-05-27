# Clinical Data & AI Pipeline Portfolio

**Healthcare builder at the intersection of surgical medicine and data engineering.**

I'm a Physician Assistant with surgical clinical experience, now building scalable data pipelines and AI-augmented workflows for healthcare and real-world evidence. My work combines deep domain knowledge — understanding how healthcare actually operates at the point of care — with the technical ability to build systems that make that knowledge scalable and reproducible.

I build with Python, SQL, and PostgreSQL, and leverage LLMs (Claude, GPT-4) as core development tools — not shortcuts, but force multipliers for producing higher-quality, faster-iterated work.

---

## Featured Project

### [NHANES Biomarker Analysis Pipeline](https://github.com/eudorach/portfolio_ds_projects/blob/main/NHANES_analysis/pipeline/README.md)

A reusable, end-to-end epidemiological pipeline built on the NHANES 2017–2020 Pre-Pandemic dataset — one of the most comprehensive population-level health surveys available.

**What it does:**
- Automated ingestion of 46 NHANES laboratory tables (`.xpt` format) into a structured PostgreSQL database
- Long-table architecture with a `biomarker_registry` that maps 345 biomarkers from raw NHANES codes to human-readable names — enabling new analyses without schema changes or hardcoded column references
- Reusable analysis functions (correlation, linear/logistic regression, quartile analysis, distribution plots) that accept any biomarker and disease combination via config — no rewriting code
- Clinically grounded cohort definitions based on ACC/AHA, WHO, and ADA guidelines
- Methodologically sound decisions: log transformation policy, multicollinearity handling, covariate adjustment, sex-stratified cohorts

**Analyses completed:**
- Urine biomarkers vs. BMI (n = 2,898)
- Carbohydrate metabolism markers vs. BMI, excluding diabetic participants (n = 3,478)
- SHBG vs. BMI in males aged 22–49 (n = 1,387)

**Stack:** Python · PostgreSQL · SQLAlchemy · pandas · statsmodels · seaborn · pyreadstat

**What makes it different:** Most NHANES analyses are one-off scripts. This is a system — designed so that asking a new clinical question is a matter of configuration, not rewriting code. That's the point.

---

## Skills & Approach

| Area | Detail |
|---|---|
| **Clinical Domain** | Surgical medicine, perioperative workflows, procedural and CPT coding, point-of-care clinical decision-making |
| **Data Engineering** | PostgreSQL schema design, long-table architecture, automated ingestion pipelines, modular reusable code |
| **Analysis** | Pearson correlation, linear & logistic regression, odds ratios, epidemiological methods, covariate adjustment |
| **Python** | pandas, SQLAlchemy, statsmodels, seaborn, pyreadstat |
| **AI-Augmented Development** | Daily use of LLMs (Claude, GPT-4) for code generation, iteration, and QA — building the way modern data teams actually work |

---

## Background

Surgical clinical experience gives me something most data engineers don't have: I understand how healthcare actually works at the point of care — the sequencing, the stakes, the documentation, the data that gets generated and why. I know how procedural and perioperative data is structured, what CPT codes represent in practice, and where real-world health data gets messy.

That clinical foundation, combined with a genuine drive to build systems and solve hard problems, is what I bring to healthcare data work.

---

*All projects are version-controlled, modular, and documented for reproducibility.*
