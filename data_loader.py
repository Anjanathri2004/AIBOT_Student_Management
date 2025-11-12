import os
import glob
import pandas as pd

DATA_DIR = "data"

def find_csv_files(data_dir: str = DATA_DIR):
    return sorted(glob.glob(os.path.join(data_dir, "*.csv")))

def load_and_concat_csvs(data_dir: str = DATA_DIR) -> pd.DataFrame:
    files = find_csv_files(data_dir)
    if not files:
        return pd.DataFrame(columns=["student_name", "grade", "class", "quiz_score", "submission_status"])

    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping {f}: {e}")
    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    for col in ["grade", "class"]:
        if col in df_all.columns:
            df_all[col] = df_all[col].astype(str).str.strip()
    return df_all

def get_unique_sorted_values(df, column):
    if column not in df.columns:
        return []
    vals = sorted(df[column].dropna().unique().tolist())
    return vals
