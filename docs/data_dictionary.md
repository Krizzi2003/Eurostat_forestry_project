# Data Dictionary

## Basic identifiers
| Column       | Description                                           | Notes |
|--------------|-------------------------------------------------------|-------|   
| country      | Country ISO code                                      | for example HR, AT, DE |
| year         | year which we observe                                 | 2021, 2022|

---

## General conventions and data handling rules

The following conventions apply to multiple indicators and feature tables in this project:

- Each information is related to years `2021` and `2022`.

- If the sum of imports and exports equals zero, or if all underlying values are missing,
  ratio-based indicators are set to `null`

- Unless explicitly stated otherwise, trade indicators are calculated using
  **total tree species (`TOTAL`)**, without separating coniferous and non-coniferous species.

- Aggregations are performed at the **country–year** level.

- When aggregating values:
  - numeric values are summed where at least one observation is available,
  - if all contributing values are missing, the result is set to `null`.

- EU-level aggregates (e.g. `EU27_2020`, `EA21`) are excluded from all datasets.

---

## Categories

### Roundwood removals by type of wood and assortment (Unit of measure: Thousand cubic metres)

These indicators represent the total volume of roundwood removed from forests during a given year.  
Values are broken down by:

| Column       | Description                                           |
|--------------|-------------------------------------------------------| 
| con_ob_remov  | Volume of coniferous roundwood measured including bark       | 
| con_ub_remov  | Volume of coniferous roundwood measured without bark         | 
| ncon_ob_remov | Volume of non-coniferous roundwood measured including bark   | 
| ncon_ub_remov | Volume of non-coniferous roundwood measured without bark     | 

---


### Roundwood removals under bark by type of ownership (Unit of measure: ratio)

This indicator describes the ownership structure of forests from which roundwood is removed measured in thousand cubic metres.
It measures the relative importance of private forest ownership compared to total forest ownership
(private + public) within each country and year.

| Column               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| private_forests_share | Share of privately owned forests in total forest area used for roundwood removals | 

**Notes:**
- The indicator is calculated as:  
  **private forests / (private forests + public forests)**.
- Values range from 0 to 1.

---

### Industrial roundwood by species (Unit of measure: ratio)

This indicator represents the trade structure of industrial roundwood for each country and year.
It measures the relative importance of imports compared to total international trade
(imports + exports) of industrial roundwood.

| Column                          | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| industrial_import/export_share  | Share of industrial roundwood imports in total industrial roundwood trade |

**Notes:**
- The indicator is calculated as:  
  **imports / (imports + exports)**.
- Imports and exports are measured in **thousand cubic metres (m³)**.
- Values range from 0 to 1:
  - values close to 1 indicate import-oriented countries,
  - values close to 0 indicate export-oriented countries.

---

### Sawnwood trade by species (Unit of measure: ratio)

This indicator describes the trade structure of sawnwood for each country and year.
It captures the relative importance of imports in total sawnwood trade. Measured in **thousand cubic metres (m³)**.

| Column                       | Description |
|------------------------------|-------------|
| sawnwood_import/export_share | Share of sawnwood imports in total trade, calculated as imports divided by the sum of imports and exports |

---

### Industrial roundwood by assortment (Unit of measure: Thousand cubic metres)

This table provides aggregated trade volumes of basic industrial wood products.
All assortments are summed to obtain total imports and exports of industrial roundwood
for each country and year.

| Column                       | Description |
|------------------------------|-------------|
| basic_wood_products_export   | Total exports of industrial roundwood assortments |
| basic_wood_products_import   | Total imports of industrial roundwood assortments |

---

### Roundwood, fuelwood and other basic products  
(Unit of measure: Thousand cubic metres, unless stated otherwise)

This table describes the production volumes of roundwood, fuelwood, and other basic
wood-related products. Indicators represent domestic production and are reported
at the country–year level.

Some products are measured in **thousand tonnes** instead of cubic metres, where no
volume-based unit is available.

| Column                                   | Description |
|------------------------------------------|-------------|
| roundwood_production                     | Total production of roundwood |
| fuelwood_production                      | Total production of fuelwood |
| industrial_roundwood_con_production      | Production of industrial roundwood from coniferous species |
| industrial_roundwood_ncon_production     | Production of industrial roundwood from non-coniferous species |
| wood_charcoal_production                 | Production of wood charcoal *(thousand tonnes)* |
| chp_res_production                       | Production of wood residues used for combined heat and power |
| chp_production                           | Production of wood used for combined heat and power |
| res_swd_production                       | Production of residues and wood chips (RES and RES_SWD combined) |
| pellet_agg_production                    | Production of aggregated pellets *(thousand tonnes)* |
| pellet_production                        | Production of pellets *(thousand tonnes)* |


---

### Sawnwood and wood-based panels  
(Unit of measure: Thousand cubic metres)

This table describes the production of sawnwood and wood-based panels.
Production volumes are reported at the country–year level and represent
domestic production.

Several products are reported separately for **coniferous** and
**non-coniferous** species where applicable.

| Column                                   | Description |
|------------------------------------------|-------------|
| sawnwood_con_production                  | Production of sawnwood from coniferous species |
| sawnwood_ncon_production                 | Production of sawnwood from non-coniferous species |
| wood-based_panels_production             | Total production of wood-based panels |
| veneer_sheets_con_production             | Production of veneer sheets from coniferous species |
| veneer_sheets_ncon_production            | Production of veneer sheets from non-coniferous species |
| plywood_con_production                   | Production of plywood from coniferous species |
| plywood_ncon_production                  | Production of plywood from non-coniferous species |
| pn_pb_production                         | Production of particleboard |
| fibreboard_production                    | Production of fibreboard |
| hardboard_production                     | Production of hardboard |
| medium_density_fiberboard_production     | Production of medium-density fibreboard (MDF) |
| other_fiberboard_production              | Production of other fibreboard products |

