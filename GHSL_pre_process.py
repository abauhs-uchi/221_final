import pandas as pd
import os

# ── 0. Paths ─────────────────────────────────────────────────────────────────
BASE_DIR = r'C:\Users\aleks\OneDrive\Desktop\machine_learning\final'
os.chdir(BASE_DIR)

RAW_PATH = r'raw_GHSL.csv'
OUT_WIDE = r'GHSL.csv'
OUT_LONG = r'GHSL_long.csv'

# ── 1. Load & deduplicate ─────────────────────────────────────────────────────
print("Loading raw data...")
raw = pd.read_csv(RAW_PATH, low_memory=False)
print(f"  Raw shape:          {raw.shape}")

n_dupes = raw.duplicated(subset='ID_UC_G0').sum()
raw = raw.drop_duplicates(subset='ID_UC_G0', keep='first')
print(f"  Duplicate city IDs: {n_dupes}  →  shape after dedup: {raw.shape}")

# ── 2. Define time-varying features to keep ──────────────────────────────────
# XXXX is replaced with each year in VALID_YEARS below.
#
# Notes on omissions vs. original script:
#   - GC_UCN_MAI and GC_CNT_GAD are excluded here: they only exist for 2025
#     in the dataset and are already captured as meta/ID columns below.
#     Including them via XXXX expansion added nothing and caused name collisions.
#   - GC_DEV_USR_2025 is a static categorical region label; kept as a meta col.
FEATURES_XXXX = [
    "EM_PM2_CON_XXXX",   # PM2.5 concentration
    "GC_UCA_KM2_XXXX",   # Urban area (km²)
    "GC_POP_TOT_XXXX",   # Total population
    "GC_DEV_WIG_XXXX",   # World income group
    "GH_BPC_TOT_XXXX",   # Built-up area per capita
    "GH_POP_TOT_XXXX",   # GHS population total
    "GH_POP_CAG_XXXX",   # Population compound annual growth
    "SC_GDP_AVG_XXXX",   # Average GDP
    "SC_SEC_HDI_XXXX",   # Human Development Index
    "SC_SEC_GDI_XXXX",   # Gender Development Index
    "SC_SEC_LET_XXXX",   # Life expectancy total
    "SC_SEC_SYT_XXXX",   # School years total
    "EM_CO2_PEC_XXXX",   # CO2 per capita
    "EM_GHG_PEC_XXXX",   # GHG per capita
    "EM_NOX_PEC_XXXX",   # NOx per capita
    "EM_PM2_PEC_XXXX",   # PM2.5 per capita
    "HZ_CON_VAC_XXXX",   # Volcanic hazard conditional probability
    "HZ_CON_RIO_XXXX",   # River flood hazard conditional probability
    "HZ_CON_PRO_XXXX",   # Probable max hazard
    "HZ_CEV_EAR_XXXX",   # Earthquake cumulative events
    "HZ_CEV_EWI_XXXX",   # Extreme wind cumulative events
    "HZ_CEV_TSU_XXXX",   # Tsunami cumulative events
    "HZ_CEV_HEW_XXXX",   # Heatwave cumulative events
    "HZ_CEV_DRO_XXXX",   # Drought cumulative events
    "HZ_CEV_TCY_XXXX",   # Tropical cyclone cumulative events
    "HZ_CEV_VOL_XXXX",   # Volcanic cumulative events
    "HZ_CEV_LAN_XXXX",   # Landslide cumulative events
    "HZ_CEV_COW_XXXX",   # Cold wave cumulative events
    "HZ_CEV_WLF_XXXX",   # Wildfire cumulative events
    "GR_SHB_GRN_XXXX",   # Share of green/vegetated built-up
    "SD_POP_HGR_XXXX",   # Population in high-risk areas
    "NS_ESB_BIO_XXXX",   # Biodiversity exposure
    "NS_ESB_GWA_XXXX",   # Groundwater availability
    "NS_ESB_NIT_XXXX",   # Nitrogen exposure
    "NS_ESB_PHO_XXXX",   # Phosphorus exposure
    "NS_ESB_SLR_XXXX",   # Sea level rise exposure
    "NS_ESB_SWA_XXXX",   # Surface water availability
    "NS_ESB_WET_XXXX",   # Wetland exposure
    "NS_ESB_MIN_XXXX",   # Min ecosystem stress
    "NS_ESB_MAX_XXXX",   # Max ecosystem stress
    "HL_FPC_HOS_XXXX",   # Hospital floor area per capita
    "HL_SHP_HOS_XXXX",   # Share of population near hospital
    "IN_ROA_DEN_XXXX",   # Road density
    "IN_CIS_ALL_XXXX",   # Infrastructure composite (all)
    "IN_CIS_ENE_XXXX",   # Infrastructure: energy
    "IN_CIS_TRA_XXXX",   # Infrastructure: transport
    "IN_CIS_WAT_XXXX",   # Infrastructure: water
    "IN_CIS_WAS_XXXX",   # Infrastructure: waste
    "IN_CIS_TEL_XXXX",   # Infrastructure: telecom
    "IN_CIS_HEA_XXXX",   # Infrastructure: health
    "IN_CIS_EDU_XXXX",   # Infrastructure: education
]

