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