import pandas as pd
import numpy as np

def clean_data_project(df_raw):
    df = df_raw.copy()
    
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["income"] = pd.to_numeric(df["income"], errors="coerce")
    df["signup_time"] = pd.to_datetime(df["signup_time"], errors="coerce")
    
    df["age_missing"] = df["age"].isna().astype(int)
    df["age"] = df["age"].fillna(df["age"].median())
    
    df["income_missing"] = df["income"].isna().astype(int)
    df["income"] = df["income"].fillna(df["income"].median())
    
    df["income"] = df["income"].clip(upper=df["income"].quantile(0.99))
    
    if "city" in df.columns:
        df["city"] = df["city"].str.strip().str.lower()
    
    if df["signup_time"].dt.tz is None:
        df["signup_time"] = df["signup_time"].dt.tz_localize("UTC")
    else:
        df["signup_time"] = df["signup_time"].dt.tz_convert("UTC")
        
    return df

cleaning_decisions = {
    "income_cap_99": "Cap income at 99th percentile to reduce influence of extreme values while keeping all records.",
    "age_median_imp": "Impute missing age with global median; less sensitive to outliers than mean."
}

# الاستخدام:
# df_final = clean_data_project(pd.read_csv("data.csv"))
# df_final.to_csv("cleaned_data.csv", index=False)