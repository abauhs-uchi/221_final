import pandas as pd

xl = pd.ExcelFile(r'raw_zips\GHS_UCDB_GLOBE_R2024A_V1_1\GHS_UCDB_GLOBE_R2024A.xlsx')
sheets_to_load = xl.sheet_names[2:]
sheet_dict = pd.read_excel(
    r'raw_zips\GHS_UCDB_GLOBE_R2024A_V1_1\GHS_UCDB_GLOBE_R2024A.xlsx',
    sheet_name=sheets_to_load,
    na_values=['-'],
)

sheet_list = list(sheet_dict.values())
merged_df = sheet_list[0]

for df in sheet_list[1:]:
    common_cols = [c for c in merged_df.columns if c in set(df.columns)]
    merged_df = merged_df.merge(df, on=common_cols, how='left')

merged_df.to_csv(r'raw_parquets_csvs/raw_GHSL.csv', index=False)
merged_df.to_parquet(r'raw_parquets_csvs/raw_GHSL.parquet', index=False)