---

### Secondary wood products – trade  
(Unit of measure: Thousand EUR)

This table captures the international trade of secondary wood products.
Values represent the total monetary value of imports and exports aggregated
at the country–year level.

| Column                          | Description |
|---------------------------------|-------------|
| secondary_wood_trade_export     | Total value of exports of secondary wood products |
| secondary_wood_trade_import     | Total value of imports of secondary wood products |


---

### Secondary paper products  
(Unit of measure: Thousand EUR)

This table describes international trade in secondary paper products.
Only trade values are included, as production values for secondary paper
products are not consistently available and would duplicate information
already captured in other production tables.

| Column                               | Description |
|--------------------------------------|-------------|
| secondary_paper_products_export      | Total value of exports of secondary paper products |
| secondary_paper_products_import      | Total value of imports of secondary paper products |


---

### Secondary wood products - production  
(Unit of measure: Thousand cubic metres)

This table represents the production of selected secondary wood products.
Only engineered wood products classified under **GLT_CLT** are included,
as other product groups either duplicate this information or do not provide
values in cubic metres.

| Column                              | Description |
|-------------------------------------|-------------|
| secondary_wood_products_production  | Production volume of secondary wood products (GLT/CLT combined) |


---

### Pulp, paper and paperboard  
(Unit of measure: Thousand tonnes)

This table represents the production of pulp, paper, and paperboard products.
All indicators are expressed in **thousand tonnes**, as no alternative physical
units are consistently available for these products.

| Column                              | Description |
|-------------------------------------|-------------|
| wood_pulp_production                | Production of wood pulp |
| other_wood_pulp_production          | Production of other wood pulp |
| recovered_paper_production          | Production of recovered paper |
| paper_paperboard_production         | Production of paper and paperboard |

---

### Economic aggregates of forestry  
(Unit of measure: Million EUR, current prices)

This table provides key macroeconomic indicators describing the economic
performance of the forestry and logging sector. The indicators follow the
concepts and definitions of the European Forest Accounts (EFA) and National
Accounts.

| Column                              | Description |
|-------------------------------------|-------------|
| output_of_forestry_mil_euro          | Total output of forestry and connected secondary activities |
| value_added_forestry_mil_euro        | Gross value added (GVA) of the forestry and logging sector |

---

### Annual work units in forestry and logging  
(Unit of measure: AWU; derived indicators in EUR per AWU)

This table describes labour input in the forestry and logging sector using
**Annual Work Units (AWU)**, where 1 AWU corresponds to one full-time equivalent
working year.

In addition to total labour input, productivity indicators are derived by
relating economic output to labour input.

| Column         | Description |
|----------------|-------------|
| awu_total      | Total annual work units in forestry and logging |
| output_per_awu | Output of forestry per annual work unit (P1 / AWU, million EUR per AWU) |
| gva_per_awu    | Gross value added per annual work unit (B1G / AWU, million EUR per AWU) |

---

### Employed persons in forestry and forest-based industry  
(Unit of measure: Thousand persons; selected indicators as ratios)

This table describes employment structure in forestry and forest-based industries,
based on Eurostat Labour Force Survey (LFS, NACE Rev. 2).

In addition to sectoral employment levels, an education structure indicator is
derived to capture human capital intensity.

| Column                                   | Description |
|------------------------------------------|-------------|
| high_education_emp/all_emp_share          | Share of employed persons with tertiary education (ISCED 2011 levels 5–8) relative to total employment |
| employment_forestry_logging               | Employment in forestry and logging (thousand persons) |
| employment_manufacturing_wood_products    | Employment in manufacture of wood and wood products (thousand persons) |
| employment_manufacturing_paper_products   | Employment in manufacture of paper and paper products (thousand persons) |
| employment_manufacturing_furniture        | Employment in manufacture of furniture (thousand persons) |

---

### Generation of waste by waste category, hazardousness and NACE Rev. 2 activity  
(Unit of measure: Tonnes; reference year: 2022)

This table describes waste generation related to forestry and forest-based activities,
based on Eurostat environmental statistics.

Only waste generated in **agriculture, forestry and fishing** is considered.
Both **hazardous and non-hazardous waste** are aggregated into total waste quantities.

Due to limited data availability in kilograms per capita (non-zero values reported
for only a small number of countries), waste quantities are expressed in **tonnes**.
Data are available only for even years; therefore, **2022** is used as the reference year.

| Column                      | Description |
|-----------------------------|-------------|
| generation_of_waste_paper   | Total generation of paper-related waste (W072), hazardous and non-hazardous combined, in tonnes |
| generation_of_waste_wood    | Total generation of wood-related waste (W075), hazardous and non-hazardous combined, in tonnes |

---

### Treatment of waste by waste category, hazardousness and waste management operations  
(Unit of measure: Tonnes; reference year: 2022)

This table describes the treatment of waste related to forestry and forest-based activities,
based on Eurostat waste management statistics.

Both **hazardous and non-hazardous waste** are aggregated into total treated waste quantities.
Waste treatment refers to all waste management operations (e.g. recycling, recovery,
incineration, disposal).

Due to the absence of consistent data in kilograms per capita, waste treatment is expressed
in **tonnes**. Data are available only for even years; therefore, **2022** is used as the
reference year.


| Column                   | Description |
|--------------------------|-------------|
| treatment_of_waste_paper | Total treated paper-related waste (W072), hazardous and non-hazardous combined, in tonnes |
| treatment_of_waste_wood  | Total treated wood-related waste (W075), hazardous and non-hazardous combined, in tonnes |




































