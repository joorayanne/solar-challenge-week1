from typing import List, Tuple
import pandas as pd
import numpy as np

def zscore_flags(df: pd.DataFrame, cols: List[str], thresh: float = 3.0) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            m, s = out[c].mean(), out[c].std(ddof=0)
            if s == 0 or np.isnan(s):
                out[f"{c}_z"] = 0.0
            else:
                out[f"{c}_z"] = (out[c] - m) / s
            out[f"{c}_outlier"] = out[f"{c}_z"].abs() > thresh
    return out

def impute_median(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            med = out[c].median()
            out[c] = out[c].fillna(med)
    return out