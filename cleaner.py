import pandas as pd
from pathlib import Path
import argparse

def clean_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df

def generate_report(df, duplicates_removed, output_file):
    print("\n==============================")
    print("        CSV CLEANING REPORT   ")
    print("==============================")
    print(f"Rows after cleaning : {df.shape[0]}")
    print(f"Columns             : {df.shape[1]}")
    print(f"Duplicates removed  : {duplicates_removed}")
    print(f"Saved output to     : {output_file}")

    print("\nMissing values per column:")
    print(df.isnull().sum())

def clean_csv(input_file, output_file):
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        return

    df = pd.read_csv(input_path)

    print("\n--- ORIGINAL DATA PREVIEW ---")
    print(df.head())

    print("\n--- ORIGINAL INFO ---")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Columns: {list(df.columns)}")

    # Clean column names
    df = clean_column_names(df)

    # Remove duplicate rows
    before_duplicates = len(df)
    df = df.drop_duplicates()
    after_duplicates = len(df)
    duplicates_removed = before_duplicates - after_duplicates

    # Fill missing values safely
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna("Unknown")

    # Save cleaned CSV
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)

    print("\n--- CLEANED DATA PREVIEW ---")
    print(df.head())

    generate_report(df, duplicates_removed, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and analyze CSV files.")
    parser.add_argument("input_file", help="Path to input CSV file")
    parser.add_argument(
        "-o", "--output",
        default="output/cleaned_data.csv",
        help="Path to save cleaned CSV"
    )

    args = parser.parse_args()
    clean_csv(args.input_file, args.output)