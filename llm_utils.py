# llm_utils.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

sns.set(style="whitegrid")

def normalize_columns(df):
    # Lowercase, strip spaces, replace special chars with underscores
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(r'\s+', '_', regex=True)
                  .str.replace(r'[^\w]', '', regex=True)
    )
    return df

def filter_rows_by_column(df, query):
    q = query.lower()
    # Look for "from <value>" or "where <col> is <value>"
    from_match = re.search(r'from (\w+)', q)
    where_match = re.search(r'where (\w+) (is|=|= is) (\w+)', q)
    
    if from_match:
        filter_value = from_match.group(1)
        for col in df.columns:
            if filter_value in df[col].astype(str).str.lower().values:
                filtered_df = df[df[col].astype(str).str.lower() == filter_value]
                return filtered_df.to_dict(orient='records')

    if where_match:
        col_name = where_match.group(1)
        val = where_match.group(3)
        if col_name in df.columns:
            filtered_df = df[df[col_name].astype(str).str.lower() == val]
            return filtered_df.to_dict(orient='records')

    return None

def get_column_names(df):
    return list(df.columns)

def is_numeric_column(df, col):
    return pd.api.types.is_numeric_dtype(df[col])

def extract_columns_from_query(df, query):
    # Find which columns appear in the query
    cols = []
    for col in df.columns:
        if col in query.lower():
            cols.append(col)
    return cols

def process_query(df: pd.DataFrame, query: str):
    df = normalize_columns(df)
    query_lower = query.lower()

    # Handle filtered queries like "Show all customers from East region"
    filtered_rows = filter_rows_by_column(df, query_lower)
    if filtered_rows is not None:
        if len(filtered_rows) == 0:
            return "No rows found matching the filter."
        return filtered_rows  # list of dicts

    # Handle summary statistics queries
    if "average" in query_lower or "mean" in query_lower:
        cols = extract_columns_from_query(df, query_lower)
        numeric_cols = [c for c in cols if is_numeric_column(df, c)]
        if not numeric_cols:
            # If user didn't specify column, try numeric columns in df
            numeric_cols = [c for c in df.columns if is_numeric_column(df, c)]
        if numeric_cols:
            averages = {col: round(df[col].mean(), 2) for col in numeric_cols}
            return f"Averages:\n" + "\n".join([f"{col}: {val}" for col, val in averages.items()])
        else:
            return "No numeric columns found for calculating average."

    if "total" in query_lower or "sum" in query_lower:
        cols = extract_columns_from_query(df, query_lower)
        numeric_cols = [c for c in cols if is_numeric_column(df, c)]
        if not numeric_cols:
            numeric_cols = [c for c in df.columns if is_numeric_column(df, c)]
        if numeric_cols:
            totals = {col: round(df[col].sum(), 2) for col in numeric_cols}
            return f"Totals:\n" + "\n".join([f"{col}: {val}" for col, val in totals.items()])
        else:
            return "No numeric columns found for calculating total."

    if "count" in query_lower or "how many" in query_lower:
        cols = extract_columns_from_query(df, query_lower)
        if not cols:
            return f"There are {len(df)} rows in the data."
        else:
            col = cols[0]
            counts = df[col].value_counts().to_dict()
            return f"Counts for {col}:\n" + "\n".join([f"{k}: {v}" for k, v in counts.items()])

    # Handle bar chart queries like "Show a bar chart of sales by region"
    if "bar chart" in query_lower or "bar graph" in query_lower:
        # Extract measure and group columns from query
        words = query_lower.split()
        if "by" in words:
            by_index = words.index("by")
            # measure is word before "by"
            if by_index > 0:
                measure = words[by_index - 1]
            else:
                measure = None
            group = words[by_index + 1] if by_index + 1 < len(words) else None

            # Match measure and group to actual columns in df
            measure_col = None
            group_col = None
            for col in df.columns:
                if measure and measure in col:
                    measure_col = col
                if group and group in col:
                    group_col = col

            if measure_col and group_col:
                # Aggregate and plot
                plt.figure(figsize=(8,5))
                plot_data = df.groupby(group_col)[measure_col].sum().reset_index()
                sns.barplot(data=plot_data, x=group_col, y=measure_col)
                plt.title(f"Bar Chart of {measure_col} by {group_col}")
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Save figure
                if not os.path.exists("charts"):
                    os.makedirs("charts")
                chart_path = "charts/bar_chart.png"
                plt.savefig(chart_path)
                plt.close()
                return chart_path
            else:
                return "Could not find columns to plot bar chart. Please be more specific."

    # Handle histogram queries like "Plot a histogram of ages"
    if "histogram" in query_lower:
        cols = extract_columns_from_query(df, query_lower)
        numeric_cols = [c for c in cols if is_numeric_column(df, c)]
        if numeric_cols:
            col = numeric_cols[0]
            plt.figure(figsize=(8,5))
            sns.histplot(df[col].dropna(), kde=False)
            plt.title(f"Histogram of {col}")
            plt.tight_layout()

            if not os.path.exists("charts"):
                os.makedirs("charts")
            chart_path = "charts/histogram.png"
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        else:
            return "No numeric column found to plot histogram."

    # For showing rows with some filter keywords
    if "show all" in query_lower or "list all" in query_lower:
        # try find column and value in query
        for col in df.columns:
            if col in query_lower:
                # Find possible filter value by removing known words
                possible_values = set(df[col].astype(str).str.lower())
                for val in possible_values:
                    if val in query_lower:
                        filtered_df = df[df[col].astype(str).str.lower() == val]
                        if filtered_df.empty:
                            return f"No rows found with {col} = '{val}'."
                        return filtered_df.to_dict(orient='records')

    # If none matched, fallback
    return "Sorry, I couldn't understand the question. Try rephrasing or ask for summary statistics like average, total, count."
