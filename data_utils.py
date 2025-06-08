# data_utils.py

import pandas as pd
import re

def clean_column_name(name):
    """Normalize column name: lowercase, remove special chars, spaces"""
    name = name.strip().lower()
    name = re.sub(r'[^a-z0-9]', '_', name)
    return name

def load_and_clean_excel(file):
    """Reads Excel and returns original df, cleaned df, and mapping"""
    df = pd.read_excel(file)

    original_columns = df.columns.tolist()
    cleaned_columns = [clean_column_name(col) for col in original_columns]
    col_map = dict(zip(cleaned_columns, original_columns))

    df.columns = cleaned_columns
    return df, col_map
