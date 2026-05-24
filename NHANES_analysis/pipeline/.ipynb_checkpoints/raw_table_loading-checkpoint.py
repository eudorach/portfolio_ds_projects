TABLE_NAME_MAP = {
    "P_SSAGP":   "raw_blood_agp",
    "P_CBC":     "raw_blood_cbc",
    "P_CRCO":    "raw_blood_chromium_cobalt",
    "P_BIOPRO":  "raw_blood_cmp",
    "P_CMV":     "raw_blood_cmv",
    "P_COT":     "raw_blood_cotinine",
    "P_HSCRP":   "raw_blood_crp",
    "P_ETHOX":   "raw_blood_ethylene_oxide",
    "P_GLU":     "raw_blood_fasting_glucose",
    "P_FERTIN":  "raw_blood_ferritin",
    "P_FOLATE":  "raw_blood_folate",
    "P_FOLFMS":  "raw_blood_folate_forms",
    "P_GHB":     "raw_blood_glycohemoglobin",
    "P_HDL":     "raw_blood_hdl",
    "P_INS":     "raw_blood_insulin",
    "P_FETIB":   "raw_blood_iron_status",
    "P_IHGEM":   "raw_blood_mercury",
    "P_PBCD":    "raw_blood_pbcd",
    "P_PFAS":    "raw_blood_pfas",
    "P_TST":     "raw_blood_sex_hormones",
    "P_TCHOL":   "raw_blood_total_cholesterol",
    "P_TFR":     "raw_blood_transferrin",
    "P_TRIGLY":  "raw_blood_triglyceride",
    "P_VOCWB":   "raw_blood_voc",
    "P_UCM":     "raw_urine_chromium",
    "P_FR":      "raw_urine_flame_retardants",
    "P_SSFR":    "raw_urine_flame_retardants_surplus",
    "P_UAS":     "raw_speciated_arsenic",
    "P_UTAS":    "raw_total_arsenic",
    "P_ALB_CR":  "raw_urine_albcr",
    "P_OPD":     "raw_urine_insecticide",
    "P_UIO":     "raw_urine_iodine",
    "P_UHG":     "raw_urine_mercury",
    "P_UM":      "raw_urine_metals",
    "P_UNI":     "raw_urine_nickel",
    "P_PERNT":   "raw_urine_perc_nit_thio",
    "P_UCPREG":  "raw_urine_pregnancy",
    "P_UVOC":    "raw_urine_voc",
    "P_UVOC2":   "raw_urine_voc_2",
    "P_BMX": "raw_bmx",
    "BPOscillometric_P_BPXO.xpt": "raw_blood_pressure",
    "P_DEMO": "raw_demographics"
}


import os
from nhanes_utils import (
    save_to_postgres,
    load_xpt)

def ingest_folder(folder_path, engine, name_map):
    for file in os.listdir(folder_path):
        if file.endswith(".xpt"):
            
            base = file.replace(".XPT", "").replace(".xpt", "")
            
            table_name = name_map.get(base, f"raw_{base.lower()}")
            
            df = load_xpt(os.path.join(folder_path, file))
            save_to_postgres(df, table_name, engine)
            
            print(f"Loaded {file} -> {table_name}")