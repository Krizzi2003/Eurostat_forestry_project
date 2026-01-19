import eurostat
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Radim direktorij u koliko ne postoji
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def download_one(dataset_cfg):
    dataset_id = dataset_cfg["id"]
    name = dataset_cfg["name"]

  
    df = eurostat.get_data_df(dataset_id)

    # Brisem stupce u slijedećim tablicama za vrstu otpada koja nije papir ili drvo
    if name in ['waste_treatment', 'waste_generation']:
         if "waste" in df.columns:
             df = df[df["waste"].isin(["W075", "W072"])]
             print(f"Filtrirano za waste codes W075 i W072 u tablici {name}.")

         else:
             print(f"Upozorenje: stupac 'waste' nije pronađen u tablici {name}.")             

    # Spremi CSV
    out_path = DATA_DIR / f"{name}.csv"
    df.to_csv(out_path, index=False)
    print(f"Skinuto i spremljeno uspjesno: {dataset_id} -> {out_path}")
    df.to_sql(name, engine, if_exists='replace', index=False)
    print(f"Uspješno stvorena tablica u bazi podataka : {name}")

DATASETS = [
    {"id": "for_remov",    "name": "roundwood_removals_by_type"},
    {"id": "for_owner",    "name": "roundwood_by_ownership"},
    {"id": "for_basic",    "name": "roundwood_fuelwood_basic"},
    {"id": "for_irass",    "name": "industrial_roundwood_by_assortment"},
    {"id": "for_irspec",   "name": "industrial_roundwood_by_species"},
    {"id": "for_swpan",    "name": "sawnwood_panels"},
    {"id": "for_swspec",   "name": "sawnwood_trade_species"},
    {"id": "for_pp",       "name": "pulp_paper_paperboard"},
    {"id": "for_secwp",    "name": "secondary_wood_trade"},
    {"id": "for_secpp",    "name": "secondary_paper_products"},
    {"id": "for_secwpp",   "name": "secondary_wood_production"},
    {"id": "for_eco_cp",   "name": "economic_aggregates_of_forestry"},
    {"id": "for_sup_cp",   "name": "supply_and_use_of_products_within_forestry"},
    {"id": "for_emsuw",    "name": "monetary_supply_and_use_of_wood_in_the_rough"},
    {"id": "for_epsuw",    "name": "physical_supply_and_use_of_wood_in_the_rough_over_bark"},
    {"id": "for_eoutput",  "name": "output_of_forestry_by_type"},
    {"id": "for_awu",      "name": "awu_forestry_logging"},
    {"id": "for_emp_lfs",  "name": "employment_lfs_rev2"},
    {"id": "for_emp_lfs1", "name": "employment_lfs_rev1_1"},
    {"id": "env_trdrrm",   "name": "material_flows_resource_productivity"},
    {"id": "env_wasgen",   "name": "waste_generation"},
    {"id": "env_wastrt",   "name": "waste_treatment"},
]

def main():
    for dataset in DATASETS:
        try:
            download_one(dataset)
        except Exception as e:
            print(f"Problem s {dataset['id']}: {e}")

if __name__ == "__main__":
    main()







