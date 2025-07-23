# NHANES Obesity and Biomarkers Study

## Overview
This project uses NHANES 2017–2020 datasets to explore relationships between biomarkers (primarily from blood and urine lab results) and obesity. The final goal is to clean and organize this data into a relational database for predictive modeling and analysis.

---

## Data Sources
- NHANES 2017–2020: [https://wwwn.cdc.gov/nchs/nhanes/](https://wwwn.cdc.gov/nchs/nhanes/)

## Data Cleaning
The NHANES data consists of multiple datasets grouped into distinct categories. For this project, I categorized them into:

- Demographics
- Body Measurements
- Urine Lab Values
- Blood Lab Values

To improve efficiency and ensure reproducibility, I cleaned each category in a separate Jupyter notebook. This modular approach also improves readability and makes it easier to track preprocessing steps for each dataset type.

## Variable Key (Column Renaming)

This section documents the renaming of original NHANES column codes to more intuitive names, organized by dataset type. All column names are updated during initial data cleaning for clarity and consistency across merged datasets.

---

### Demographics
| Original Column | New Column Name | Description |
|-----------------|-----------------|-------------|
| `SEQN`          | `participant_id`| Unique NHANES participant ID |
| `RIAGENDR`      | `gender`        | 1 = Male, 2 = Female |
| `RIDAGEYR`      | `age_year`      | Age in years |
| `RIDRETH3`      | `race`          | Hispanic and Non-Hispanic races (see Encoded Values) |
| `DMDEDUC2`      | `education_level` | Education level up to college or above (see Encoded Values) |
| `DMDMARTZ` | `marital_status` | Marital status (see Encoded Values) |
| `INDFMPIR` | `family_income_poverty` | Ratio of family income to poverty |

### Body Measures
The body measures were done on both males and females and ages 0 - 150 years unless specified. 

| Original Column | New Column Name | Description |
|---|---|---|
|  `BMXWT` | `weight_kg` | Body weight in kgs |
| `BMIWT` | `weight_comment` | Comment code for body weight |
| `BMXRECUM` | `recumbent_length_cm` | Height measures in cm, age 0-47 months |
| `BMXHT` | `standing_height` | Standing height in cm |
| `BMIHT` | `standing_height_comment` | Comment code for standing height (see Encoded Values) |
| `BMXBMI` | `bmi` | Body mass index in kg/m**2 |
| `BMDBMIC` | `bmi_category_child` | BMI Category (see Encoded Values) |
| `BMXLEG` | `upper_leg_cm` | Upper leg length in cm, age 8 - 150 years |
| `BMXARML` | `upper_arm_cm` | Upper arm length in cm, age 8 - 150 years |
| `BMXARMC` | `arm_circumference_cm` | Arm circumference in cm, age 2 months - 150 years |
| `BMXWAIST` | `waist_circ_cm` | Waist circumference in cm, age 2-150 years |
| `BMXHIP` | `hip_circ_cm` | Hip circumference in cm, age 12-150 years | 

### 💧 Urine Lab Datasets

| Dataset File | Original Column | New Column Name           | Description                          |
|--------------|-----------------|---------------------------|--------------------------------------|
| 1.P_ALB_CR.XPT   | `URXUMA`   | `albumin_urine_ug_mL`       | Urinary albumin (µg/mL)              |
| 1.P_ALB_CR.XPT   | `URXUMS`   | `albumin_urine_mg_L`        | Urinary albumin (mg/L)               |
| 1.P_ALB_CR.XPT   | `URDUMALC` | `alb_comment`               | Comment code for albumin (see Encoded Values |
| 1.P_ALB_CR.XPT   | `URXUCR`   | `creatinine_urine_mg_dL`    | Urinary creatinine (mg/dL)           |
| 1.P_ALB_CR.XPT   | `URXCRS`   | `creatinine_urine_umol_L`   | Urinary creatinine (µmol/L)          |
| 1.P_ALB_CR.XPT   | `URDUCRLC` | `creatinine_comment`        | Comment code for urinary creatinine (see Encoded Values |
| 1.P_ALB_CR.XPT   | `URDACT`   | `alb_creat_ratio`         | Albumin-to-creatinine ratio          |
| 2.P_UTAS.XPT     | `URXUAS`   | `total_arsenic_ug_L` | Total arsenic (ug/L) |
| 2.P_UTAS.XPT     | `URDUASLC` | `total_arsenic_comment` | Total arsenic comment (see Encoded Values) |
| 3.P_UAS.XPT      | `URXUAS3`  | `arsenous_acid_ug_L`              | Arsenous acid concentration (µg/L)              |
| 3.P_UAS.XPT      | `URDUA3LC` | `arsenous_acid_comment`           | Comment code for arsenous acid result           |
| 3.P_UAS.XPT      | `URXUAS5`  | `arsenic_acid_ug_L`               | Arsenic acid concentration (µg/L)               |
| 3.P_UAS.XPT      | `URDUA5LC` | `arsenic_acid_comment`            | Comment code for arsenic acid result            |
| 3.P_UAS.XPT      | `URXUAB`   | `arsenobetaine_ug_L`              | Arsenobetaine concentration (µg/L)              |
| 3.P_UAS.XPT      | `URDUABLC` | `arsenobetaine_comment`           | Comment code for arsenobetaine result           |
| 3.P_UAS.XPT      | `URXUAC`   | `arsenocholine_ug_L`              | Arsenocholine concentration (µg/L)              |
| 3.P_UAS.XPT      | `URDUACLC` | `arsenocholine_comment`           | Comment code for arsenocholine result           |
| 3.P_UAS.XPT      | `URXUDMA`  | `dimethylarsinic_acid_ug_L`       | Dimethylarsinic acid concentration (µg/L)       |
| 3.P_UAS.XPT      | `URDUDALC` | `dimethylarsinic_comment`         | Comment code for dimethylarsinic acid result    |
| 3.P_UAS.XPT      | `URXUMMA`  | `monomethylarsonic_acid_ug_L`     | Monomethylarsonic acid concentration (µg/L)     |
| 3.P_UAS.XPT      | `URDUMMAL` | `monometylarsonic_comment`        | Comment code for monomethylarsonic acid result  |
| 4.P_UCM.XPT      | `URXUCM`   | `chromium_ug_L`     | Chromium concentration in urine (µg/L) |
| 4.P_UCM.XPT      | `URDUCMLC` | `chromium_comment`  | Comment code for chromium measurement  |
| 5.P_FR.XPT       | `URXBCPP`  | `1_chloro_2_propyl_phosphate`      | 1-Chloro-2-propyl phosphate (µg/L)            |
| 5.P_FR.XPT       | `URDBCPLC` | `1ch_2pro_comment`     | Comment code for 1-Chloro-2-propyl phosphate             |
| 5.P_FR.XPT       | `URXBCEP`  | `bis_1_chloroethyl_phosphate`   | Bis(1-chloroethyl) phosphate (µg/L)                      |
| 5.P_FR.XPT       | `URDCEPLC` | `bis_1_chlo_phos_comment`   | Comment code for Bis(1-chloroethyl) phosphate            |
| 5.P_FR.XPT       | `URXBDCP`  | `1_3_dichloro_2_propyl_phosphate`  | 1,3-Dichloro-2-propyl phosphate (µg/L)            |
| 5.P_FR.XPT       | `URDBDCLC` | `1_3_di_2_pro_comment`     | Comment code for 1,3-Dichloro-2-propyl phosphate         |
| 5.P_FR.XPT       | `URXDBUP`  | `dibutyl_phosphate`        | Dibutyl phosphate (µg/L)                                 |
| 5.P_FR.XPT       | `URDDUPLC` | `dibutyl_phos_comment`     | Comment code for Dibutyl phosphate                      |
| 5.P_FR.XPT       | `URXDPHP`  | `diphenyl_phosphate`        | Diphenyl phosphate (µg/L)                                |
| 5.P_FR.XPT       | `URDDPHLC` | `diphe_phos_comment`          | Comment code for Diphenyl phosphate                     |
| 5.P_FR.XPT       | `URXTBBA`  | `2_3_4_5_tetrabromobenzoic_acid`       | 2,3,4,5-Tetrabromobenzoic acid (µg/L)         |
| 5.P_FR.XPT       | `URDBBALC` | `2_3_4_5_tet_comment`         | Comment code for 2,3,4,5-Tetrabromobenzoic acid        |
| 6.P_SSFR.XPT     | `SSIPPP`   | `2_isopropylphenyl_phenyl_phosphate` | 2-isopropylphenyl-phenyl phosphate (µg/L) |
| 6.P_SSFR.XPT     | `SSIPPPL`  | `2_isopropylphenyl_phenyl_phosphate_comment` |2-isopropylphenyl-phenyl phosphate comment|
| 6.P_SSFR.XPT     | `SSBPPP`   | `4_tert_butylphenyl_phenyl_phosphate` | 4-tert-butylphenyl phenyl phosphate (µg/L) |
| 6.P_SSFR.XPT     | `SSBPPPL`  | `4_tert_butylphenyl_phenyl_phosphate_comment`| 4-tert-butylphenyl phenyl phosphate comment|
| 7.P_UIO.XPT      | `URXUIO`   | `urine_iodine` | Urine iodine (µg/L) |
| 7.P_UIO.XPT      | `URDUIOLC` | `urine_iodine_comment` | Urine iodine comment |
| 8.P_UHG.XPT      | `URXUHG`   | `urine_mercury` | Urine mercury level (µg/L) |
| 8.P_UHG.XPT      | `URDUHGLC` | `urine_mercury_comment` | Urine mercury comment |
| 9.P_UM.XPT          | `URXUBA`   | `urine_barium` | Urine barium level ((µg/L) |
| 9.P_UM.XPT           | `URDUBALC`  | `barium_comment` | Comment code for urine barium |
| 9.P_UM.XPT           | `URXUCD`    | `urine_cadmium` | Urine cadmium level (µg/L) |
| 9.P_UM.XPT           | `URDUCDLC`  | `cadmium_comment` | Comment code for cadmiumn |
| 9.P_UM.XPT           | `URXUCO`    | `urine_cobalt` | Urine cobalt (µg/L) | 
| 9.P_UM.XPT           | `URDUCOLC` | `cobalt_comment` | Comment code for urine cobalt |
| 9.P_UM.XPT           | `URXUCS` | `urine_cesium` | Urine cesium level (µg/L) |
| 9.P_UM.XPT           | `URDUCSLC` | `cesium_comment` | Comment code for urine cesium |
| 9.P_UM.XPT           | `URXUMO` | `urine_molybdenum` | Urine molybdenum level (µg/L) |
| 9.P_UM.XPT           | `URDUMOLC` | `molybdenum_comment` | Comment code for urine molybdenum |
| 9.P_UM.XPT           | `URXUMN` | `urine_manganese` | Urine manganese level (µg/L) |
| 9.P_UM.XPT           | `URDUMNLC` | `manganese_comment` | Comment code for urine manganese |
| 9.P_UM.XPT           | `URXUPB` | `urine_lead` | Urine lead level (µg/L) |
| 9.P_UM.XPT           | `URDUPBLC` | `lead_comment` | Comment code for urine lead |
| 9.P_UM.XPT          | `URXUSB` | `urine_antimony` | Urine antimony level (µg/L) |
| 9.P_UM.XPT           | `URDUSBLC` | `antimony_comment` | Comment code for urine antimony |
| 9.P_UM.XPT           | `URXUSN` | `urine_tin` | Urine tin level (µg/L) |
| 9.P_UM.XPT           | `URDUSNLC` | `tin_comment` | Comment code for urine tin |
| 9.P_UM.XPT           | `URXUTL` | `urine_thallium` | Urine thallium level (µg/L) |
| 9.P_UM.XPT           | `URDUTLLC` | `thallium_comment` | Comment code for urine thallium |
| 9.P_UM.XPT           | `URXUTU` | `urine_tungsten` | Urine tungsten level (µg/L) |
| 9.P_UM.XPT           | `URDUTULC` | `tungsten_comment` | Comment code for urine tungsten |
| 10.P_UNI.XPT         | `URXUNI`         | `urine_nickel`            | Urine nickel level (µg/L)                 |
| 10.P_UNI.XPT         | `URDUNILC`       | `urine_nickel_comment`    | Comment code for urine nickel             |
| 11.P_OPD.XPT      | `URXOP1`         | `dimethylphosphate_ng_mL`         | Urine dimethylphosphate level (ng/mL)           |
| 11.P_OPD.XPT      | `URDOP1LC`       | `dimethylphosphate_comment`       | Comment code for dimethylphosphate              |
| 11.P_OPD.XPT      | `URXOP2`         | `diethylphosphate_ng_mL`          | Urine diethylphosphate level (ng/mL)            |
| 11.P_OPD.XPT      | `URDOP2LC`       | `diethylphosphate_comment`        | Comment code for diethylphosphate               |
| 11.P_OPD.XPT      | `URXOP3`         | `dimethylthiophosphate_ng_mL`     | Urine dimethylthiophosphate level (ng/mL)       |
| 11.P_OPD.XPT      | `URDOP3LC`       | `dimethylthiophosphate_comment`   | Comment code for dimethylthiophosphate          |
| 11.P_OPD.XPT      | `URXOP4`         | `diethylthiophosphate_ng_mL`      | Urine diethylthiophosphate level (ng/mL)        |
| 11.P_OPD.XPT      | `URDOP4LC`       | `diethylthiophosphate_comment`    | Comment code for diethylthiophosphate           |
| 11.P_OPD.XPT      | `URXOP5`         | `dimethyldithiophosphate_ng_mL`   | Urine dimethyldithiophosphate level (ng/mL)     |
| 11.P_OPD.XPT      | `URDOP5LC`       | `dimethyldithiophosphate_comment` | Comment code for dimethyldithiophosphate        |
| 11.P_OPD.XPT      | `URXOP6`         | `diethyldithiophosphate_ng_mL`    | Urine diethyldithiophosphate level (ng/mL)      |
| 11.P_OPD.XPT      | `URDOP6LC`       | `diethyldithiophosphate_comment`  | Comment code for diethyldithiophosphate         |
| 12.P_PERNT.XPT  | `URXUP8`         | `perchlorate_urine_ng_mL`    | Urine perchlorate level (ng/mL)             |
| 12.P_PERNT.XPT  | `URDUP8LC`       | `perchlorate_comment`        | Comment code for urine perchlorate          |
| 12.P_PERNT.XPT  | `URXNO3`         | `nitrate_urine_ng_mL`        | Urine nitrate level (ng/mL)                 |
| 12.P_PERNT.XPT  | `URDNO3LC`       | `nitrate_comment`            | Comment code for urine nitrate              |
| 12.P_PERNT.XPT  | `URXSCN`         | `thiocyanate_urine_ng_mL`    | Urine thiocyanate level (ng/mL)             |
| 12.P_PERNT.XPT  | `URDSCNLC`       | `thiocyanate_comment`        | Comment code for urine thiocyanate          |
| 13.P_UCPREG.XPT  | `URXPREG`        | `pregnancy_test_result`    | Urine pregnancy test result (See Encoded Values)     |
| 14.P_UVOC.XPT | `URX2MH`    | `2_methylhippuric_acid_ng_ml`                     | 2-Methylhippuric acid (ng/mL) |
| 14.P_UVOC.XPT | `URD2MHLC`  | `2_methylhippuric_acid_comment`                   | Comment code for 2-Methylhippuric acid |
| 14.P_UVOC.XPT | `URX34M`    | `3__and_4_methylhippuric_acid_ng_ml`              | 3- and 4-Methylhippuric acid (ng/mL) |
| 14.P_UVOC.XPT | `URD34MLC`  | `3__and_4_methylhippuric_acid_comment`            | Comment code for 3- and 4-Methylhippuric acid |
| 14.P_UVOC.XPT | `URXAAM`    | `n_acetyl_s_2_carbamoylethyl_l_cysteine_ng_ml`    | N-Acetyl-S-(2-carbamoylethyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDAAMLC`  | `n_acetyl_s_2_carbamoylethyl_l_cysteine_comment`  | Comment code for N-Acetyl-S-(2-carbamoylethyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXAMC`    | `n_acetyl_s_n_methylcarbamoyl_l_cysteine_ng_ml`   | N-Acetyl-S-(N-methylcarbamoyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDAMCLC`  | `n_acetyl_s_n_methylcarbamoyl_l_cysteine_comment` | Comment code for N-Acetyl-S-(N-methylcarbamoyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXATC`    | `2_aminothiazoline_4_carboxylic_acid_ng_ml`       | 2-Aminothiazoline-4-carboxylic acid (ng/mL) |
| 14.P_UVOC.XPT | `URDATCLC`  | `2_aminothiazoline_4_carboxylic_acid_comment`     | Comment code for 2-Aminothiazoline-4-carboxylic acid |
| 14.P_UVOC.XPT | `URXBMA`    | `n_acetyl_s_benzyl_l_cysteine_ng_ml`              | N-Acetyl-S-benzyl-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDBMALC`  | `n_acetyl_s_benzyl_l_cysteine_comment`            | Comment code for N-Acetyl-S-benzyl-L-cysteine |
| 14.P_UVOC.XPT | `URXBPM`    | `n_acetyl_s_n_propyl_l_cysteine_ng_ml`            | N-Acetyl-S-n-propyl-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDBPMLC`  | `n_acetyl_s_n_propyl_l_cysteine_comment`          | Comment code for N-Acetyl-S-n-propyl-L-cysteine |
| 14.P_UVOC.XPT | `URXCEM`    | `n_acetyl_s_2_carboxyethyl_l_cysteine_ng_ml`      | N-Acetyl-S-(2-carboxyethyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDCEMLC`  | `n_acetyl_s_2_carboxyethyl_l_cysteine_comment`    | Comment code for N-Acetyl-S-(2-carboxyethyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXCYHA`   | `n_acetyl_s_1_cyano_2_hydroxyethyl_l_cysteine_ng_ml` | N-Acetyl-S-(1-cyano-2-hydroxyethyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDCYALC`  | `n_acetyl_s_1_cyano_2_hydroxyethyl_l_cysteine_comment` | Comment code for N-Acetyl-S-(1-cyano-2-hydroxyethyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXCYM`    | `n_acetyl_s_2_cyanoethyl_l_cysteine_ng_ml`        | N-Acetyl-S-(2-cyanoethyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDCYMLC`  | `n_acetyl_s_2_cyanoethyl_l_cysteine_comment`      | Comment code for N-Acetyl-S-(2-cyanoethyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXDHB`    | `n_acetyl_s_34_dihydroxybutyl_l_cysteine_ng_ml`   | N-Acetyl-S-(3,4-dihydroxybutyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDDHBLC`  | `n_acetyl_s_34_dihydroxybutyl_l_cysteine_comment` | Comment code for N-Acetyl-S-(3,4-dihydroxybutyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXGAM`    | `n_acetyl_s_2_carbamoyl_2_hydroxyethyl_l_cysteine_ng_ml` | N-Acetyl-S-(2-carbamoyl-2-hydroxyethyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDGAMLC`  | `n_acetyl_s_2_carbamoyl_2_hydroxyethyl_l_cysteine_comment` | Comment code for N-Acetyl-S-(2-carbamoyl-2-hydroxyethyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXHEM`    | `n_acetyl_s_2_hydroxyethyl_l_cysteine_ng_ml`      | N-Acetyl-S-(2-hydroxyethyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDHEMLC`  | `n_acetyl_s_2_hydroxyethyl_l_cysteine_comment`    | Comment code for N-Acetyl-S-(2-hydroxyethyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXHP2`    | `n_acetyl_s_2_hydroxypropyl_l_cysteine_ng_ml`     | N-Acetyl-S-(2-hydroxypropyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDHP2LC`  | `n_acetyl_s_2_hydroxypropyl_l_cysteine_comment`   | Comment code for N-Acetyl-S-(2-hydroxypropyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXHPM`    | `n_acetyl_s_3_hydroxypropyl_l_cysteine_ng_ml`     | N-Acetyl-S-(3-hydroxypropyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDHPMLC`  | `n_acetyl_s_3_hydroxypropyl_l_cysteine_comment`   | Comment code for N-Acetyl-S-(3-hydroxypropyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXIPM3`   | `n_acetyl_s_3_hydroxypropyl_1_methyl_l_cysteine_ng_ml` | N-Acetyl-S-(3-hydroxypropyl-1-methyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDPM3LC`  | `n_acetyl_s_3_hydroxypropyl_1_methyl_l_cysteine_comment` | Comment code for N-Acetyl-S-(3-hydroxypropyl-1-methyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXMAD`    | `mandelic_acid_ng_ml`                            | Mandelic acid (ng/mL) |
| 14.P_UVOC.XPT | `URDMADLC`  | `mandelic_acid_comment`                          | Comment code for Mandelic acid |
| 14.P_UVOC.XPT | `URXMB3`    | `n_acetyl_s_4_hydroxy_2_butenyl_l_cysteine_ng_ml` | N-Acetyl-S-(4-hydroxy-2-butenyl)-L-cysteine (ng/mL) |
| 14.P_UVOC.XPT | `URDMB3LC`  | `n_acetyl_s_4_hydroxy_2_butenyl_l_cysteine_comment` | Comment code for N-Acetyl-S-(4-hydroxy-2-butenyl)-L-cysteine |
| 14.P_UVOC.XPT | `URXPHG`    | `phenylglyoxylic_acid_ng_ml`                     | Phenylglyoxylic acid (ng/mL) |
| 14.P_UVOC.XPT | `URDPHGLC`  | `phenylglyoxylic_acid_comment`                   | Comment code for Phenylglyoxylic acid |
| 14.P_UVOC.XPT | `URXPMM`    | `2_thioxothiazolidine_4_carboxylic_acid`         | 2-Thioxothiazolidine-4-carboxylic acid (ng/mL) |
| 14.P_UVOC.XPT | `URDPMMLC`  | `2_thioxothiazolidine_4_carboxylic_acid_comment` | Comment code for 2-Thioxothiazolidine-4-carboxylic acid |
| 15.P_UVOC2.XPT | `URXMUCA`   | `trans_trans_muconic_acid_ng_ml`       | Trans,trans-Muconic acid (ng/mL) |
| 15.P_UVOC2.XPT | `URDMUCLC`  | `trans_trans_muconic_acid_comment`     | Comment code for Trans,trans-Muconic acid |
| 15.P_UVOC2.XPT | `URXPHMA`   | `phenylmercapturic_acid_ng_ml`         | Phenylmercapturic acid (ng/mL) |
| 15.P_UVOC2.XPT | `URDPMALC`  | `phenylmercapturic_acid_comment`       | Comment code for Phenylmercapturic acid |


Add more rows as additional urine datasets are cleaned.

---

### 🩸 Blood Lab Datasets

| Dataset File | Original Column | New Column Name           | Description                          |
|--------------|-----------------|---------------------------|--------------------------------------|
| 1.P_SSAGP.xpt | `SSAGP` | `alpha_1_agp_g_L` | Alpha-1-acid glycoprotein (g/L) |
| 2.P_HDL.xpt | `LBDHDD` | `direct_hdl_mg_dl` | Direct HDL cholesterol (mg/dL) |
| 2.P_HDL.xpt | `LBDHDDSI` | `direct_hdl_mmol_l` | Direct HDL cholesterol (mmol/L) |
| 3.P_TRIGLY.xpt | `LBXTR`     | `triglyceride_mg_dl`               | Triglycerides (mg/dL)                                |
| 3.P_TRIGLY.xpt | `LBDTRSI`   | `triglyceride_mmol_l`              | Triglycerides (mmol/L)                               |
| 3.P_TRIGLY.xpt | `LBDLDL`    | `ldl_friedewald_mg_dl`             | LDL cholesterol (Friedewald equation, mg/dL)         |
| 3.P_TRIGLY.xpt | `LBDLDLSI`  | `ldl_friedewald_mmol_l`            | LDL cholesterol (Friedewald equation, mmol/L)        |
| 3.P_TRIGLY.xpt | `LBDLDLM`   | `ldl_martin_hopkins_mg_dl`         | LDL cholesterol (Martin–Hopkins method, mg/dL)       |
| 3.P_TRIGLY.xpt | `LBDLDMSI`  | `ldl_martin_hopkins_mmol_l`        | LDL cholesterol (Martin–Hopkins method, mmol/L)      |
| 3.P_TRIGLY.xpt | `LBDLDLN`   | `ldl_nih_mg_dl`                    | LDL cholesterol (NIH equation, mg/dL)                |
| 3.P_TRIGLY.xpt | `LBDLDNSI`  | `ldl_nih_mmol_l`                   | LDL cholesterol (NIH equation, mmol/L)               |
| 4.P_TCHOL.xpt | `LBXTC`   | `total_cholesterol_mg_dl`   | Total cholesterol (mg/dL)         |
| 4.P_TCHOL.xpt | `LBDTCSI` | `total_cholesterol_mmol_l`  | Total cholesterol (mmol/L)        |
| 5.P_CRCO.xpt | `LBXBCR`     | `chromium_blood_ug_l`        | Chromium in blood (µg/L)           |
| 5.P_CRCO.xpt | `LBDBCRSI`   | `chromium_blood_nmol_l`      | Chromium in blood (nmol/L)         |
| 5.P_CRCO.xpt | `LBDBCRLC`   | `chromium_blood_comment`     | Comment code for chromium          |
| 5.P_CRCO.xpt | `LBXBCO`     | `cobalt_blood_ug_l`          | Cobalt in blood (µg/L)             |
| 5.P_CRCO.xpt | `LBDBCOSI`   | `cobalt_blood_nmol_l`        | Cobalt in blood (nmol/L)           |
| 5.P_CRCO.xpt | `LBDBCOLC`   | `cobalt_blood_comment`       | Comment code for cobalt            |
| 6.P_CBC.xpt | `LBXWBCSI`                | `white_blood_cell_count`                 | White blood cell count (1000 cells/µL)    |
| 6.P_CBC.xpt | `LBXLYPCT`                | `lymphocyte_percent`                     | Lymphocyte percentage                     |
| 6.P_CBC.xpt | `LBXMOPCT`                | `monocyte_percent`                       | Monocyte percentage                       |
| 6.P_CBC.xpt | `LBXNEPCT`                | `segmented_neutrophils_percent`          | Neutrophil percentage                     |
| 6.P_CBC.xpt | `LBXEOPCT`                | `eosinophils_percent`                    | Eosinophil percentage                     |
| 6.P_CBC.xpt | `LBXBAPCT`                | `basophils_percent`                      | Basophil percentage                       |
| 6.P_CBC.xpt | `LBXLYNUM`                | `lymphocyte_number`                      | Lymphocyte count (1000 cells/µL)          |
| 6.P_CBC.xpt | `LBXMONUM`                | `monocyte_number`                        | Monocyte count (1000 cells/µL)            |
| 6.P_CBC.xpt | `LBXNENUM`                | `segmented_neutrophils_number`           | Neutrophil count (1000 cells/µL)          |
| 6.P_CBC.xpt | `LBXEONUM`                | `eosinophils_number`                     | Eosinophil count (1000 cells/µL)          |
| 6.P_CBC.xpt | `LBXBANUM`                | `basophils_number`                       | Basophil count (1000 cells/µL)            |
| 6.P_CBC.xpt | `LBXRBCSI`                | `red_blood_cell_count`                   | Red blood cell count (million cells/µL)   |
| 6.P_CBC.xpt | `LBXHGB`                  | `hemoglobin`                             | Hemoglobin (g/dL)                         |
| 6.P_CBC.xpt | `LBXHCT`                  | `hematocrit_percent`                     | Hematocrit (%)                            |
| 6.P_CBC.xpt | `LBXMCVSI`                | `mean_cell_volume`                       | Mean cell volume (fL)                     |
| 6.P_CBC.xpt | `LBXMC`                   | `mean_cell_hgb_concentration`            | Mean cell hemoglobin concentration (g/dL) |
| 6.P_CBC.xpt | `LBXMH`                   | `mean_cell_hemoglobin`                   | Mean cell hemoglobin (pg)                 |
| 6.P_CBC.xpt | `LBXRDW`                  | `red_cell_distribution_width`            | Red cell distribution width (%)           |
| 6.P_CBC.xpt | `LBXPLTSI`                | `platelet_count`                         | Platelet count (1000 cells/µL)            |
| 6.P_CBC.xpt | `LBXMPVSI`                | `mean_platelet_volume`                   | Mean platelet volume (fL)                 |
| 6.P_CBC.xpt | `LBXNRSI`                 | `nucelated_red_blood_cells`              | Nucleated red blood cells (1000 cells/µL) |
| 7.P_COT.xpt | `LBXCOT`          | `serum_cotinine_ng_ml`      | Serum cotinine level (ng/mL)    |
| 7.P_COT.xpt | `LBDCOTLC`        | `serum_cotinine_comment`    | Comment code for serum cotinine |
| 7.P_COT.xpt | `LBXHCOT`         | `serum_hydroxycotinine_ng_ml` | Serum hydroxycotinine level (ng/mL) |
| 7.P_COT.xpt | `LBDHCOLC`        | `serum_hydroxycotinine_comment` | Comment code for serum hydroxycotinine |
| 8.P_CMV.xpt     | `LBXIGG`   | `cmv_igg`         | Cytomegalovirus (CMV) IgG antibody |
| 8.P_CMV.xpt     | `LBXIGM`   | `cmv_igm`         | Cytomegalovirus (CMV) IgM antibody |
| 8.P_CMV.xpt     | `LBXIGGA`  | `cmv_igg_avidity` | Cytomegalovirus (CMV) IgG avidity (See Encoded Values)|
| 9.P_ETHOX.xpt   | `LBXEOA`     | `eto_pmol_g_hb` | Ethylene oxide hemoglobin adduct level (pmol/g Hb) |
| 9.P_ETHOX.xpt   | `LBDEOALC`   | `eto_comment`   | Comment code for ethylene oxide measurement         |
| 10.P_FERTIN.xpt | `LBXFER`     | `ferritin_ng_ml` | Ferritin concentration (ng/mL)         |
| 10.P_FERTIN.xpt | `LBDFERSI`   | `ferritin_ug_l`   | Ferritin concentration (µg/L - SI units) |
| 11.P_FETIB.xpt | `LBXIRN`    | `iron_frozen_ug_dl`        | Iron concentration in frozen serum (µg/dL)       |
| 11.P_FETIB.xpt | `LBDIRNSI`  | `iron_frozen_umol_l`       | Iron concentration in frozen serum (µmol/L)      |
| 11.P_FETIB.xpt | `LBXUIB`    | `uibc_ug_dl`               | Unsaturated Iron Binding Capacity (µg/dL)        |
| 11.P_FETIB.xpt | `LBDUIBLC`  | `uibc_comment`             | Comment code for UIBC                            |
| 11.P_FETIB.xpt | `LBDUIBSI`  | `uibc_umol_l`              | Unsaturated Iron Binding Capacity (µmol/L)       |
| 11.P_FETIB.xpt | `LBDTIB`    | `tibc_ug_dl`               | Total Iron Binding Capacity (µg/dL)              |
| 11.P_FETIB.xpt | `LBDTIBSI`  | `tibc_umol_l`              | Total Iron Binding Capacity (µmol/L)             |
| 11.P_FETIB.xpt | `LBDPCT`    | `transferrin_saturation`   | Transferrin saturation percentage (%)            |
| 12.P_FOLATE.xpt | `LBDRFO`    | `rbc_folate_ng_ml`    | Red blood cell folate (ng/mL)        |
| 12.P_FOLATE.xpt | `LBDRFOSI`  | `rbc_folate_nmol_l`   | Red blood cell folate (nmol/L)       |
| 13.P_FOLFMS.xpt | `LBDFOTSI`  | `serum_total_folate_nmol_l`              | Serum total folate (nmol/L)              |
| 13.P_FOLFMS.xpt | `LBDFOTSI2` | `serum_total_folate_ng_ml`               | Serum total folate (ng/mL)               |
| 13.P_FOLFMS.xpt | `LBDFMTH`   | `5_methyl_tetrahydrofolate_nmol_l`       | 5-Methyltetrahydrofolate (nmol/L)        |
| 13.P_FOLFMS.xpt | `LBDCMTH`   | `5_methyl_tetrahydrofolate_cmt`          | Comment code for 5-Methyltetrahydrofolate |
| 13.P_FOLFMS.xpt | `LBDFACID`  | `folic_acid_nmol_l`                      | Folic acid (nmol/L)                      |
| 13.P_FOLFMS.xpt | `LBDCFACI`  | `folic_acid_cmt`                         | Comment code for folic acid              |
| 13.P_FOLFMS.xpt | `LBDFTHF`   | `5_formyl_tetrahydrofolate_nmol_l`       | 5-Formyltetrahydrofolate (nmol/L)        |
| 13.P_FOLFMS.xpt | `LBDCFTHF`  | `5_formyl_tetrahydrofolate_cmt`          | Comment code for 5-Formyltetrahydrofolate |
| 13.P_FOLFMS.xpt | `LBDTHF`    | `tetrahydrofolate_nmol_l`                | Tetrahydrofolate (nmol/L)                |
| 13.P_FOLFMS.xpt | `LBDCTHF`   | `tetrahydrofolate_cmt`                   | Comment code for tetrahydrofolate        |
| 13.P_FOLFMS.xpt | `LBDFMNL`   | `510_methenyl_tetrahydrofolate_nmol_l`   | 5,10-Methenyltetrahydrofolate (nmol/L)   |
| 13.P_FOLFMS.xpt | `LBDCMNL`   | `510_methenyl_tetrahydrofolate_cmt`      | Comment code for 5,10-Methenyltetrahydrofolate |
| 13.P_FOLFMS.xpt | `LBDFOXP`   | `mefox_oxidation_product_nmol_l`         | MeFox oxidation product (nmol/L)         |
| 13.P_FOLFMS.xpt | `LBDCOXP`   | `mefox_oxidation_product_cmt`            | Comment code for MeFox oxidation product |
| 14.P_GHB.xpt | `LBXGH` | `glycohemoglobin_percent` | Glycohemoglobin (%) |
| 15.P_HSCRP.xpt | `LBXHSCRP` | `hs_crp_mg_l`     | High-sensitivity C-reactive protein (mg/L) |
| 15.P_HSCRP.xpt | `LBDHRPLC` | `hs_crp_cmt`      | High-sensitivity CRP comment               |
| 16.P_IHGEM.xpt   | `LBXIHG`       | `mercury_inorganic_ug_l`         | Inorganic mercury (µg/L)                 |
| 16.P_IHGEM.xpt   | `LBDIHGSI`     | `mercury_inorganic_nmol_l`       | Inorganic mercury (nmol/L)               |
| 16.P_IHGEM.xpt   | `LBDIHGC`      | `mercury_inorganic_comment_code` | Inorganic mercury comment code           |
| 16.P_IHGEM.xpt   | `LBXEHG`       | `mercury_ethyl_ug_l`             | Ethyl mercury (µg/L)                     |
| 16.P_IHGEM.xpt   | `LBDEHGSI`     | `mercury_ethyl_nmol_l`           | Ethyl mercury (nmol/L)                   |
| 16.P_IHGEM.xpt   | `LBDEHGC`      | `mercury_ethyl_comment_code`     | Ethyl mercury comment code               |
| 16.P_IHGEM.xpt   | `LBXMHG`       | `mercury_methyl_ug_l`            | Methyl mercury (µg/L)                    |
| 16.P_IHGEM.xpt   | `LBDMHGSI`     | `mercury_methyl_nmol_l`          | Methyl mercury (nmol/L)                  |
| 16.P_IHGEM.xpt   | `LBDMHGC`      | `mercury_methyl_comment_code`    | Methyl mercury comment code              |
| 17.P_INS.xpt   | `WTSAF2YR`     | `fasting_subsample_weight`  | Fasting subsample 2-year weight |
| 17.P_INS.xpt   | `LBXINSI`      | `insulin_μu_ml`             | Insulin (µU/mL)                |
| 17.P_INS.xpt   | `LBDINSI`      | `insulin_pmol_l`            | Insulin (pmol/L)               |
| 17.P_INS.xpt   | `LBDINSC`      | `insulin_comment_code`      | Insulin comment code           |
| 18.P_PBCD.xpt | `LBXBPB`                      | `blood_lead_ug_dl`              | Blood lead (µg/dL)             |
| 18.P_PBCD.xpt | `LBDPBLC`                     | `blood_lead_comment_code`       | Blood lead comment code        |
| 18.P_PBCD.xpt | `LBDPBNSI`                    | `blood_lead_umol_l`             | Blood lead (µmol/L)            |
| 18.P_PBCD.xpt | `LBXBCd`                      | `blood_cadmium_ug_l`            | Blood cadmium (µg/L)           |
| 18.P_PBCD.xpt | `LBDCdNSI`                    | `blood_cadmium_nmol_l`          | Blood cadmium (nmol/L)         |
| 18.P_PBCD.xpt | `LBDCdLC`                     | `blood_cadmium_comment_code`    | Blood cadmium comment code     |
| 18.P_PBCD.xpt | `LBXTHg`                      | `blood_mercury_total_ug_l`      | Blood mercury total (µg/L)     |
| 18.P_PBCD.xpt | `LBDTHgNSI`                   | `blood_mercury_total_nmol_l`    | Blood mercury total (nmol/L)   |
| 18.P_PBCD.xpt | `LBDTHgLC`                    | `blood_mercury_total_comment_code` | Blood mercury total comment code |
| 18.P_PBCD.xpt | `LBXSEL`                      | `blood_selenium_ug_l`           | Blood selenium (µg/L)          |
| 18.P_PBCD.xpt | `LBDSELNSI`                   | `blood_selenium_umol_l`         | Blood selenium (µmol/L)        |
| 18.P_PBCD.xpt | `LBDSELLC`                   | `blood_selenium_comment_code`   | Blood selenium comment code    |
| 18.P_PBCD.xpt | `LBXMNG`                      | `blood_manganese_ug_l`          | Blood manganese (µg/L)         |
| 18.P_PBCD.xpt | `LBDMNGNSI`                   | `blood_manganese_nmol_l`        | Blood manganese (nmol/L)       |
| 18.P_PBCD.xpt | `LBDMNGLC`                   | `blood_manganese_comment_code`  | Blood manganese comment code   |
| 19.P_PFAS.xpt | `LBXPFOA`                             | `perfluorodecanoic_acid_ng_ml`          | Perfluorodecanoic acid (ng/mL)       |
| 19.P_PFAS.xpt | `LBDPFOALC`                          | `perfluorodecanoic_acid_comment_code`   | Perfluorodecanoic acid comment code  |
| 19.P_PFAS.xpt | `LBXPFH`                             | `perfluorohexane_sulfonic_acid_ng_ml`   | Perfluorohexane sulfonic acid (ng/mL)|
| 19.P_PFAS.xpt | `LBDPFHLC`                          | `perfluorohexane_sulfonic_acid_comment_code` | Perfluorohexane sulfonic acid comment code |
| 19.P_PFAS.xpt | `LBXNMPA`                            | `2_n_methyl_pfosaacetic_acid_ng_ml`     | 2-N-Methyl PFOSA acetic acid (ng/mL)|
| 19.P_PFAS.xpt | `LBDNMPALC`                         | `2_n_methyl_pfosa_acetic_acid_comment_code` | 2-N-Methyl PFOSA acetic acid comment code |
| 19.P_PFAS.xpt | `LBXPFNA`                            | `perfluorononanoic_acid_ng_ml`          | Perfluorononanoic acid (ng/mL)       |
| 19.P_PFAS.xpt | `LBDPFNALC`                         | `perfluorononanoic_acid_comment_code`   | Perfluorononanoic acid comment code  |
| 19.P_PFAS.xpt | `LBXPFUA`                            | `perfluoroundecanoic_acid_ng_ml`        | Perfluoroundecanoic acid (ng/mL)     |
| 19.P_PFAS.xpt | `LBDPFUALC`                         | `perfluoroundecanoic_acid_comment_code` | Perfluoroundecanoic acid comment code|
| 19.P_PFAS.xpt | `LBXPFOA`                            | `n_perfluorooctanoic_acid_ng_ml`        | N-Perfluorooctanoic acid (ng/mL)     |
| 19.P_PFAS.xpt | `LBDPFOALC`                         | `n_perfluorooctanoic_acid_comment_code` | N-Perfluorooctanoic acid comment code|
| 19.P_PFAS.xpt | `LBXPFOS`                           | `br_perfluorooctanoic_acid_iso_ng_ml`   | Br Perfluorooctanoic acid iso (ng/mL)|
| 19.P_PFAS.xpt | `LBDPFOSLC`                        | `br_perfluorooctanoic_acid_iso_comment_code` | Br Perfluorooctanoic acid iso comment code |
| 19.P_PFAS.xpt | `LBXPFOSNS`                        | `n_perfluorooctane_sulfonic_acid_ng_ml` | N-Perfluorooctane sulfonic acid (ng/mL)|
| 19.P_PFAS.xpt | `LBDPFOSNSLC`                      | `n_perfluorooctane_sulfonic_acid_comment_code` | N-Perfluorooctane sulfonic acid comment code |
| 19.P_PFAS.xpt | `LBXPFOS`                          | `sm_pfos_ng_ml`                         | Serum PFOS (ng/mL)                   |
| 19.P_PFAS.xpt | `LBDPFOSLC`                       | `sm_pfos_comment_code`                   | Serum PFOS comment code              |
| 20.P_GLU.xpt | `GLUFSG`              | `fasting_glucose_mg_dl`   | Fasting glucose (mg/dL) |
| 20.P_GLU.xpt | `GLUFSM`              | `fasting_glucose_mmol_l`  | Fasting glucose (mmol/L)|
| 21.P_TST.xpt | `P0217HPR` (example variable name) | `17alpha_hydroxyprogesterone_ng_dl`       |             |
| 21.P_TST.xpt | (corresponding variable name)      | `17alpha_hydroxyprogesterone_nmol_l`      |             |
| 21.P_TST.xpt | (corresponding variable name)      | `17alpha_hydroxyprogesterone_comment_code`|             |
| 21.P_TST.xpt | (corresponding variable name)      | `androstenedione_ng_dl`                     |             |
| 21.P_TST.xpt | (corresponding variable name)      | `androstenedione_nmol_l`                    |             |
| 21.P_TST.xpt | (corresponding variable name)      | `androstenedione_comment_code`              |             |
| 21.P_TST.xpt | (corresponding variable name)      | `anti_mullerian_hormone_ng_ml`              |             |
| 21.P_TST.xpt | (corresponding variable name)      | `anti_mullerian_hormone_pmol_l`             |             |
| 21.P_TST.xpt | (corresponding variable name)      | `anti_mullerian_hormone_comment_code`       |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estradiol_pg_ml`                           |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estradiol_pmol_l`                          |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estradiol_comment_code`                    |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estrone_ng_dl`                             |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estrone_pmol_l`                            |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estrone_comment_code`                      |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estrone_sulfate_pg_ml`                     |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estrone_sulfate_pmol_l`                    |             |
| 21.P_TST.xpt | (corresponding variable name)      | `estrone_sulfate_comment_code`              |             |
| 21.P_TST.xpt | (corresponding variable name)      | `follicle_stimulating_hormone_miu_ml`      |             |
| 21.P_TST.xpt | (corresponding variable name)      | `fsh_comment_code`                          |             |
| 21.P_TST.xpt | (corresponding variable name)      | `luteinizing_hormone_miu_ml`                |             |
| 21.P_TST.xpt | (corresponding variable name)      | `luteinizing_hormone_comment_code`          |             |
| 21.P_TST.xpt | (corresponding variable name)      | `progesterone_ng_dl`                        |             |
| 21.P_TST.xpt | (corresponding variable name)      | `progesterone_nmol_l`                       |             |
| 21.P_TST.xpt | (corresponding variable name)      | `progesterone_comment_code`                 |             |
| 21.P_TST.xpt | (corresponding variable name)      | `shbg_nmol_l`                              |             |
| 21.P_TST.xpt | (corresponding variable name)      | `shbg_comment_code`                         |             |

---

### 🧬 Encoded Value References

#### Gender (`RIAGENDR`)
- `1` = Male  
- `2` = Female

#### Race (`RIDRETH3`)
- `1` = Mexican American  
- `2` = Other Hispanic  
- `3` = Non-Hispanic White  
- `4` = Non-Hispanic Black  
- `6` = Non-Hispanic Asian  
- `7` = Other Race – Including Multi-Racial

#### Education Level (`DMDEDUC2`)
- `1` = Less than 9th grade
- `2` = 9-11th grade (includes 12th grade with no diploma)
- `3` = High school graduate/GED or equivalent
- `4` = Some college or AA degree
- `5` = College graduate or above
- `7` = Refused
- `9` = Don't know

#### Marital Status (`DMDMARTZ`)
- `1` = Married/living with partner
- `2` = Widowed/divorced/separated
- `3` = Never married
- `77` = Refused
- `99` = Don't know

#### Standing height comment (`BMIHT`)
- `1` = Could not obtain
- `3` = Not straight

#### Pediatric BMI Category (`BMDBMIC`)
- `1` = Underweight
- `2` = Normal weight
- `3` = Overweight
- `4` = Obese

#### Lab Comment Codes (applies to all '_comment' columns)
- `0` = at or above the limit of detection
- `1` = below the limit of detection

#### Urine Pregnancy Test Reslut
- `1` = Positive
- `2` = Negative
- `3` = Not Done

#### CMV IgG avidity
- `1` = Low
- `2` = High
- `3` = Indeterminate

#### Hepatitis A Antibody
- `1` = Positive
- `2` = Negative
- `3` = Indeterminate

#### Hepatitis B Surface Antibody
- `1` = Positive
- `2` = Negative
- `3` = Indeterminate

#### Hepatitis B Core Antigen/Antibody
- `1` = Positive
- `2` = Negative
- `3` = Indeterminate

### Hepatitis D Antibody
- `1` = Positive
- `2` = Negative
- `3` = Indeterminate

### Hepatitis D Antibody Retesting
- `0` = Hep sAg positive, no surplus sample	
- `1` =	Hep sAg positive, reactive	0	24	
- `2` =	Hep sAg positive, non-reactive	20	44	
- `6` = 	Hep sAg negative, not retested

#### Hepatitis C RNA
- `1` = Positive
- `2` = Negative
- `3` = Negative screening HCV antibody

### Hepatitis C Antibody (confirmed)
- `1` =	Positive	
- `2` =	Negative	
- `3` =	Negative Screening HCV Antibody	
- `4` =	Positive HCV RNA

#### Hepatitis C Genotype
- `1` =	Genotype 1a	
- `2` =	Genotype 1b		
- `3` =	Gen 1 other than a/b/not determined		
- `4` =	Genotype 2	
- `5` =	Genotype 3		
- `6` =	Genotype 4		
- `7` =	Genotype 5	
- `8` =	Genotype 6		
- `9` =	Genotype undetermined

#### Hepatitis E IgG/IgM
- `1` = Positive
- `2` = Negative
- `3` = Indeterminate


### Functions

#### `drop_rows_with_both_nans()`
Removes rows where both `col1` and `col2` are NaN.

#### `get_common_nan_ids()`
Identifies participant IDs with NaNs in both columns. Useful for understanding overlap in missing data.

#### `standardize_id_column()`
Renames the original identifier column to 'participant_id'
...

### Column Changes
- Renamed columns are tracked in the [Variable Key](#variable-key-column-renaming)
- Encoded values are kept in raw format; meanings are described above.

## Merging Datasets

All datasets are merged using `participant_id` as the key. Merges are typically done using an inner join to preserve only complete records.

```python
merged_df = df1.merge(df2, on='participant_id', how='inner')
