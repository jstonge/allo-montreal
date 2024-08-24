import pandas as pd
import sys

df_pop = pd.read_excel("http://ville.montreal.qc.ca/pls/portal/url/ITEM/55637C4923B8B03EE0530A930132B03E", sheet_name="01_Population, Densité", skiprows=2).iloc[:-4, :]
df_pop.rename(columns={'Unnamed: 0': 'arrondissement', 'Population en 2016': '2016', 'Population en 2011': '2011'}, inplace=True)
df_pop = df_pop[~df_pop.arrondissement.isin(['Autres villes', 'Ville de Montréal','AGGLOMÉRATION DE MONTRÉAL'])]
# df_pop['arrondissement'] = df_pop['arrondissement'].apply(normalize_name)
df_pop_long = df_pop[['arrondissement', '2016', '2011']].melt(id_vars='arrondissement', var_name='year', value_name='population')
df_pop_long.to_csv(sys.stdout)