import pandas as pd

def get_accessible_data(admin_role, df: pd.DataFrame):
    if df.empty:
        return df
    grade = admin_role.get("grade")
    class_ = admin_role.get("class")

    filtered = df.copy()
    if grade:
        filtered = filtered[filtered["grade"].astype(str) == str(grade)]
    if class_:
        filtered = filtered[filtered["class"].astype(str) == str(class_)]
    return filtered.reset_index(drop=True)
