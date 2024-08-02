import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Lataa datasetit
companies_df = pd.read_csv("data.csv")

# Suodata yritykset, joilla on vuotuinen liikevaihto
companies_with_revenue_df = companies_df[companies_df['Annual_Revenue'].notna()].copy()

# Erittele teknologiat yksittäisiksi kohteiksi
all_technologies = companies_with_revenue_df['Technologies'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
unique_technologies = all_technologies.unique()

# Luo DataFrame teknologioiden läsnäololle (1) tai poissaololle (0)
technology_presence_df = pd.get_dummies(all_technologies, prefix='', prefix_sep='').groupby(level=0).max()

# Tasoita sarakkeet varmistaaksesi, että kaikki ainutlaatuiset teknologiat ovat läsnä
technology_presence_df = technology_presence_df.reindex(columns=unique_technologies, fill_value=0)

# Laske teknologioiden lukumäärä kullekin yritykselle
companies_with_revenue_df['Technology_Count'] = technology_presence_df.sum(axis=1)

# Valitse lopullisen DataFramen relevantit sarakkeet
final_df = companies_with_revenue_df[['CompanyID', 'Annual_Revenue', 'Industry', 'Technology_Count', 'Lists']].copy()
final_df = pd.concat([final_df.reset_index(drop=True), technology_presence_df], axis=1)

# Varmistetaan, että kaikki unique_technologies -elementit ovat final_df -DataFramessa
final_tech_columns = set(final_df.columns)
unique_technologies_in_final_df = [tech for tech in unique_technologies if tech in final_tech_columns]

# Laske kunkin teknologian läsnäolon ja vuotuisen liikevaihdon välinen korrelaatio
correlation_with_revenue = final_df[unique_technologies_in_final_df + ['Annual_Revenue']].corr()['Annual_Revenue'].drop('Annual_Revenue')

# Laske teollisuuden ja vuotuisen liikevaihdon välinen korrelaatio
industry_correlation = pd.get_dummies(final_df['Industry'])
industry_correlation['Annual_Revenue'] = final_df['Annual_Revenue']
industry_correlation_corr = industry_correlation.corr()['Annual_Revenue'].drop('Annual_Revenue')

# Järjestä teollisuudet niiden liikevaihtokorrelaation mukaan
industry_ranking = industry_correlation_corr.rank(ascending=False).to_dict()

# Arvota teknologiat niiden liikevaihtokorrelaation mukaan käyttäen normaalia jakaumaa
technology_scores = norm.cdf(correlation_with_revenue)

# Laske Technology_General_Valence-pisteet
technology_median_score = np.median(technology_scores)
final_df.loc[:, 'Technology_General_Valence'] = final_df['Lists'].apply(lambda x: len(str(x).split(','))) + technology_median_score

# Laske Tech_Correlation_with_revenue vektorisoiduilla operaatioilla
tech_corr_matrix = final_df[unique_technologies_in_final_df].values * correlation_with_revenue.values
final_df.loc[:, 'Tech_Correlation_with_revenue'] = tech_corr_matrix.sum(axis=1)

# Luo teollisuuskorrelaatioiden sarakkeet vektorisoiduilla operaatioilla
final_df.loc[:, 'Industry_Correlation_with_revenue'] = final_df['Industry'].map(industry_correlation_corr.to_dict())
final_df.loc[:, 'Industry_Ranking'] = final_df['Industry'].map(industry_ranking)

# Sovella teknologiapisteet teknologiasarakkeisiin vektorisoiduilla operaatioilla
for tech in unique_technologies_in_final_df:
    final_df.loc[:, tech] *= technology_scores[unique_technologies_in_final_df.index(tech)]

# Laske keskimääräinen, maksimi-, minimi- ja mediaaniliikevaihto jokaiselle teknologialle
technology_stats = final_df.melt(id_vars=['Annual_Revenue'], value_vars=unique_technologies_in_final_df, var_name='Technology', value_name='Presence')
technology_stats = technology_stats[technology_stats['Presence'] > 0].groupby('Technology')['Annual_Revenue'].agg(['mean', 'max', 'min', 'median', 'count'])

# Laske keskimääräinen, maksimi-, minimi- ja mediaaniliikevaihto jokaiselle toimialalle
industry_stats = final_df.groupby('Industry')['Annual_Revenue'].agg(['mean', 'max', 'min', 'median', 'count'])

# Valitse ja järjestä vaaditut sarakkeet
final_df = final_df[['CompanyID', 'Annual_Revenue', 'Tech_Correlation_with_revenue', 'Industry_Correlation_with_revenue', 
                     'Technology_Count', 'Industry_Ranking', 'Technology_General_Valence'] + unique_technologies_in_final_df]

# Tallenna lopullinen DataFrame CSV-tiedostoon Power BI -analyysiä varten
final_df.to_csv('companies_technology_industry_scoring.csv', index=False)

# Valmistele korrelaatiotulokset DataFrame tilastojen kanssa
correlation_with_revenue_df = correlation_with_revenue.reset_index()
correlation_with_revenue_df.columns = ['Technology', 'Correlation_with_Revenue']
correlation_with_revenue_df = correlation_with_revenue_df.merge(technology_stats.reset_index(), on='Technology', how='left')
correlation_with_revenue_df.rename(columns={'mean': 'Average_Revenue', 'max': 'Max_Revenue', 'min': 'Min_Revenue', 'median': 'Median_Revenue', 'count': 'N'}, inplace=True)

# Tallenna korrelaatiotulokset CSV-tiedostoon
correlation_with_revenue_df.to_csv('technology_revenue_correlation_all.csv', index=False)

# Valmistele teollisuuskorrelaatiotulokset DataFrame tilastojen kanssa
industry_correlation_df = industry_correlation_corr.reset_index()
industry_correlation_df.columns = ['Industry', 'Correlation_with_Revenue']
industry_correlation_df = industry_correlation_df.merge(industry_stats.reset_index(), on='Industry', how='left')
industry_correlation_df.rename(columns={'mean': 'Average_Revenue', 'max': 'Max_Revenue', 'min': 'Min_Revenue', 'median': 'Median_Revenue', 'count': 'N'}, inplace=True)

# Tallenna teollisuuskorrelaatiotulokset CSV-tiedostoon
industry_correlation_df.to_csv('industry_revenue_correlation.csv', index=False)

# Tulosta lopullisen DataFramen ensimmäiset rivit
print("Final DataFrame for Power BI analysis:")
print(final_df.head())

# Tulosta korrelaatiotulokset
print("Correlation between Technologies and Annual Revenue:")
print(correlation_with_revenue_df)
print("Correlation between Industries and Annual Revenue:")
print(industry_correlation_df)

# Käännä lukemat suomeksi ja muotoile lukuarvot
correlation_with_revenue_df.columns = ['Teknologia', 'Korrelaatio_liikevaihtoon', 'Keskiarvo_liikevaihto', 'LiikevaihtoMAX', 'LiikevaihtoMIN', 'LiikevaihtoMedian', 'N']
industry_correlation_df.columns = ['Toimiala', 'Korrelaatio_liikevaihtoon', 'Keskiarvo_liikevaihto', 'LiikevaihtoMAX', 'LiikevaihtoMIN', 'LiikevaihtoMedian', 'N']

# Muotoile luvut luettavampaan muotoon
correlation_with_revenue_df['Keskiarvo_liikevaihto'] = correlation_with_revenue_df['Keskiarvo_liikevaihto'].apply(lambda x: f"{x:,.0f}")
correlation_with_revenue_df['LiikevaihtoMAX'] = correlation_with_revenue_df['LiikevaihtoMAX'].apply(lambda x: f"{x:,.0f}")
correlation_with_revenue_df['LiikevaihtoMIN'] = correlation_with_revenue_df['LiikevaihtoMIN'].apply(lambda x: f"{x:,.0f}")
correlation_with_revenue_df['LiikevaihtoMedian'] = correlation_with_revenue_df['LiikevaihtoMedian'].apply(lambda x: f"{x:,.0f}")

industry_correlation_df['Keskiarvo_liikevaihto'] = industry_correlation_df['Keskiarvo_liikevaihto'].apply(lambda x: f"{x:,.0f}")
industry_correlation_df['LiikevaihtoMAX'] = industry_correlation_df['LiikevaihtoMAX'].apply(lambda x: f"{x:,.0f}")
industry_correlation_df['LiikevaihtoMIN'] = industry_correlation_df['LiikevaihtoMIN'].apply(lambda x: f"{x:,.0f}")
industry_correlation_df['LiikevaihtoMedian'] = industry_correlation_df['LiikevaihtoMedian'].apply(lambda x: f"{x:,.0f}")

print("Teknologiat ja niiden korrelaatiot liikevaihtoon sekä keskiarvoinen liikevaihto:")
print(correlation_with_revenue_df)
print("Toimialat ja niiden korrelaatiot liikevaihtoon sekä keskiarvoinen liikevaihto:")
print(industry_correlation_df)
