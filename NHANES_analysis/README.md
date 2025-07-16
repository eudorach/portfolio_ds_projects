# NHANES Obesity and Biomarkers Study

## Overview
This project uses NHANES 2017–2020 datasets to explore relationships between biomarkers (primarily from blood and urine lab results) and obesity. The final goal is to clean and organize this data into a relational database for predictive modeling and analysis.

---

## Data Sources
- NHANES 2017–2020: [https://wwwn.cdc.gov/nchs/nhanes/](https://wwwn.cdc.gov/nchs/nhanes/)


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

Add blood dataset rows as you clean them.

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

### Functions

#### `drop_rows_with_both_nans()`
Removes rows where both `col1` and `col2` are NaN.

#### `get_common_nan_ids()`
Identifies participant IDs with NaNs in both columns. Useful for understanding overlap in missing data.

...

### Column Changes
- Renamed columns are tracked in the [Variable Key](#variable-key-column-renaming)
- Encoded values are kept in raw format; meanings are described above.

## Merging Datasets

All datasets are merged using `participant_id` as the key. Merges are typically done using an inner join to preserve only complete records.

```python
merged_df = df1.merge(df2, on='participant_id', how='inner')