VALID_YEARS = list(range(1970, 2021, 5)) + [2025]

time_cols = []
for template in FEATURES_XXXX:
    time_cols += [template.replace('XXXX', str(y)) for y in VALID_YEARS]

# Keep only columns present in the raw file
time_cols = [c for c in time_cols if c in raw.columns]

# ── 3. Meta (identity) columns ───────────────────────────────────────────────
# These are row identifiers and are never melted into the time series.
META_COLS = ['ID_UC_G0', 'GC_UCN_MAI_2025', 'GC_CNT_GAD_2025', 'GC_DEV_USR_2025']
meta_present = [c for c in META_COLS if c in raw.columns]

# Safety: remove any time_col that shares a name with a meta col.
# (Prevents duplicate columns when subsetting the DataFrame.)
time_cols = [c for c in time_cols if c not in meta_present]

# ── 4. Build wide dataframe & save ───────────────────────────────────────────
df = raw[meta_present + time_cols].copy()

# Normalize city name casing
df['GC_UCN_MAI_2025'] = df['GC_UCN_MAI_2025'].astype(str).str.strip().str.title()

assert not df.columns.duplicated().any(), "Duplicate column names detected in wide df!"

df.to_csv(OUT_WIDE, index=False)
print(f"\nWide file saved → {OUT_WIDE}  shape: {df.shape}")

# ── 5. Melt: wide → long ─────────────────────────────────────────────────────
print("\nReshaping to long format...")

df_long = df.melt(
    id_vars=meta_present,
    value_vars=time_cols,
    var_name='variable',
    value_name='value'
)

# Extract feature prefix and year using regex — robust against any naming edge cases
extracted = df_long['variable'].str.extract(r'^(.+)_(\d{4})$')
df_long['feature'] = extracted.iloc[:, 0]
df_long['year']    = extracted.iloc[:, 1].astype(int)
df_long = df_long.drop(columns='variable')

# Drop rows where extraction failed (defensive)
df_long = df_long.dropna(subset=['feature', 'year'])

print(f"  Long shape: {df_long.shape}  |  years: {sorted(df_long['year'].unique())}")

# ── 6. Pivot to city × year panel ────────────────────────────────────────────
INDEX_COLS = ['ID_UC_G0', 'GC_UCN_MAI_2025', 'GC_CNT_GAD_2025', 'GC_DEV_USR_2025', 'year']

df_panel = (
    df_long
    .pivot_table(
        index=INDEX_COLS,
        columns='feature',
        values='value',
        aggfunc='first',  # each city × year × feature is unique
    )
    .reset_index()
)
df_panel.columns.name = None

# ── 7. Drop unwanted feature groups ─────────────────────────────────────────
# IN_CIS_*: composite infrastructure index (redundant with sub-scores)
# HZ_CEV_*: cumulative hazard event counts (we keep HZ_CON_* probability scores)
DROP_PREFIXES = ('IN_CIS_', 'HZ_CEV_')
cols_to_drop = [c for c in df_panel.columns if c.startswith(DROP_PREFIXES)]
df_panel = df_panel.drop(columns=cols_to_drop)
print(f"\n  Dropped {len(cols_to_drop)} columns with prefixes {DROP_PREFIXES}")
print(f"  Panel shape: {df_panel.shape}")

# ── 8. Sort & interpolate within each city ───────────────────────────────────
df_panel = df_panel.sort_values(['ID_UC_G0', 'year']).reset_index(drop=True)

feature_cols = [c for c in df_panel.columns if c not in INDEX_COLS]

# Pivot_table can produce object dtype even for numeric data when there are
# mixed NaN patterns; force numeric conversion before interpolation.
df_panel[feature_cols] = df_panel[feature_cols].apply(pd.to_numeric, errors='coerce')

def _interpolate_city(group):
    """Linear interpolation within each city's observed range; no extrapolation."""
    return group[feature_cols].interpolate(method='linear', limit_area='inside')

print("  Interpolating missing values within each city...")
df_panel[feature_cols] = (
    df_panel
    .groupby('ID_UC_G0', group_keys=False)
    .apply(_interpolate_city)
)

# ── 9. Summary & save ────────────────────────────────────────────────────────
print(f"\nFinal panel shape: {df_panel.shape}")

missing = (
    df_panel[feature_cols]
    .isnull().sum()
    .div(len(df_panel))
    .mul(100)
    .round(1)
    .sort_values(ascending=False)
)
missing_nonzero = missing[missing > 0]
if missing_nonzero.empty:
    print("No missing values remaining after interpolation.")
else:
    print(f"\nMissing % after interpolation ({len(missing_nonzero)} columns with gaps):")
    print(missing_nonzero.to_string())

df_panel.to_csv(OUT_LONG, index=False)
print(f"\nLong panel saved → {OUT_LONG}")
print("Done.")