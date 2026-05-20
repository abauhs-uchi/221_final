import pandas as pd


df= pd.read_csv(r'raw_parquets_csvs\raw_GHSL.csv')
df_sub = df.duplicated()
df_sub.to_csv(r'Preproccessing\wip.csv')

assert df['ID_UC_G0'].is_unique         #Confirm ids are unique
assert df['GC_UCN_MAI_2025'].is_unique  #Confirm City namaes are unique.
'''
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].where(df[col].notna(), None)
'''

df.to_csv(r'Preproccessing\GHSL.csv')

cols_to_keep_xxxx =   ["EM_PM2_CON_XXXX",
"GC_UCN_MAI_XXXX","GC_UCA_KM2_XXXX",
"GC_POP_TOT_XXXX","GC_DEV_WIG_XXXX",
"GH_BPC_TOT_XXXX","GH_POP_TOT_XXXX",
"GH_POP_CAG_XXXX","SC_GDP_AVG_XXXX",
"SC_SEC_HDI_XXXX","SC_SEC_GDI_XXXX",
"SC_SEC_LET_XXXX","SC_SEC_SYT_XXXX",
"EM_CO2_PEC_XXXX","EM_GHG_PEC_XXXX",
"EM_NOX_PEC_XXXX","EM_PM2_PEC_XXXX",
"HZ_CON_VAC_XXXX","HZ_CON_RIO_XXXX",
"HZ_CON_PRO_XXXX","HZ_CEV_EAR_XXXX",
"HZ_CEV_EWI_XXXX","HZ_CEV_TSU_XXXX",
"HZ_CEV_HEW_XXXX","HZ_CEV_DRO_XXXX",
"HZ_CEV_TCY_XXXX","HZ_CEV_VOL_XXXX",
"HZ_CEV_LAN_XXXX","HZ_CEV_COW_XXXX",
"HZ_CEV_WLF_XXXX","GR_SHB_GRN_XXXX",
"SD_POP_HGR_XXXX","NS_ESB_BIO_XXXX",
"NS_ESB_GWA_XXXX","NS_ESB_NIT_XXXX",
"NS_ESB_PHO_XXXX","NS_ESB_P25_XXXX",
"NS_ESB_SLR_XXXX","NS_ESB_SWA_XXXX",
"NS_ESB_WET_XXXX","NS_ESB_MIN_XXXX",
"NS_ESB_MAX_XXXX","HL_FPC_HOS_XXXX",
"HL_SHP_HOS_XXXX","IN_ROA_DEN_XXXX",
"IN_CIS_ALL_XXXX","IN_CIS_ENE_XXXX",
"IN_CIS_TRA_XXXX","IN_CIS_WAT_XXXX",
"IN_CIS_WAS_XXXX","IN_CIS_TEL_XXXX",
"IN_CIS_HEA_XXXX","IN_CIS_EDU_XXXX",]

valid_dates = range(1970, 2025, 5) 
cols_to_keep =[]
for feature in cols_to_keep_xxxx:
    cols_to_keep += [feature + str(i) for i in valid_dates]
