import pandas as pd
import os

os.chdir(r'C:\Users\aleks\OneDrive\Desktop\machine_learning\final')

# Load processed data and add city names back from raw
df = pd.read_csv(r'GHSL.csv', low_memory=False)
raw = pd.read_csv(r'raw_GHSL.csv', low_memory=False)

# Add city name and country back
df = df.merge(raw[['ID_UC_G0', 'GC_UCN_MAI_2025', 'GC_CNT_GAD_2025']], 
              on='ID_UC_G0', how='left')

# Standardize city names
df['GC_UCN_MAI_2025'] = (df['GC_UCN_MAI_2025']
                          .str.strip()
                          .str.title())

# Reshape from wide to long format
id_cols = ['ID_UC_G0', 'GC_UCN_MAI_2025', 'GC_CNT_GAD_2025']
value_cols = [c for c in df.columns if c not in id_cols]

df_long = df.melt(id_vars=id_cols, value_vars=value_cols,
                  var_name='variable', value_name='value')

# Split variable into feature + year
df_long['feature'] = df_long['variable'].str[:-5]
df_long['year'] = df_long['variable'].str[-4:].astype(int)
df_long = df_long.drop(columns='variable')

# Pivot so each feature is its own column
df_long = df_long.pivot_table(index=['ID_UC_G0', 'GC_UCN_MAI_2025',
                                      'GC_CNT_GAD_2025', 'year'],
                               columns='feature',
                               values='value').reset_index()

df_long.columns.name = None

# Drop IN_CIS and HZ_CEV columns
cols_to_drop = [c for c in df_long.columns if c.startswith('IN_CIS') or c.startswith('HZ_CEV')]
df_long = df_long.drop(columns=cols_to_drop)

# Sort by city and year
df_long = df_long.sort_values(['ID_UC_G0', 'year']).reset_index(drop=True)

# Feature columns to interpolate
feature_cols = [c for c in df_long.columns if c not in 
                ['ID_UC_G0', 'GC_UCN_MAI_2025', 'GC_CNT_GAD_2025', 'year']]

# Interpolate within each city, no extrapolation
def interpolate_city(group):
    return group[feature_cols].interpolate(method='linear', limit_area='inside')

df_long[feature_cols] = df_long.groupby('ID_UC_G0', group_keys=False).apply(interpolate_city)

print("Done! Shape:", df_long.shape)
print("\nMissing % after interpolation:")
missing = (df_long[feature_cols].isnull().sum() / len(df_long) * 100).round(1).sort_values(ascending=False)
print(missing[missing > 0].to_string())

df_long.to_csv(r'GHSL_long.csv', index=False)