 # Football Moneyball Analytics Pipeline

An end-to-end data analytics and ETL pipeline built to identify undervalued football players by combining statistical performance metrics with market valuations.

---

## Overview
This project applies "Moneyball" analytics principles to modern football data. Using a custom Python ETL script and Microsoft SQL Server, the pipeline ingests player performance metrics, transforms raw stats, and executes relational SQL queries to pinpoint target players whose pitch output significantly exceeds their market value.

---

## Tech Stack & Architecture
* **Language:** Python (`pandas`, `pyodbc`)
* **Database:** Microsoft SQL Server (T-SQL)
* **Pipeline:** Automated ETL script (`etl_pipeline.py`)
* **Data Analysis:** SQL queries (`moneyball_analaysis.sql`) for player efficiency scoring and valuation comparisons

---

## Repository Structure
* **`etl_pipeline.py`** – Automated Python script connecting data sources to the local SQL Server instance.
* **`moneyball_analaysis.sql`** – Advanced T-SQL queries aggregating player stats, performance metrics, and valuation rankings.

---

## Key Analytics & Methodology
1. **Data Ingestion (ETL):** Cleaning and mapping player datasets into relational SQL database tables.
2. **Performance vs. Value Index:** Calculating key performance ratios (goals/assists per 90, progressive actions, defensive efficiency) against current market values.
3. **Target Identification:** Filtering high-performing candidates operating below benchmark market valuations.

---

## Future Enhancements
- Connect interactive visualizations via Power BI / Tableau dashboards.
- Incorporate machine learning models for market value estimation.
