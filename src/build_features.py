import pandas as pd
from sqlalchemy import create_engine
import features as ct
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

# Finalna tablica u koju ću pokušati spojiti sve podatke
final_df = pd.read_sql("SELECT * FROM final_table", engine)

# Dupliram redove u final_df kako bi svaka država imala po dvije godine
def double_dataframe(original_df):
    original_df = original_df.loc[final_df.index.repeat(2)].reset_index(drop=True)
    return original_df

# Dodajem godine 2021, 2022 uz svaku državu
def add_years(original_df):
    years = [2021, 2022] * (len(original_df) // 2)
    original_df["year"] = years
    return original_df



final_df = double_dataframe(final_df)
final_df = add_years(final_df)
#pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
#pd.set_option("display.width", None)
print(final_df)

#Tablice

final_df = ct.add_config_bark_features(final_df, pd.read_sql("SELECT * FROM roundwood_removals_by_type", engine))

#Gotova tablica roundwood_removals_by_type

#----------------------------

final_df = ct.add_roundwood_by_ownership_features(final_df, pd.read_sql("SELECT * FROM roundwood_by_ownership", engine))

#Gotova tablica roundwood_by_ownership

#----------------------------

#Tablicu industrial_roundwood_by_assortment prekacemo

final_df = ct.add_industrial_roundwood_by_species_features(final_df, pd.read_sql("SELECT * FROM industrial_roundwood_by_species", engine))

#Gotova tablica industrial_roundwood_by_species

#----------------------------

final_df = ct.add_sawnwood_trade_species_features(final_df, pd.read_sql("SELECT * FROM sawnwood_trade_species", engine))

#Gotova tablica sawnwood_trade_species

#----------------------------

#Ubacivanje iz tablice roundwood_fuelwood_basic

#roundwood_fuelwood_basic_roundwood_imp_exp
final_df = ct.roundwood_fuelwood_basic_imp_exp_features(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), {"IMP": "import", "EXP": "export"})


#roundwood_fuelwood_basic_roundwood
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["RW"], "THS_M3", {"RW": "roundwood", "PRD": "production"})
#roundwood_fuelwood_basic_fuelwood
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["RW_FW"], "THS_M3", {"RW_FW": "fuelwood", "PRD": "production"})
#roundwood_fuelwood_basic_industrial_roundwood_conif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["CONIF"], ["RW_IN"], "THS_M3", {"RW_IN": "industrial_roundwood_con", "PRD": "production"})
#roundwood_fuelwood_basic_industrial_roundwood_nconif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["NCONIF", "NC_TRO"], ["RW_IN"], "THS_M3", {"RW_IN": "industrial_roundwood_ncon", "PRD": "production"})
#roundwood_fuelwood_basic_wood_charcoal, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["CHA"], "THS_T", {"CHA": "wood_charcoal", "PRD": "production"})
#roundwood_fuelwood_basic_chp_res
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["CHP_RES"], "THS_M3", {"CHP_RES": "chp_res", "PRD": "production"})
#roundwood_fuelwood_basic_chp
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["CHP"], "THS_M3", {"CHP": "chp", "PRD": "production"})
#roundwood_fuelwood_basic_res_&_res_swd_combined
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["RES", "RES_SWD"], "THS_M3", {"RES": "res_swd", "RES_SWD": "res_swd", "PRD": "production"})
#roundwood_fuelwood_basic_pellet_agg, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["PEL_AGG"], "THS_T", {"PEL_AGG": "pellet_agg", "PRD": "production"})
#roundwood_fuelwood_basic_pellet, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM roundwood_fuelwood_basic", engine), ["TOTAL"], ["PEL"], "THS_T", {"PEL": "pellet", "PRD": "production"})

#Gotova tablica roundwood_fuelwood_basic

#----------------------------

#Ubacivanje iz tablice sawnwood_panels 
#!!! FUNKCIJA JE ISTA KAO I FUNKCIJA ZA roundwood_fuelwood_basic SAMO ŠTO SE OVOM PUTU BIRAJU DRUGI PARAMETRI

#sawnwood_panels_sawnwood_conif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["CONIF"], ["SN"], "THS_M3", {"SN": "sawnwood_con", "PRD": "production"})
#sawnwood_panels_sawnwood_nconif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["NCONIF", "NC_TRO"], ["SN"], "THS_M3", {"SN": "sawnwood_ncon", "PRD": "production"})
#sawnwood_panels_wood-based_panels
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["TOTAL"], ["PN"], "THS_M3", {"PN": "wood-based_panels", "PRD": "production"})
#sawnwood_panels_veneer_sheets_conif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["CONIF"], ["PN_VN"], "THS_M3", {"PN_VN": "veneer_sheets_con", "PRD": "production"})
#sawnwood_panels_veneer_sheets_nconif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["NCONIF", "NC_TRO"], ["PN_VN"], "THS_M3", {"PN_VN": "veneer_sheets_ncon", "PRD": "production"})
#sawnwood_panels_plywood_conif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["CONIF"], ["PN_PY"], "THS_M3", {"PN_PY": "plywood_con", "PRD": "production"})
#sawnwood_panels_plywood_nconif
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["NCONIF", "NC_TRO"], ["PN_PY"], "THS_M3", {"PN_PY": "plywood_ncon", "PRD": "production"})
#sawnwood_panels_particleboard
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["TOTAL"], ["PN_PB"], "THS_M3", {"PN_PB": "pn_pb", "PRD": "production"})
#sawnwood_panels_fiberboard
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["TOTAL"], ["PN_FB"], "THS_M3", {"PN_FB": "fibreboard", "PRD": "production"})
#sawnwood_panels_hardboard
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["TOTAL"], ["PN_FB_HB"], "THS_M3", {"PN_FB_HB": "hardboard", "PRD": "production"})
#sawnwood_panels_medium_density_fiberboard
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["TOTAL"], ["PN_FB_MDF"], "THS_M3", {"PN_FB_MDF": "medium_density_fiberboard", "PRD": "production"})
#sawnwood_panels_other_fiberboard
final_df = ct.basic_function(final_df, pd.read_sql("SELECT * FROM sawnwood_panels", engine), ["TOTAL"], ["PN_FB_O"], "THS_M3", {"PN_FB_O": "other_fiberboard", "PRD": "production"})

#Gotova tablica sawnwood_panels

#----------------------------

final_df = ct.secondary_wood_trade_add_features(final_df, pd.read_sql("SELECT * FROM secondary_wood_trade", engine), {"IMP": "import", "EXP": "export"})

#Gotova tablica secondary_wood_trade

#----------------------------

final_df = ct.secondary_paper_products_features(final_df, pd.read_sql("SELECT * FROM secondary_paper_products", engine), mapa = {"IMP": "import", "IMP_XEU": "import","EXP": "export","EXP_XEU": "export"})

#Ubacivanje iz tablice pulp_paper_paperboard

#pulp_paper_paperboard_wood_pulp, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function_without_treespec(final_df, pd.read_sql("SELECT * FROM pulp_paper_paperboard", engine), ["PL"], "THS_T", {"PL": "wood_pulp", "PRD": "production"})
#pulp_paper_paperboard_other_wood_pulp, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function_without_treespec(final_df, pd.read_sql("SELECT * FROM pulp_paper_paperboard", engine), ["PLO"], "THS_T", {"PLO": "other_wood_pulp", "PRD": "production"})
#pulp_paper_paperboard_recovered_paper, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function_without_treespec(final_df, pd.read_sql("SELECT * FROM pulp_paper_paperboard", engine), ["RCP"], "THS_T", {"RCP": "recovered_paper", "PRD": "production"})
#pulp_paper_paperboard_paper_paperboard, !!! druga mjerna jedinica (THS_T)
final_df = ct.basic_function_without_treespec(final_df, pd.read_sql("SELECT * FROM pulp_paper_paperboard", engine), ["PP"], "THS_T", {"PP": "paper_paperboard", "PRD": "production"})

#Gotova tablica pulp_paper_paperboard

#----------------------------

final_df = ct.economic_aggregates_of_forestry(final_df, pd.read_sql("SELECT * FROM economic_aggregates_of_forestry", engine), {"P1" : "output_of_forestry_mil_euro", "B1G" : "value_added_forestry_mil_euro"})

#Gotova tablica economic_aggregates_of_forestry

#----------------------------

final_df = ct.add_awu_forestry_logging_features(final_df, pd.read_sql("SELECT * FROM awu_forestry_logging", engine))

#Gotova tablica awu_forestry_logging

#----------------------------


print("----------------------------\n")

print("----------------------------\n")
# pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)
print(final_df)
final_df.to_csv("../data/processed/final_eurostat_features.csv", index=False)