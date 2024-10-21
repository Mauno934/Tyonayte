# Työnäyte Python / AI / Power BI / Azure Databricks (PySpark)

Ajattelin tutustua yhteen työpaikkakuvauksessa mainittuun teknologiaan ja tehdä sen ympärille monipuolisen työnäytteen. En voi muutenkaan jakaa työtä vaan suoraan sillä se olisi tietosuojan kannalta erittäin huono asia.
Visualisointi on uutta eikä sille ole niin ollut tarvetta nykyisessä työpaikassa, joten tämä on kokeiluna hyvin mielenkiintoinen ja opettava.
Sisällytin paljon omaa koodia tähän jotka loin aikapitkälti lennosta, ainoastaan tekoälyskripti oli aiempaa kokeilua. En myöskään liittänyt SQL suoraan vaan otin tietynlaisen samplen csv muodossa jotta en jakaisi rakenteita tai tietoa
jota ei haluattaisi jakaa. 

Työnäyteessä tehdyt osat eivät ole täydellisiä vaan niiden tarkoitus on luoda riittävän kattava kokonaisuus, aikaa minulla oli vain muutama päivä joten koodi voi osin myös näyttää siltä.

Koska dokumentti on hyvin laaja ja arviointiin ei välttämättä voi niin paljon aikaa käyttää, sisällytin keskeisiä skriptejä myös [Power BI osuuteen](#power-bi) jossa tulee tiivistetymmin asioita mutta kattaa eri osuuksia samanaikaisesti. Kohdassa [modernit tietokantaratkaisut tekoälyllä](#modernit-tietokantaratkaisut-tekoälyllä) esittelen myös yksinkertaista tekoälyratkaisua paljon käytetyissä Regex operaatioissa. Haastavimmat datan käsittelyt ja laskennat Pythonilla, sekä niiden visualisointi löytyvät ihan [lopusta](#monimutkainen-data-ja-lopullinen-työ). Lisäsin myös hieman [Azurea](#edistynyt-data-analyysi-sparkilla-ja-azurella) jossa teen asioita Databricksillä käyttäen PySpark, toteutan siinä samanlaisia ideoita mitä töissä on tullut vastaan mutta hieman eri suunnasta.

Tämän kokonaisuuden luominen oli erittäin mielenkiintoista ja innosti minua kehittymään monella osa-alueella. 



## Sisällysluettelo
- [Python](#Python)
  - [Osastojen analyysi pythonilla](#osastojen-analyysi-pythonilla)
    - [Datan esikäsittely](#datan-esikäsittely)
  - [Pisteytysjärjestelmän kehitys](#pisteytysjärjestelmän-kehitys)
    - [Datan pisteytys](#datan-pisteytys)
      - [Kontaktien pisteytys](#kontaktien-pisteytys)
      - [Yritysten pisteytys](#yritysten-pisteytys)
  - [Analyysi: teknologioiden ja toimialojen korrelaatio liikevaihtoon](#analyysi-teknologioiden-ja-toimialojen-korrelaatio-liikevaihtoon)
    - [Datasetin lataaminen ja esikäsittely](#datasetin-lataaminen-ja-esikäsittely)
    - [Teknologioiden erottelu ja lähtötietojen valmistelu](#teknologioiden-erottelu-ja-lähtötietojen-valmistelu)
    - [Teknologioiden lukumäärän laskenta yrityksille](#teknologioiden-lukumäärän-laskenta-yrityksille)
    - [Korrelaatioiden laskenta ja tulosten yhdistäminen](#korrelaatioiden-laskenta-ja-tulosten-yhdistäminen)
    - [Tilastot teknologioille ja toimialoille](#tilastot-teknologioille-ja-toimialoille)
    - [Lopullisten tulosten tallentaminen](#lopullisten-tulosten-tallentaminen)
    - [Tulosten tulostaminen ja muotoilu](#tulosten-tulostaminen-ja-muotoilu)
- [Modernit tietokantaratkaisut tekoälyllä](#modernit-tietokantaratkaisut-tekoälyllä)
  - [AI-vertailu: regex-työmäärän tarkastelu](#ai-vertailu-regex-työmäärän-tarkastelu)
    - [Tavallinen tapa](#tavallinen-tapa)
    - [Tekoälyversio](#tekoälyversio)
    - [Vertailu regex-työmäärästä](#vertailu-regex-työmäärästä)
      - [Perinteinen versio](#perinteinen-versio)
      - [Tekoälyversio](#tekoälyversio-1)
      - [Hybridiversio](#hybridiversio)
    - [Teknisiä osuuksia](#teknisiä-osuuksia)
- [Power BI](#power-bi)
  - [Datan formatointi ja visualisointi](#datan-formatointi-ja-visualisointi)
  - [Monimutkainen data ja lopullinen työ](#monimutkainen-data-ja-lopullinen-työ)
 - [Edistynyt data-analyysi PySparkilla ja Azurella](#edistynyt-data-analyysi-sparkilla-ja-azurella)







## Python
Ehdottomasti lempiohjelmointikieleni, dynaaminen ja nopea määrittely, tehokas. Aloitetaan esittelemällä Python kielen toteutuksia valmistaaksemme datasta visualisointeja.





### Osastojen analyysi pythonilla

#### Datan esikäsittely

Huomasin että Power BI pystyy moniin operaatioihin mutta on parasta luoda sille hyviä sampleja valmiiksi pythonilla jossa dataoperaatiot luistavat sulavasti. 
Aloitin mahdollisimman yksinkertaisesta mallista johon sitten lisäsin Power BI ymmärryksen kasvaessa monimutkaisuutta ja resoluutiota.
Käytin Pandas-kirjastoa osastodatan esikäsittelyyn ja analysointiin. Tämä sisälsi osastojen erittelyn ja kontaktien määrän laskemisen kullekin osastolle.

```python
import pandas as pd

# Lataa datasetti
contacts_df = pd.read_csv('data.csv')

# Eri osastojen erittely ja määrien laskeminen
departments = contacts_df['Departments'].str.split(',').explode()
department_counts = departments.value_counts()

# Luo yhteenvetotaulukko
department_summary = pd.DataFrame({
    'Department': department_counts.index,
    'Count': department_counts.values
})


```
<details>
  <summary>Osastojen edustus:</summary>
  
  **Jokaisen osaston edustajien määrät (Top 10 osastoa):**
  - Myynti: 3,911
  - Johto (C-Suite): 3,718
  - Tuote: 2,288
  - Markkinointi: 1,365
  - Operatiivinen toiminta: 1,227
  - Tekninen ja insinöörit: 1,174
  - Tietotekniikka: 1,119
  - Talous: 358
  - Henkilöstöhallinto: 330
  - Suunnittelu: 210

  **Mediaani- ja keskiarvoesiintymät per yritys:**
  
  **Top 10 osastojen mediaaniesiintymät per yritys:**
  - Myynti: 1.0
  - Johto (C-Suite): 1.0
  - Tuote: 1.0
  - Markkinointi: 1.0
  - Operatiivinen toiminta: 1.0
  - Tekninen ja insinöörit: 1.0
  - Tietotekniikka: 1.0
  - Talous: 1.0
  - Henkilöstöhallinto: 1.0
  - Suunnittelu: 1.0

  **Top 10 osastojen keskiarvoesiintymät per yritys:**
  - Myynti: 1.91
  - Johto (C-Suite): 1.34
  - Tuote: 2.71
  - Markkinointi: 1.41
  - Operatiivinen toiminta: 1.41
  - Tekninen ja insinöörit: 1.45
  - Tietotekniikka: 1.65
  - Talous: 1.28
  - Henkilöstöhallinto: 1.31
  - Suunnittelu: 1.31

</details>

<details>
  <summary>Osastojen edustus yli 1000 työntekijän yrityksissä:</summary>
  
  **Jokaisen osaston edustajien määrät (Top 10 osastoa):**
  - Tietotekniikka: 1,290
  - Tuote: 1,062
  - Myynti: 917
  - Tekninen ja insinöörit: 737
  - Operatiivinen toiminta: 430
  - Talous: 306
  - Markkinointi: 252
  - Johto (C-Suite): 198
  - Henkilöstöhallinto: 170
  - Lakiasiat: 63

  **Mediaani- ja keskiarvoesiintymät per yritys:**

  **Top 10 osastojen mediaaniesiintymät per yritys:**
  - Johto (C-Suite): 1.0
  - Tekninen ja insinöörit: 3.0
  - Talous: 2.0
  - Henkilöstöhallinto: 3.0
  - Tietotekniikka: 4.0
  - Lakiasiat: 1.0
  - Markkinointi: 2.0
  - Operatiivinen toiminta: 2.0
  - Tuote: 5.0
  - Myynti: 3.0

  **Top 10 osastojen keskiarvoesiintymät per yritys:**
  - Johto (C-Suite): 2.68
  - Tekninen ja insinöörit: 7.60
  - Talous: 5.46
  - Henkilöstöhallinto: 3.27
  - Tietotekniikka: 11.94
  - Lakiasiat: 2.52
  - Markkinointi: 3.76
  - Operatiivinen toiminta: 5.58
  - Tuote: 13.28
  - Myynti: 12.56

</details>

## Pisteytysjärjestelmän kehitys

### Datan pisteytys
Kehitin pisteytysjärjestelmän, joka ottaa huomioon eri tekijöitä kontaktien ja yritysten laadun arvioimiseksi. Käytin vektorisoituja operaatioita tehokkuuden parantamiseksi.

#### Kontaktien pisteytys
```python
contacts_df['Has_Proper_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & (~contacts_df['Last_Name'].str.contains(r'^\w\.$'))
contacts_df['Has_Abbreviated_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & contacts_df['Last_Name'].str.contains(r'^\w\.$')
contacts_df['Has_Proper_Title'] = contacts_df['Title'].notna() & (~contacts_df['Title'].str.contains(r'\bat\b|\b/\b'))
contacts_df['Company_Match'] = contacts_df['Account_Id'].map(company_name_mapping) == contacts_df['Company']
contacts_df['Email_Verified'] = contacts_df['Email_Status'] == 'Verified'
contacts_df['Seniority_Exists'] = contacts_df['Seniority'].notna()
contacts_df['Departments_Exists'] = contacts_df['Departments'].notna()

contacts_df['Score'] = (
    contacts_df['Has_Proper_Name'] * 2 +
    contacts_df['Has_Abbreviated_Name'] * 1 +
    contacts_df['Has_Proper_Title'] * 2 +
    contacts_df['Has_Separator_Title'] * 1 +
    contacts_df['Company_Match'].fillna(False) * 2 +
    (~contacts_df['Company_Match'].fillna(True)) & contacts_df['Company'].notna() * 1 +
    contacts_df['Email_Verified'] * 1 +
    contacts_df['Seniority_Exists'] * 1 +
    contacts_df['Departments_Exists'] * 1
)
```
#### Yritysten pisteytys
```python
companies_df['Contact_Company_Match'] = companies_df.apply(
    lambda row: row['Company'] in contact_company_names.get(row['Account_Id'], set()), axis=1
).astype(bool)
companies_df['Employees_Valid'] = companies_df['Number_of_Employees'].notna() & (companies_df['Number_of_Employees'] > 3)
companies_df['Industry_Exists'] = companies_df['Industry'].notna()
social_media_fields = ['Website', 'Company_Linkedin_Url', 'Facebook_Url', 'Twitter_Url']
companies_df['Social_Media_Count'] = companies_df[social_media_fields].notna().sum(axis=1)
location_fields = ['Company_Country', 'Company_City']
companies_df['Location_Count'] = companies_df[location_fields].notna().sum(axis=1)

companies_df['Score'] = (
    companies_df['Contact_Company_Match'].fillna(False) * 2 +
    (~companies_df['Contact_Company_Match'].fillna(True)) & companies_df['Company'].notna() * 1 +
    companies_df['Employees_Valid'] * 2 +
    companies_df['Industry_Exists'] * 1 +
    companies_df['Social_Media_Count'] * 0.5 +
    companies_df['Location_Count'] * 0.5
)
```
<details>
  <summary>Koko skripti</summary>

```python
import numpy as np

# Esilaskenta 
company_name_mapping = companies_df.set_index('Account_Id')['Company'].to_dict()

# Vektorisoitu pisteytys kontakteille
contacts_df['Has_Proper_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & (~contacts_df['Last_Name'].str.contains(r'^\w\.$'))
contacts_df['Has_Abbreviated_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & contacts_df['Last_Name'].str.contains(r'^\w\.$')

contacts_df['Has_Proper_Title'] = contacts_df['Title'].notna() & (~contacts_df['Title'].str.contains(r'\bat\b|\b/\b'))
contacts_df['Has_Separator_Title'] = contacts_df['Title'].notna() & contacts_df['Title'].str.contains(r'\bat\b|\b/\b')

contacts_df['Company_Match'] = contacts_df['Account_Id'].map(company_name_mapping) == contacts_df['Company']

contacts_df['Email_Verified'] = contacts_df['Email_Status'] == 'Verified'
contacts_df['Seniority_Exists'] = contacts_df['Seniority'].notna()
contacts_df['Departments_Exists'] = contacts_df['Departments'].notna()

contacts_df['Score'] = (
    contacts_df['Has_Proper_Name'] * 2 +
    contacts_df['Has_Abbreviated_Name'] * 1 +
    contacts_df['Has_Proper_Title'] * 2 +
    contacts_df['Has_Separator_Title'] * 1 +
    contacts_df['Company_Match'].fillna(False).astype(int) * 2 +
    (~contacts_df['Company_Match'].fillna(True)).astype(int) & contacts_df['Company'].notna().astype(int) * 1 +
    contacts_df['Email_Verified'].astype(int) * 1 +
    contacts_df['Seniority_Exists'].astype(int) * 1 +
    contacts_df['Departments_Exists'].astype(int) * 1
)

# Vektorisoitu pisteytys yrityksille
contact_company_names = contacts_df.groupby('Account_Id')['Company'].apply(set).to_dict()

companies_df['Contact_Company_Match'] = companies_df.apply(
    lambda row: row['Company'] in contact_company_names.get(row['Account_Id'], set()), axis=1
).astype(bool)
companies_df['Employees_Valid'] = companies_df['Number_of_Employees'].notna() & (companies_df['Number_of_Employees'] > 3)
companies_df['Industry_Exists'] = companies_df['Industry'].notna()
social_media_fields = ['Website', 'Company_Linkedin_Url', 'Facebook_Url', 'Twitter_Url']
companies_df['Social_Media_Count'] = companies_df[social_media_fields].notna().sum(axis=1)
location_fields = ['Company_Country', 'Company_City']
companies_df['Location_Count'] = companies_df[location_fields].notna().sum(axis=1)

# Lasketaan kokonaispistemäärä
companies_df['Score'] = (
    companies_df['Contact_Company_Match'].fillna(False).astype(int) * 2 +
    ((~companies_df['Contact_Company_Match'].fillna(True)).astype(int) & companies_df['Company'].notna().astype(int)) * 1 +
    companies_df['Employees_Valid'].astype(int) * 2 +
    companies_df['Industry_Exists'].astype(int) * 1 +
    companies_df['Social_Media_Count'] * 0.5 +
    companies_df['Location_Count'] * 0.5
)

# Näytetään tilastot pisteistä
contacts_score_stats = contacts_df['Score'].describe()
companies_score_stats = companies_df['Score'].describe()

contacts_score_stats, companies_score_stats
</details>

department_summary.to_csv('department_summary.csv', index=False)
```
</details>

<details>
  <summary>Pisteiden statistiikat</summary>

#### Kontaktien pisteiden statistiikat:
- Lukumäärä: 29,426
- Keskiarvo: 7.90
- Keskihajonta: 0.84
- Minimi: 5.00
- 25. prosenttipiste (Q1): 7.00
- Mediaani (Q2): 8.00
- 75. prosenttipiste (Q3): 8.00
- Maksimi: 9.00

#### Yritysten pisteiden statistiikat:
- Lukumäärä: 32,675
- Keskiarvo: 4.20
- Keskihajonta: 2.31
- Minimi: 0.00
- 25. prosenttipiste (Q1): 2.00
- Mediaani (Q2): 3.50
- 75. prosenttipiste (Q3): 6.50
- Maksimi: 8.00

#### Kontaktien pisteiden jakauma:
Histogrammi näyttää kontaktipisteiden esiintymistiheyden. Useimmilla kontakteilla on pisteet välillä 7 ja 9, mikä osoittaa, että suurimmalla osalla merkinnöistä on melko täydelliset tiedot.

![Kontaktien pisteiden jakauma](https://github.com/Mauno934/Tyonayte/blob/main/output%20(3).png?raw=true)

#### Yritysten pisteiden jakauma:
Histogrammi näyttää yrityspisteiden esiintymistiheyden. Pisteet ovat laajemmin jakautuneet, ja huomattava määrä yrityksiä saa alhaisemmat pisteet, mikä osoittaa, että näiden merkintöjen tiedot ovat puutteellisia. Kuitenkin 
puutteellisuus on verrattuna ideaaliseen dataan, ja on riippuvainen datan käyttötarkoituksesta tai esimerkiksi siitä onko paikka jossa data on välimuoto jollekin prosessille. 

![Yritysten pisteiden jakauma](https://github.com/Mauno934/Tyonayte/blob/main/output%20(2).png?raw=true)

Nämä kaaviot kuvaavat visuaalisesti datan laatua ja täydellisyyttä, korostaen alueita, joilla voidaan tehdä parannuksia. Myöskin kuvaavat preferenssejä datan rikastuksessa. 
</details>

## Analyysi: teknologioiden ja toimialojen korrelaatio liikevaihtoon

Tämä projekti analysoi, miten eri teknologiat ja toimialat korreloivat yritysten liikevaihtoon.

### Datasetin lataaminen ja esikäsittely

Lataa yritysten tiedot ja suodata ne, joilla on vuotuinen liikevaihto.

```python
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Lataa datasetit
companies_df = pd.read_csv("data.csv")

# Suodata yritykset, joilla on vuotuinen liikevaihto
companies_with_revenue_df = companies_df[companies_df['Annual_Revenue'].notna()].copy()
```
#### Teknologioiden erottelu ja lähtötietojen valmistelu

```python
# Erittele teknologiat yksittäisiksi kohteiksi
all_technologies = companies_with_revenue_df['Technologies'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
unique_technologies = all_technologies.unique()

# Luo dataframe teknologioiden läsnäololle (1) tai poissaololle (0)
technology_presence_df = pd.get_dummies(all_technologies, prefix='', prefix_sep='').groupby(level=0).max()

# Tasoita sarakkeet varmistaaksesi, että kaikki ainutlaatuiset teknologiat ovat läsnä
technology_presence_df = technology_presence_df.reindex(columns=unique_technologies, fill_value=0)
```
#### Teknologioiden lukumäärän laskenta yrityksille

```python
# Laske teknologioiden lukumäärä kullekin yritykselle
companies_with_revenue_df['Technology_Count'] = technology_presence_df.sum(axis=1)

# Valitse lopullisen dataframen relevantit sarakkeet
final_df = companies_with_revenue_df[['CompanyID', 'Annual_Revenue', 'Industry', 'Technology_Count', 'Lists']].copy()
final_df = pd.concat([final_df.reset_index(drop=True), technology_presence_df], axis=1)
```
#### Korrelaatioiden laskenta ja tulosten yhdistäminen
```python
# Varmistetaan, että kaikki unique_technologies -elementit ovat final_df -dataframessa
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

# Arvota teknologiat niiden liikevaihtokorrelaation mukaan käyttäen normaalijakaumaa
technology_scores = norm.cdf(correlation_with_revenue)

# Laske technology_general_valence-pisteet
technology_median_score = np.median(technology_scores)
final_df.loc[:, 'Technology_General_Valence'] = final_df['Lists'].apply(lambda x: len(str(x).split(','))) + technology_median_score

# Laske tech_correlation_with_revenue vektorisoiduilla operaatioilla
tech_corr_matrix = final_df[unique_technologies_in_final_df].values * correlation_with_revenue.values
final_df.loc[:, 'Tech_Correlation_with_revenue'] = tech_corr_matrix.sum(axis=1)

# Luo teollisuuskorrelaatioiden sarakkeet vektorisoiduilla operaatioilla
final_df.loc[:, 'Industry_Correlation_with_revenue'] = final_df['Industry'].map(industry_correlation_corr.to_dict())
final_df.loc[:, 'Industry_Ranking'] = final_df['Industry'].map(industry_ranking)

# Sovella teknologiapisteet teknologiasarakkeisiin vektorisoiduilla operaatioilla
for tech in unique_technologies_in_final_df:
    final_df.loc[:, tech] *= technology_scores[unique_technologies_in_final_df.index(tech)]
```
#### Tilastot teknologioille ja toimialoille
```python
# Laske keskimääräinen, maksimi-, minimi- ja mediaaniliikevaihto jokaiselle teknologialle
technology_stats = final_df.melt(id_vars=['Annual_Revenue'], value_vars=unique_technologies_in_final_df, var_name='Technology', value_name='Presence')
technology_stats = technology_stats[technology_stats['Presence'] > 0].groupby('Technology')['Annual_Revenue'].agg(['mean', 'max', 'min', 'median', 'count'])

# Laske keskimääräinen, maksimi-, minimi- ja mediaaniliikevaihto jokaiselle toimialalle
industry_stats = final_df.groupby('Industry')['Annual_Revenue'].agg(['mean', 'max', 'min', 'median', 'count'])
```
#### Lopullisten tulosten tallentaminen
```python
# Valitse ja järjestä vaaditut sarakkeet
final_df = final_df[['CompanyID', 'Annual_Revenue', 'Tech_Correlation_with_revenue', 'Industry_Correlation_with_revenue', 
                     'Technology_Count', 'Industry_Ranking', 'Technology_General_Valence'] + unique_technologies_in_final_df]

# Tallenna lopullinen dataframe csv-tiedostoon power bi -analyysiä varten
final_df.to_csv('companies_technology_industry_scoring.csv', index=False)

# Valmistele korrelaatiotulokset dataframe tilastojen kanssa
correlation_with_revenue_df = correlation_with_revenue.reset_index()
correlation_with_revenue_df.columns = ['Technology', 'Correlation_with_Revenue']
correlation_with_revenue_df = correlation_with_revenue_df.merge(technology_stats.reset_index(), on='Technology', how='left')
correlation_with_revenue_df.rename(columns={'mean': 'Keskiarvo_liikevaihto', 'max': 'LiikevaihtoMAX', 'min': 'LiikevaihtoMIN', 'median': 'LiikevaihtoMedian', 'count': 'N'}, inplace=True)

# Tallenna korrelaatiotulokset csv-tiedostoon
correlation_with_revenue_df.to_csv('technology_revenue_correlation_all.csv', index=False)

# Valmistele teollisuuskorrelaatiotulokset dataframe tilastojen kanssa
industry_correlation_df = industry_correlation_corr.reset_index()
industry_correlation_df.columns = ['Industry', 'Correlation_with_Revenue']
industry_correlation_df = industry_correlation_df.merge(industry_stats.reset_index(), on='Industry', how='left')
industry_correlation_df.rename(columns={'mean': 'Keskiarvo_liikevaihto', 'max': 'LiikevaihtoMAX', 'min': 'LiikevaihtoMIN', 'median': 'LiikevaihtoMedian', 'count': 'N'}, inplace=True)

# Tallenna teollisuuskorrelaatiotulokset csv-tiedostoon
industry_correlation_df.to_csv('industry_revenue_correlation.csv', index=False)
```
#### Tulosten tulostaminen ja muotoilu
```python
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
```
<details>
    <summary>Lambda-funktioiden selitykset:</summary>

#### Keskiarvo_liikevaihto:

```python
correlation_with_revenue_df['Keskiarvo_liikevaihto'] = correlation_with_revenue_df['Keskiarvo_liikevaihto'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'Keskiarvo_liikevaihto' arvot tuhaterotinpilkuilla ja ilman desimaaleja, mikä tekee arvoista luettavampia.



#### Liikevaihtomax:

```python
correlation_with_revenue_df['LiikevaihtoMAX'] = correlation_with_revenue_df['LiikevaihtoMAX'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'LiikevaihtoMAX' arvot samalla tavalla, käyttäen tuhaterotinpilkkuja ja poistamalla desimaalit.

#### Liikevaihtomin:

```python
correlation_with_revenue_df['LiikevaihtoMIN'] = correlation_with_revenue_df['LiikevaihtoMIN'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'LiikevaihtoMIN' arvot kuten edellä, parantaen luettavuutta.

#### Liikevaihtomedian:



```python
correlation_with_revenue_df['LiikevaihtoMedian'] = correlation_with_revenue_df['LiikevaihtoMedian'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'LiikevaihtoMedian' arvot tuhaterotinpilkuilla ja ilman desimaaleja.

#### Keskiarvo_liikevaihto (toimialat):



```python
industry_correlation_df['Keskiarvo_liikevaihto'] = industry_correlation_df['Keskiarvo_liikevaihto'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'Keskiarvo_liikevaihto' arvot tuhaterotinpilkuilla ja ilman desimaaleja, toimialakohtaisesti.

#### Liikevaihtomax (toimialat):



```python
industry_correlation_df['LiikevaihtoMAX'] = industry_correlation_df['LiikevaihtoMAX'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'LiikevaihtoMAX' arvot samalla tavalla, toimialakohtaisesti.

#### Liikevaihtomin (toimialat):



```python
industry_correlation_df['LiikevaihtoMIN'] = industry_correlation_df['LiikevaihtoMIN'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'LiikevaihtoMIN' arvot kuten edellä, toimialakohtaisesti.

#### Liikevaihtomedian (toimialat):



```python
industry_correlation_df['LiikevaihtoMedian'] = industry_correlation_df['LiikevaihtoMedian'].apply(lambda x: f"{x:,.0f}")
```
Tämä lambda-funktio muotoilee sarakkeen 'LiikevaihtoMedian' arvot tuhaterotinpilkuilla ja ilman desimaaleja, toimialakohtaisesti.

#### Technology_general_valence:

```python
final_df.loc[:, 'Technology_General_Valence'] = final_df['Lists'].apply(lambda x: len(str(x).split(','))) + technology_median_score
```
Tämä lambda-funktio laskee sarakkeen 'Technology_General_Valence' arvot laskemalla, kuinka monta kertaa kukin teknologia esiintyy 'Lists'-sarakkeessa ja lisäämällä siihen 'technology_median_score' -arvon. Tämä antaa yleisen arvion teknologian yleisyydestä ja merkityksestä.
</details>

# Modernit tietokantaratkaisut tekoälyllä
Tekoäly tuo uusia mahdollisuuksia teknologisille toteutuksille, erityisesti tietokannoissa. Tarkastellaan säännöllisten lausekkeiden määrän ja tarpeen muutoksia esimerkkiskriptissä.


## Ai-vertailu: regex-työmäärän tarkastelu
Tässä vertailussa otamme käytännön toteutuksen OpenAI API:sta yhdistettynä Bing search API:iin. Skriptit ovat tehtyjä tutkimustarkoitukseen ja käyttävät snippettejä bing hausta eivätkä mene sivuille itsessään. 

#### Tavallinen tapa
```python
regex_patterns = [
    r"liikevaihto oli ([\d\s,]+(\.\d{1,2})? [a-zA-Z]+)",  
    r"Liikevaihto \(tuhatta euroa\) [\d\s:]*?(\d+): Liikevaihdon muutos",
    r"liikevaihto oli ([\d\s,]+(\.\d{1,2})? [a-zA-Z]+)",
    r"Liikevaihto \(tuhatta euroa\) [\d\s:]*?(\d+): Liikevaihdon muutos",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+(\.\d{1,2})? [a-zA-Z]+)",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ t\. €)",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ milj\. €)",
    r"Liikevaihto ([\d\s,]+ milj\. €)",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ t\. €) ja liikevaihdon muutos",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ €) ja henkilöstömäärä",
    r"Taloustiedot\. Liikevaihto\. ([\d\s,]+ milj\. €)"
]
```
Tästä löytyy jo jonkinverran regexiä, ja kun ottaa huomioon esimerkiksi tilanteen jossa verrataan silmukassa parhaita ehdokkaita, regexin käyttäminen datan arviointiin on huomattavasti työläämpi ja vaatii paljon kehitystä.
Jos myös verrataan tilanteeseen jossa AI valitsee oikean ehdokkaan ja tekee arvion sekä luo listan tiedoista, listan järjestyksen vastaus ei tekoälyn luonteesta johtuen aina ole oikea, mutta pienellä määrällä Regex funktioita
pystytään asia korjaamaan. 

#### Tekoälyversio
Määritellään sarakkeet

```python
# Jäsennä taloudellinen tieto
def parse_financial_info(financial_info):
    # Luodaan lista vakioarvoilla
    parsed_data = {
        "Revenue": "N/A",
        "Revenue Change": "N/A",
        "Annual Profit": "N/A",
        "CEO": "N/A",
        "Founding Year": "N/A"
    }
    
    # Uusi rivi määrittelee datan parseemisen
    info_list = financial_info.split("\n")
    
    # Tarkista onko pituus oikein
    if len(info_list) >= 5:
        parsed_data["Revenue"] = info_list[0].strip()
        parsed_data["Revenue Change"] = info_list[1].strip()
        parsed_data["Annual Profit"] = info_list[2].strip()
        parsed_data["CEO"] = info_list[3].strip()
        parsed_data["Founding Year"] = info_list[4].strip()
    else:
        # Jos pituus ei ole oikein tai järjestys, todo: laitetaan regex sekä paremmat tunnistukset virheellisistä tiedoista
        print("Warning: Incomplete financial information received.")
        
    return parsed_data
```



Tekoälyn käyttö oikean datan valinnassa mahdollistaa sen että laittaa loogisia parametrejä, joita tekoäly voi käyttää tietona sekä itse tekoälyn päättelykyvyn

```python
# Tarkista onko sana erillinen tekstissä
def is_distinct_word_in_text(word, text):
    pattern = r'\b' + re.escape(word) + r'\b'
    return re.search(pattern, text, re.IGNORECASE) is not None

# Analysoi ja tallenna tiedot
def analyze_and_store_data(data, company):
    candidates = []
    try:
        for result in data['webPages']['value']:
            url = result['url']
            if any(site in url for site in ['finder.fi', 'asiakastieto.fi', 'vainu.io']):
                anchor_text = result['name']
                snippet = result['snippet']
                if is_distinct_word_in_text(company, anchor_text):
                    candidates.append(snippet)
        
        if candidates:
            best_candidate = select_best_candidate(candidates)
            financial_info = analyze_snippet(best_candidate)
            parsed_data = parse_financial_info(financial_info)
            store_data_in_workbook(company, parsed_data)
    except KeyError:
        with workbook_lock:
            ws.append([company, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
```
Tekoäly valitsee parhaan ehdokkaan

```python
def select_best_candidate(candidates):
    global last_openai_request_time
    last_openai_request_time = rate_limit(last_openai_request_time, time_between_requests)
    
    prompt = "Given the following financial snippets, which one is most likely to be the correct company?\n"
    for i, candidate in enumerate(candidates):
        prompt += f"{i+1}. {candidate}\n"
    
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=50  # Kasvata token-rajoitusta, jotta saadaan koko vastaus
        )
        
        # Pura mallin vastauksesta valinta
        text_response = response['choices'][0]['text'].strip()
        choice_match = re.search(r'\d+', text_response)
        
        #Jos löytyy numero, käytä sitä valintana
        if choice_match:
            choice = int(choice_match.group()) - 1  # Muuta yksipohjaiseksi indeksiksi
            return candidates[choice]
        else:
            print(f"Unexpected response format: {text_response}")
            return candidates[0]  # Jos vastausformaatti on odottamaton, tulosta virhe ja palauta ensimmäinen ehdokas (ehkä ei paras idea)
```

Tekoäly analysoi valitsemansa katkealman ja purkaa tiedot järjestyksessä johon on varmistusmekanismeja

```python
# Analysoi tekstikatkelma
def analyze_snippet(snippet):
    global last_openai_request_time
    last_openai_request_time = rate_limit(last_openai_request_time, time_between_requests)
    
    prompt = f"Extract the following financial information from the snippet: {snippet}. Please provide the latest information in the following order: 1. Revenue (only numbers), 2. Revenue Change(+/- value), 3. Annual Profit (+/- value), 4. CEO, 5. Founding Year."
    
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100  # Säätövaraa
        )
        
        if 'choices' in response and 'text' in response['choices'][0]:
            financial_info = response['choices'][0]['text'].strip()
            return financial_info  # Tässä taloustietojen toivon mukaan pitäisi olla oikeassa järjestyksessä
        else:
            print("Unexpected response format.")
            return None
            
    except (Exception, openai.error.InvalidRequestError) as e:  # Openai yleiset virheet
        print(f"API Request failed: {e}")
        return None
```

Hybridi rajaus voisi olla esimerkiksi tällainen 

```python
def select_best_candidate(candidates):
    global last_openai_request_time
    last_openai_request_time = rate_limit(last_openai_request_time, time_between_requests)
    
    prompt = "Given the following financial snippets, which one is most likely to be the correct company?\n"
    for i, candidate in enumerate(candidates):
        prompt += f"{i+1}. {candidate}\n"
    
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=50  # Kasvata token-rajoitusta, jotta saadaan koko vastaus
        )
        
        # Pura mallin vastauksesta valinta
        text_response = response['choices'][0]['text'].strip()
        choice_match = re.search(r'\d+', text_response)
        
        #Jos löytyy numero, käytä sitä valintana
        if choice_match:
            choice = int(choice_match.group()) - 1  # Muuta yksipohjaiseksi indeksiksi
            return candidates[choice]
        else:
            print(f"Unexpected response format: {text_response}")
            return candidates[0]  # Jos vastausformaatti on odottamaton, tulosta virhe ja palauta ensimmäinen ehdokas (ehkä ei paras idea)
```
Valinnan jälkeen käytetään regex

```python
def search_info(company, search_type, site):
#API määrittely...

regex_patterns = [
    r"liikevaihto oli ([\d\s,]+(\.\d{1,2})? [a-zA-Z]+)",  # Alkuperäinen regex
    r"Liikevaihto \(tuhatta euroa\) [\d\s:]*?(\d+): Liikevaihdon muutos",  # Uusi regex
    r"liikevaihto oli ([\d\s,]+(\.\d{1,2})? [a-zA-Z]+)",
    r"Liikevaihto \(tuhatta euroa\) [\d\s:]*?(\d+): Liikevaihdon muutos",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+(\.\d{1,2})? [a-zA-Z]+)",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ t\. €)",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ milj\. €)",
    r"Liikevaihto ([\d\s,]+ milj\. €)",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ t\. €) ja liikevaihdon muutos",
    r"liikevaihto oli edellisenä tilikautena ([\d\s,]+ €) ja henkilöstömäärä",
    r"Taloustiedot\. Liikevaihto\. ([\d\s,]+ milj\. €)"
]

best_info_with_data = None  # Paras osuma, joka sisältää "liikevaihto" ja siihen liittyvän datan
best_info_without_data = None  # Paras osuma, joka sisältää "liikevaihto" mutta ei dataa
fallback_info = None  # Varatieto, jos "liikevaihto" ei löydy

# Käydään läpi hakutulokset
for result in results.get("webPages", {}).get("value", []):
    snippet = result.get("snippet", "")  # Ote tekstistä
    anchor_text = result.get("name", "")  # Sivun otsikko
    
    # Tarkistetaan, sisältääkö sivun otsikko yrityksen nimen
    if is_distinct_word_in_text(preprocess_company_name(company).lower(), anchor_text.lower()):
        for regex in regex_patterns:
            match = re.search(regex, snippet)  # Etsitään regex osumia otteesta
            if match:
                break  # Lopetetaan silmukka, kun osuma löytyy
        
        # Tarkistetaan, sisältääkö ote "liikevaihto"
        if "liikevaihto" in snippet.lower():
            if match:
                best_info_with_data = (match.group(1) if search_type == "Liikevaihto" else match.group(0)), snippet, anchor_text
            elif not best_info_without_data:
                best_info_without_data = "Sisältää liikevaihto mutta ei dataa", snippet, anchor_text
        elif not fallback_info:
            fallback_info = "Sivu olemassa, mutta ei liikevaihto tietoa", snippet, anchor_text

# Palautetaan paras osuma, varatieto tai tyhjä arvo
return best_info_with_data if best_info_with_data else (best_info_without_data if best_info_without_data else (fallback_info if fallback_info else (None, "", "")))

```
### Vertailu regex-työmäärästä:

#### Perinteinen versio:
- Sisältää yhteensä 11 regex-kuviota, jotka on suunniteltu tunnistamaan erilaisia liikevaihtoon liittyviä ilmaisuja.
- Vertailussa voi tulla potentiaalisesti monia erilaisia ilmaisutapoja sekä samoilla sivuilla niin myöskin eri sivuilla
- Regex-kuviot ovat monimutkaisempia ja kattavat useita erilaisia tapoja ilmaista liikevaihto, kuten tuhannet eurot, miljoonat eurot, ja liikevaihdon muutos.
- Regex-työmäärä on huomattavasti suurempi, koska se käsittelee useita eri muotoisia ja monimutkaisia liikevaihtoon liittyviä lauseita.
- Skripti tällaisenaan tuskin kattaa mitenkään hyvin käyttötarkoitusta
- Edullisempi

#### Tekoälyversio:
- Ainoastaan datan esikäsittelyyn sekä oikeellisuuden tarkastamiseen tarvittavia regex lauseita.
- Melko vakaa formaatti joka kehittyy mallien kehittyessä
- Käyttötarkoitusta ja analyysia helpompi laajentaa
- Kalliimpi

#### Hybridiversio:
- Etuna on kontekstin tehokkaampi rajaus, ja api kutsut vähenevät OpenAI:lle.
- Laaduntakaaminen ratkaisussa, kustannusten hallinta. 

Nämä ovat vain esimerkkitoteutuksia yleisestä loogisesta ajattelusta mitä kuuluu tekoälyratkaisuihin, hyötyjen arviointiin suhteessa kustannukiin. Pitkään minua on myös innostanut idea jossa tekoäly pyrkisi syvällisempään
ymmärrykseen esimerkiksi asiakkaan tarpeista, mahdollisista parhaista asiakkaista tai toimenpiteistä heidän nykyisessä tilanteessaan. 


# Power BI

### Datan formatointi ja visualisointi

Kun ensimmäisen kerran avasin Power BI:n päätin laittaa sinne tietokannan laajoja osuuksia csv muodossa. Ratkaisu ei ollut elegantein mahdollinen mutta opin käyttämään ohjelmaa mielestäni melko hyvin lyhyessä ajassa. Kuitenkin huomatessani DAX-kaavojen rajoitukset, päätin esikäsitellä dataa pythonilla. Aiemmin tuotokset tekoälyratkaisua mukaan lukematta ovat suunnattu nimenomaan dataksi Power BI:hin. Jotkut ovat vieläkin liian isoja tai huonosti muotoiltuja
näytteitä mutta niistä voi luoda uusia sopivampia osia. Tuotin ideat lennosta joten todennäköisyys että sain aikaiseksi todella hyvin kuvaavaa dataa ja uskomattomia visuaaleja on melko olematon. Ideana tässä oli näyttää että olen valmis
omaksumaan teknlogioita nopeasti ja erittäin kiinnostunut työskentelemään sen eteen.

Sain kuitenkin opeteltua melko paljon erilaista käsittelyä visualisoinnissa ja osaan tehdä sitä tehokkaasti. Joissain töissä joita tässä esittelen painottuu alustava käsittely pythonilla, joissain yksinkertainen tapa kuvata dataa ja ilmiöitä sekä myös DAX kaavojen soveltaminen. Työni visuaalinen puoli on katsottavissa tarkemmin upotettuna Power BI:nä linkistä: https://mauno934.github.io/Tyonayte/ mutta tässä käyn läpi suurimman osan noista ja myös enemmän joitain teknisia toteutuksia joita upotetussa näytteessä ei ole.


Aiemmin esittelin kahden kokoista datasamplea osastoista, Top 10 osastoa esiintyvyydeltä sekä Top 10 Osastoa pelkästään yli tuhannen henkilön yrityksissä. Toin näistä tiedostot Power BI työpöytäsovellukseen ja aloin luoda graafista esitystä. Loin Clustered Bar Chartin jossa osastot näkyvät Y-akselilla ja eri arvot X akselilla, siistin taulukkoa monella eri tavalla ja kokeilin eri asioita. 
Toteutusta varten käytin DAX-kieltä luodakseni yhdistetyn taulukon yhdistääkseni osastot ja myös testatakseni Power BI kykyä luoda normaalijakauma ilman lisäosia tai Python visualizeria. 
<details>
    <summary>Koodi</summary>

```dax
CombinedTable = 
UNION(
    SELECTCOLUMNS(
        Top_10_Departments_Counts,
        "Department1", Top_10_Departments_Counts[Department],
        "Department2", BLANK(),
        "DepartmentMerged", Top_10_Departments_Counts[Department],
        "Value", Top_10_Departments_Counts[Count],
        "Count1", Top_10_Departments_Counts[Count],
        "Count2", BLANK(),
        "NormalValue1", BLANK(),
        "NormalValue2", BLANK(),
        "NormalValueMerged", BLANK()
    ),
    SELECTCOLUMNS(
        NormalDistributionTable1,
        "Department1", BLANK(),
        "Department2", BLANK(),
        "DepartmentMerged", BLANK(),
        "Value", [Value],
        "Count1", BLANK(),
        "Count2", BLANK(),
        "NormalValue1", [NormalValue],
        "NormalValue2", BLANK(),
        "NormalValueMerged", [NormalValue]
    ),
    SELECTCOLUMNS(
        Top_10_Departments_Counts___1000_Employees_,
        "Department1", BLANK(),
        "Department2", Top_10_Departments_Counts___1000_Employees_[Department],
        "DepartmentMerged", Top_10_Departments_Counts___1000_Employees_[Department],
        "Value", Top_10_Departments_Counts___1000_Employees_[Count],
        "Count1", BLANK(),
        "Count2", Top_10_Departments_Counts___1000_Employees_[Count],
        "NormalValue1", BLANK(),
        "NormalValue2", BLANK(),
        "NormalValueMerged", BLANK()
    ),
    SELECTCOLUMNS(
        NormalDistributionTable2,
        "Department1", BLANK(),
        "Department2", BLANK(),
        "DepartmentMerged", BLANK(),
        "Value", [Value],
        "Count1", BLANK(),
        "Count2", BLANK(),
        "NormalValue1", BLANK(),
        "NormalValue2", [NormalValue2],
        "NormalValueMerged", [NormalValue2]
    )
)

// Normaalijakauman määrittelyt
NormalDistributionTable1 = 
VAR Mean1 = [MeanCount]
VAR StdDev1 = [StdDevCount]
VAR ScalingFactor = 10000  // skaalauskerroin
RETURN 
ADDCOLUMNS(
    GENERATESERIES(Mean1 - 4 * StdDev1, Mean1 + 4 * StdDev1, StdDev1 / 10),
    "NormalValue", 
    (ScalingFactor * (1 / (StdDev1 * SQRT(2 * PI()))) * EXP(-0.5 * (([Value] - Mean1) / StdDev1) ^ 2))
)
MeanCount = CALCULATE(AVERAGE(Top_10_Departments_Counts[Count]))
StdDevCount = CALCULATE(STDEV.P(Top_10_Departments_Counts[Count]))
```
</details>
Normaalijakauma onnistui lopulta, vaikka ei ole tässä esimerkissä kuvaavin, niin pääsin oppimaan paljon Power BI:n käytöstä.

Yksi normaalijakauma yksillä osastoarvoilla
![Screenshot 2024-08-02 233408](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-02%20233408.png?raw=true)

Kaksi rinnakkaista normaalijakaumaa sekä yhdistetty normaalijakauma molemmilla osastoarvoilla
![Screenshot 2024-08-03 003855](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-03%20003855.png?raw=true)

![Screenshot 2024-08-03 004703](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-03%20004703.png?raw=true)

### Datakoherenssi dashboard sekä liikevaihdon korrelaatio teknologiaan
Tämä dashboard näyttää erikoiselta koska siinä on mitattu erilaisia asioita joidenka yhteyttä ei välttämättä heti näe. Ideana on tarkistaa linketetyn datan määrä sekä datapisteiden laadullisuus. Samalla on pienempi ennustin
joka on näistä riippuvainen. Ennustimen tulokset ovat hieman erikoisia (tietysti näyteotos on myös ilmeisen pieni, ja random sattui myös poimimaan lithium akkuteknologian kaikista mahdollisuuksista...)
![Dashboard](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-03%20172210.png?raw=true)
<details>
  <summary>Korrelaatiovertailu pythonilla</summary>

  ```python
  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ladataan datasetit
companies_df = pd.read_csv("data.csv")  

# Suodatetaan yritykset, joilla on vuosiliikevaihto saatavilla
companies_with_revenue_df = companies_df[companies_df['Annual_Revenue'].notna()]

# Pilkotaan teknologiat 15 yleisimpään ja valitaan 15 satunnaista
all_technologies = companies_with_revenue_df['Technologies'].str.split(',', expand=True).stack()
top_15_technologies = all_technologies.value_counts().head(15).index.tolist()
remaining_technologies = all_technologies.value_counts().tail(len(all_technologies.unique()) - 15)
random_15_technologies = remaining_technologies.sample(15, random_state=42).index.tolist()

# Luodaan dataframe teknologiakohtaiselle läsnäololle
technology_columns = top_15_technologies + random_15_technologies
for tech in technology_columns:
    companies_with_revenue_df[tech] = companies_with_revenue_df['Technologies'].apply(lambda x: tech in str(x).split(','))

# Valitaan vain tarvittavat sarakkeet csv-tiedostoa varten
power_bi_ready_df = companies_with_revenue_df[['Account_Id', 'Company', 'Annual_Revenue'] + technology_columns]

# Tallennetaan power bi -valmis dataframe csv-tiedostoon
power_bi_ready_df.to_csv('power_bi_ready_technology_revenue.csv', index=False)

# Lasketaan korrelaatio kunkin teknologian läsnäolon ja vuosiliikevaihdon välillä
correlation_with_revenue = power_bi_ready_df[technology_columns + ['Annual_Revenue']].corr()['Annual_Revenue'].drop('Annual_Revenue')

# Jaetaan korrelaatiot top 15 ja satunnaiseen 15
correlation_top_15 = correlation_with_revenue.loc[top_15_technologies]
correlation_random_15 = correlation_with_revenue.loc[random_15_technologies]

# Tallennetaan korrelaatiotulokset csv-tiedostoon
correlation_with_revenue.to_csv('technology_revenue_correlation.csv', header=['Correlation_with_Revenue'])

# Tulostetaan korrelaatiotulokset
print("Korrelaatio Top 15 Teknologioiden ja Vuosiliikevaihdon välillä:")
print(correlation_top_15)
print("\nKorrelaatio Satunnaisen 15 Teknologian ja Vuosiliikevaihdon välillä:")
print(correlation_random_15)

# Yhdistetään tulokset vertailua varten
comparison_df = pd.DataFrame({
    'Technology': top_15_technologies + random_15_technologies,
    'Correlation_with_Revenue': list(correlation_top_15) + list(correlation_random_15),
    'Type': ['Top 15'] * len(correlation_top_15) + ['Random 15'] * len(correlation_random_15)
})

# Tallennetaan yhdistetyt vertailutulokset csv-tiedostoon
comparison_df.to_csv('technology_revenue_comparison.csv', index=False)

# Piirretään vertailu
plt.figure(figsize=(12, 8))
comparison_df.set_index('Technology')['Correlation_with_Revenue'].plot(kind='bar', color=['blue' if x == 'Top 15' else 'orange' for x in comparison_df['Type']])
plt.title('Korrelaatio Teknologioiden ja Vuosiliikevaihdon Välillä')
plt.xlabel('Teknologia')
plt.ylabel('Korrelaatio Vuosiliikevaihdon kanssa')
plt.xticks(rotation=90)
plt.legend(['Top 15', 'Satunnainen 15'])
plt.grid(True)
plt.tight_layout()
plt.show()
```
</details>

<details>
    <summary>DAX koodi</summary>
  
  ```dax 
ContactsWithMatchingID = 
CALCULATE(
COUNTROWS(Contacts),
Contacts[HasMatchingCompany] = 1
)
TotalContacts = COUNTROWS(Contacts)
```
</details>

<details>
    <summary>Datan pisteitys pythonilla</summary>
    
  ```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ladataan datasetit
contacts_df = pd.read_csv(data.csv")
companies_df = pd.read_csv("data.csv")

# Esilasketaan tarvittavat mappingit
company_name_mapping = companies_df.set_index('Account_Id')['Company'].to_dict()

# Vektorisoitu pisteytys kontakteille
contacts_df['Has_Proper_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & (~contacts_df['Last_Name'].fillna('').str.contains(r'^\w\.$'))
contacts_df['Has_Abbreviated_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & contacts_df['Last_Name'].fillna('').str.contains(r'^\w\.$')

contacts_df['Has_Proper_Title'] = contacts_df['Title'].notna() & (~contacts_df['Title'].fillna('').str.contains(r'\bat\b|\b/\b'))
contacts_df['Has_Separator_Title'] = contacts_df['Title'].notna() & contacts_df['Title'].fillna('').str.contains(r'\bat\b|\b/\b')

contacts_df['Company_Match'] = contacts_df['Account_Id'].map(company_name_mapping) == contacts_df['Company']

contacts_df['Email_Verified'] = contacts_df['Email_Status'] == 'Verified'
contacts_df['Seniority_Exists'] = contacts_df['Seniority'].notna()
contacts_df['Departments_Exists'] = contacts_df['Departments'].notna()

contacts_df['Score'] = (
    contacts_df['Has_Proper_Name'] * 2 +
    contacts_df['Has_Abbreviated_Name'] * 1 +
    contacts_df['Has_Proper_Title'] * 2 +
    contacts_df['Has_Separator_Title'] * 1 +
    contacts_df['Company_Match'].fillna(False).astype(int) * 2 +
    ((~contacts_df['Company_Match'].fillna(True)).astype(int) & contacts_df['Company'].notna().astype(int)) * 1 +
    contacts_df['Email_Verified'].astype(int) * 1 +
    contacts_df['Seniority_Exists'].astype(int) * 1 +
    contacts_df['Departments_Exists'].astype(int) * 1
)

# Vektorisoitu pisteytys yrityksille
contact_company_names = contacts_df.groupby('Account_Id')['Company'].apply(set).to_dict()

companies_df['Contact_Company_Match'] = companies_df.apply(
    lambda row: row['Company'] in contact_company_names.get(row['Account_Id'], set()), axis=1
).astype(bool)
companies_df['Employees_Valid'] = companies_df['Number_of_Employees'].notna() & (companies_df['Number_of_Employees'] > 3)
companies_df['Industry_Exists'] = companies_df['Industry'].notna()
social_media_fields = ['Website', 'Company_Linkedin_Url', 'Facebook_Url', 'Twitter_Url']
companies_df['Social_Media_Count'] = companies_df[social_media_fields].notna().sum(axis=1)
location_fields = ['Company_Country', 'Company_City']
companies_df['Location_Count'] = companies_df[location_fields].notna().sum(axis=1)

# Lasketaan kokonaispisteet
companies_df['Score'] = (
    companies_df['Contact_Company_Match'].fillna(False).astype(int) * 2 +
    ((~companies_df['Contact_Company_Match'].fillna(True)).astype(int) & companies_df['Company'].notna().astype(int)) * 1 +
    companies_df['Employees_Valid'].astype(int) * 2 +
    companies_df['Industry_Exists'].astype(int) * 1 +
    companies_df['Social_Media_Count'] * 0.5 +
    companies_df['Location_Count'] * 0.5
)

# Näytetään tilastot pisteistä
contacts_score_stats = contacts_df['Score'].describe()
companies_score_stats = companies_df['Score'].describe()

print("Kontaktien pisteiden tilastot:")
print(contacts_score_stats)
print("\nYritysten pisteiden tilastot:")
print(companies_score_stats)

# Yhdistetään pisteet ja tallennetaan tulokset
combined_scores_df = pd.concat([contacts_df[['Account_Id', 'Score']], companies_df[['Account_Id', 'Score', 'Industry']]], axis=0)
combined_scores_df.to_csv('combined_scores.csv', index=False)

# Muutetaan kategorinen 'industry' sarake numeeriseksi koodeiksi
combined_scores_df['Industry_Code'] = combined_scores_df['Industry'].astype('category').cat.codes

# Funktio korrelaatiomatriisin laskemiseen valituille sarakkeille
def calculate_correlation_matrix(df, columns):
    correlation_matrix = df[columns].corr()
    return correlation_matrix

# Määritä sarakkeet korrelaatiota varten 
columns_for_correlation = ['Score', 'Industry_Code']  # Lisää tai poista sarakkeita tarpeen mukaan

# Lasketaan korrelaatiomatriisi
correlation_matrix = calculate_correlation_matrix(combined_scores_df, columns_for_correlation)

# Muutetaan korrelaatiomatriisi pitkään muotoon power bi:tä varten
correlation_long_format = correlation_matrix.unstack().reset_index()
correlation_long_format.columns = ['Variable1', 'Variable2', 'Correlation']

# Tallennetaan korrelaatiomatriisi csv-tiedostoon
correlation_long_format.to_csv('correlation_matrix.csv', index=False)

# Tulostetaan korrelaatiomatriisi
print("Korrelaatiomatriisi (pitkä muoto):")
print(correlation_long_format)

# Piirretään korrelaatiomatriisi visualisointia varten
plt.figure(figsize=(8, 6))
plt.matshow(correlation_matrix, cmap='coolwarm', fignum=1)
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.colorbar()
plt.title('Korrelaatiomatriisi', pad=20)
plt.show()
```

</details>



#### Visuaalinen muokkaus ja filtteröinti Power BI:ssä

Tein vielä pari kaavioita datasta ja harjoittelin muokkaamista ja filtteröintiä ehdollisilla säännöillä. Ensimmäisessä kuvassa on filtteröity top 25 käyttäen top N filtteröintiä ja toisessa on kaikki toimialat pisteiden keskiarvoineen laitettu piirakkakaavioon.

![Top25](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-03%20175548.png?raw=true)
![Pie](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-03%20180958.png?raw=true)





### Monimutkainen data ja lopullinen työ

Päätin vielä loppuun laittaa laajempaa dataa ja soveltaa visualisointiin. Ensimmäinen skripti filtteröi dataa edustavammaksi tilastollisin menetelmin sekä rikastaa sitä laskelmilla. Alunperin meinasin tyytyä tuohon mutta päätin että haluan lisää laskelmia ja kunnollisia korrelaatioita joten tein vielä toisin skriptin joka loi kaksi jättiläismäistä korrelaatiomatriisia. Rikastin laskelmilla kuten Cohenin D, ja datalla voisikin nyt tehdä melkein mitä vain visualisointeja. 
<details>
  <summary>Ensimmäinen skripti</summary>

  ```python
import pandas as pd
import numpy as np
from scipy.stats import norm

# Lataa datasetti
companies_df = pd.read_csv("data.csv")

# Poista duplikaatit 'Technologies' -sarakkeen sisällä
def remove_duplicates(tech_list):
    if pd.isna(tech_list):
        return tech_list
    unique_techs = list(dict.fromkeys(tech_list.split(',')))
    return ','.join(unique_techs)

companies_df['Technologies'] = companies_df['Technologies'].apply(remove_duplicates)

# Suodata yritykset, joilla on vuotuinen liikevaihto
companies_with_revenue_df = companies_df[companies_df['Annual_Revenue'].notna()].copy()

# Jaa teknologiat yksittäisiksi merkinnöiksi
all_technologies = companies_with_revenue_df['Technologies'].str.split(',', expand=True).stack().reset_index(level=0, drop=False)
unique_technologies = all_technologies[0].unique()

# Luo DataFrame teknologioiden läsnäololle (1) tai poissaololle (0)
technology_presence_df = pd.get_dummies(all_technologies.set_index('level_0')[0]).groupby('level_0').max()

# Varmista, että kaikki yksilölliset teknologiat ovat sarakkeina
technology_presence_df = technology_presence_df.reindex(columns=unique_technologies, fill_value=0)

# Varmista, että technology_presence_df:llä on sama indeksi kuin companies_with_revenue_df:llä
technology_presence_df = technology_presence_df.reindex(companies_with_revenue_df.index)

# Laske teknologioiden määrä jokaiselle yritykselle
companies_with_revenue_df['Technology_Count'] = technology_presence_df.sum(axis=1)

# Valitse relevantit sarakkeet lopullista DataFramea varten
final_df = pd.concat([companies_with_revenue_df[['Account_Id', 'Annual_Revenue', 'Industry', 'Technology_Count', 'Lists']],
                      technology_presence_df], axis=1)

# Suodata rivit, joilla ei ole Account_Id:tä
final_df = final_df[final_df['Account_Id'].notna()]

# Varmista, että kaikki unique_technologies-elementit ovat final_df:ssä
final_tech_columns = set(final_df.columns)
unique_technologies_in_final_df = [tech for tech in unique_technologies if tech in final_tech_columns]

# Laske teknologioiden läsnäolon ja vuotuisen liikevaihdon välinen korrelaatio
correlation_with_revenue = final_df[unique_technologies_in_final_df + ['Annual_Revenue']].corr()['Annual_Revenue'].drop('Annual_Revenue')

# Tarkista null-arvot korrelaatioissa
if correlation_with_revenue.isnull().any():
    print("Varoitus: Korrelaatioissa on null-arvoja! Tarkista datasi ja laskelmasi.")

# Laske toimialojen korrelaatio vuotuiseen liikevaihtoon
industry_correlation = pd.get_dummies(final_df['Industry'])
industry_correlation['Annual_Revenue'] = final_df['Annual_Revenue']
industry_correlation_corr = industry_correlation.corr()['Annual_Revenue'].drop('Annual_Revenue')

# Järjestä toimialat niiden korrelaation mukaan liikevaihtoon
industry_ranking = industry_correlation_corr.rank(ascending=False).to_dict()

# Järjestä teknologiat niiden liikevaihtokorrelaation mukaan normaalijakaumaa käyttäen
technology_scores = norm.cdf(correlation_with_revenue)

# Laske Technology_General_Valence-pisteet
technology_median_score = np.median(technology_scores)
final_df['Technology_General_Valence'] = final_df['Lists'].apply(lambda x: len(str(x).split(','))) + technology_median_score

# Laske Tech_Correlation_with_revenue kunkin yrityksen teknologioiden keskimääräisen korrelaation perusteella
def calculate_tech_correlation(row):
    techs = row[unique_technologies_in_final_df]  # Yrityksen teknologiat
    present_techs = techs[techs > 0].index  # Vain käytössä olevat teknologiat
    correlations = correlation_with_revenue.loc[present_techs]  # Teknologioiden korrelaatiot
    if len(correlations) > 0:
        return correlations.mean()  # Korrelaatioiden keskiarvo
    else:
        return np.nan

final_df['Tech_Correlation_with_revenue'] = final_df.apply(calculate_tech_correlation, axis=1)

# Luo toimialakorrelaatiokolumnit vektorisoiduilla operaatioilla
final_df = final_df.join(final_df['Industry'].map(industry_correlation_corr.to_dict()).rename('Industry_Correlation_with_revenue'))
final_df = final_df.join(final_df['Industry'].map(industry_ranking).rename('Industry_Ranking'))

# Sovella teknologiapisteitä teknologiasarakkeisiin vektorisoiduilla operaatioilla
for tech in unique_technologies_in_final_df:
    final_df[tech] *= technology_scores[unique_technologies_in_final_df.index(tech)]

# Laske keskiarvo, maksimi, minimi, mediaani ja lukumäärä liikevaihdolle kullekin teknologialle
technology_stats = final_df.melt(id_vars=['Annual_Revenue'], value_vars=unique_technologies_in_final_df, var_name='Technology', value_name='Presence')
technology_stats = technology_stats[technology_stats['Presence'] > 0].groupby('Technology')['Annual_Revenue'].agg(['mean', 'max', 'min', 'median', 'count'])

# Laske keskiarvo, maksimi, minimi, mediaani ja lukumäärä liikevaihdolle kullekin toimialalle
industry_stats = final_df.groupby('Industry')['Annual_Revenue'].agg(['mean', 'max', 'min', 'median', 'count'])

# Täytä puuttuvat arvot sopivilla oletusarvoilla
final_df.fillna(0, inplace=True)
correlation_with_revenue_df = correlation_with_revenue.reset_index()
correlation_with_revenue_df.columns = ['Technology', 'Correlation_with_Revenue']
correlation_with_revenue_df = correlation_with_revenue_df.merge(technology_stats.reset_index(), on='Technology', how='left')
correlation_with_revenue_df.rename(columns={'mean': 'Keskiarvo_liikevaihto', 'max': 'LiikevaihtoMAX', 'min': 'LiikevaihtoMIN', 'median': 'LiikevaihtoMedian', 'count': 'N'}, inplace=True)
correlation_with_revenue_df.fillna(0, inplace=True)

industry_correlation_df = industry_correlation_corr.reset_index()
industry_correlation_df.columns = ['Industry', 'Correlation_with_Revenue']
industry_correlation_df = industry_correlation_df.merge(industry_stats.reset_index(), on='Industry', how='left')
industry_correlation_df.rename(columns={'mean': 'Keskiarvo_liikevaihto', 'max': 'LiikevaihtoMAX', 'min': 'LiikevaihtoMIN', 'median': 'LiikevaihtoMedian', 'count': 'N'}, inplace=True)
industry_correlation_df.fillna(0, inplace=True)

# Muotoile numerot helpommin luettaviksi
correlation_with_revenue_df['Keskiarvo_liikevaihto'] = correlation_with_revenue_df['Keskiarvo_liikevaihto'].apply(lambda x: f"{x:,.0f}")
correlation_with_revenue_df['LiikevaihtoMAX'] = correlation_with_revenue_df['LiikevaihtoMAX'].apply(lambda x: f"{x:,.0f}")
correlation_with_revenue_df['LiikevaihtoMIN'] = correlation_with_revenue_df['LiikevaihtoMIN'].apply(lambda x: f"{x:,.0f}")
correlation_with_revenue_df['LiikevaihtoMedian'] = correlation_with_revenue_df['LiikevaihtoMedian'].apply(lambda x: f"{x:,.0f}")

industry_correlation_df['Keskiarvo_liikevaihto'] = industry_correlation_df['Keskiarvo_liikevaihto'].apply(lambda x: f"{x:,.0f}")
industry_correlation_df['LiikevaihtoMAX'] = industry_correlation_df['LiikevaihtoMAX'].apply(lambda x: f"{x:,.0f}")
industry_correlation_df['LiikevaihtoMIN'] = industry_correlation_df['LiikevaihtoMIN'].apply(lambda x: f"{x:,.0f}")
industry_correlation_df['LiikevaihtoMedian'] = industry_correlation_df['LiikevaihtoMedian'].apply(lambda x: f"{x:,.0f}")

# Sovella logaritmimuunnos ja suodata
final_df['Log_Annual_Revenue'] = np.log(final_df['Annual_Revenue'])
revenue_95_percentile = final_df['Log_Annual_Revenue'].quantile(0.95)
filtered_final_df = final_df[final_df['Log_Annual_Revenue'] <= revenue_95_percentile]

# Poista teknologiasarakkeet, joilla on pelkkiä nollia suodatuksen jälkeen
filtered_final_df = filtered_final_df.loc[:, (filtered_final_df != 0).any(axis=0)]

# Laske suodatetut tilastot
filtered_weighted_mean_log_revenue = np.exp(np.average(filtered_final_df['Log_Annual_Revenue'], weights=filtered_final_df['Technology_Count']))
filtered_median_log_revenue = np.exp(filtered_final_df['Log_Annual_Revenue'].median())
filtered_mean_tech_count = filtered_final_df['Technology_Count'].mean()
filtered_median_tech_count = filtered_final_df['Technology_Count'].median()

# Tulosta tulokset
print(f"Suodatettu painotettu logaritmisen vuotuisen liikevaihdon keskiarvo (95. prosenttipiste): {filtered_weighted_mean_log_revenue}")
print(f"Suodatettu logaritmisen vuotuisen liikevaihdon mediaani (95. prosenttipiste): {filtered_median_log_revenue}")
print(f"Suodatettu teknologioiden määrän keskiarvo (95. prosenttipiste): {filtered_mean_tech_count}")
print(f"Suodatettu teknologioiden määrän mediaani (95. prosenttipiste): {filtered_median_tech_count}")

# Tallenna lopullinen DataFrame CSV-tiedostoon Power BI -analyysia varten
filtered_final_df.to_csv('filtered_companies_technology_industry_scoring.csv', index=False)
correlation_with_revenue_df.to_csv('filtered_technology_revenue_correlation_all.csv', index=False)
industry_correlation_df.to_csv('filtered_industry_revenue_correlation.csv', index=False)

# Tulosta ensimmäiset rivit lopullisesta DataFramesta
print("Lopullinen DataFrame Power BI -analyysiä varten:")
print(filtered_final_df.head())

# Tulosta korrelaatiotulokset
print("Teknologiat ja niiden korrelaatiot liikevaihtoon sekä keskiarvoinen liikevaihto:")
print(correlation_with_revenue_df)
print("Toimialat ja niiden korrelaatiot liikevaihtoon sekä keskiarvoinen liikevaihto:")
print(industry_correlation_df)


```
</details>
<details>
  <summary>Toinen skripti</summary>
  
  ```python
import pandas as pd
import numpy as np
from scipy.stats import norm, skew, kurtosis

# Lataa datasetti
companies_df = pd.read_csv('filtered_companies_technology_industry_scoring.csv')

# Tunnista teknologiakolumnit
start_col = companies_df.columns.get_loc('Lists') + 1
end_col = companies_df.columns.get_loc('Technology_General_Valence') - 1
technology_columns = companies_df.columns[start_col:end_col + 1]

# Luo binäärinen läsnäolo/poissaolo DataFrame teknologioille
technology_presence_df = (companies_df[technology_columns] > 0).astype(int)

# Suodata teknologiat, joilla on riittävästi dataa
technology_presence_counts = technology_presence_df.sum()
sufficient_data_technologies = technology_presence_counts[technology_presence_counts > 1].index
technology_presence_df = technology_presence_df[sufficient_data_technologies]

# Poista teknologiat, joilla on NaN-korrelaatioarvoja
technology_corr = technology_presence_df.corr()
technology_corr = technology_corr.dropna(axis=0, how='any').dropna(axis=1, how='any')

# Tallenna teknologiakorrelaatiomatriisi CSV-tiedostoon
technology_corr.to_csv('technology_correlation_matrix.csv')

# Tulosta korrelaatiomatriisi varmistukseksi
print("Technology Correlation Matrix:")
print(technology_corr.head())

# Lataa suodatetut datasetit
correlation_with_revenue_df = pd.read_csv('filtered_technology_revenue_correlation_all.csv')
industry_correlation_df = pd.read_csv('filtered_industry_revenue_correlation.csv')

# Luo ID:t jokaiselle riville
companies_df['ID'] = range(1, len(companies_df) + 1)

# Laske tilastot
stats = {
    'mean': companies_df['Annual_Revenue'].mean(),
    'median': companies_df['Annual_Revenue'].median(),
    'mode': companies_df['Annual_Revenue'].mode()[0] if not companies_df['Annual_Revenue'].mode().empty else np.nan,
    'std_dev': companies_df['Annual_Revenue'].std(),
    'variance': companies_df['Annual_Revenue'].var(),
    'skewness': skew(companies_df['Annual_Revenue']),
    'kurtosis': kurtosis(companies_df['Annual_Revenue']),
    'min': companies_df['Annual_Revenue'].min(),
    'max': companies_df['Annual_Revenue'].max(),
    '25th_percentile': np.percentile(companies_df['Annual_Revenue'], 25),
    '50th_percentile': np.percentile(companies_df['Annual_Revenue'], 50),
    '75th_percentile': np.percentile(companies_df['Annual_Revenue'], 75),
    '90th_percentile': np.percentile(companies_df['Annual_Revenue'], 90),
    '95th_percentile': np.percentile(companies_df['Annual_Revenue'], 95),
    '99th_percentile': np.percentile(companies_df['Annual_Revenue'], 99)
}

# Lisää normaalijakauman arvot
companies_df['Normal_Distribution'] = norm.pdf(companies_df['Annual_Revenue'], stats['mean'], stats['std_dev'])

# Funktio Cohenin d:n laskemiseen lisätarkistuksin
def cohens_d(x, y):
    nx = len(x)
    ny = len(y)
    if nx < 2 or ny < 2:
        return np.nan  # Ei tarpeeksi näytteitä Cohenin d:n laskemiseen
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / dof)
    if pooled_std == 0:
        return np.nan  # Keskihajonta 0, Cohen's d ei voida laskea
    return (np.mean(x) - np.mean(y)) / pooled_std

# Suodata pois rivit, joissa toimiala on merkitty "0":ksi toimialaan liittyvää analyysiä varten
industry_related_df = companies_df[companies_df['Industry'] != '0']

# Laske Cohenin d kullekin teknologiakäytön määrälle ja toimialalle verrattuna koko populaatioon
tech_groups = companies_df.groupby('Technology_Count')
industry_groups = industry_related_df.groupby('Industry')  # Käytä suodatettua datasettiä

cohens_d_tech_overall = []
cohens_d_industry_overall = []

for name, group in tech_groups:
    d = cohens_d(group['Annual_Revenue'], companies_df['Annual_Revenue'])
    cohens_d_tech_overall.append({'Technology_Count': name, 'Cohens_d': d})

for name, group in industry_groups:
    d = cohens_d(group['Annual_Revenue'], industry_related_df['Annual_Revenue'])  # Käytä suodatettua datasettiä
    cohens_d_industry_overall.append({'Industry': name, 'Cohens_d': d})

cohens_d_tech_overall_df = pd.DataFrame(cohens_d_tech_overall)
cohens_d_industry_overall_df = pd.DataFrame(cohens_d_industry_overall)

# Laske Cohenin d kullekin teknologiakäytön määrälle ja toimialalle verrattuna toisiinsa
tech_counts = sorted(companies_df['Technology_Count'].unique())
industries = industry_related_df['Industry'].unique()  # Käytä suodatettua datasettiä

cohens_d_tech_groups = []
cohens_d_industry_groups = []

# Pareittainen vertailu Technology Countien osalta
for i in range(len(tech_counts)):
    for j in range(i + 1, len(tech_counts)):
        group1 = companies_df[companies_df['Technology_Count'] == tech_counts[i]]
        group2 = companies_df[companies_df['Technology_Count'] == tech_counts[j]]
        d = cohens_d(group1['Annual_Revenue'], group2['Annual_Revenue'])
        cohens_d_tech_groups.append({'Technology_Count_1': tech_counts[i], 'Technology_Count_2': tech_counts[j], 'Cohens_d': d})

# Pareittainen vertailu Toimialojen osalta
for i in range(len(industries)):
    for j in range(i + 1, len(industries)):
        group1 = industry_related_df[industry_related_df['Industry'] == industries[i]]  # Käytä suodatettua datasettiä
        group2 = industry_related_df[industry_related_df['Industry'] == industries[j]]  # Käytä suodatettua datasettiä
        d = cohens_d(group1['Annual_Revenue'], group2['Annual_Revenue'])
        cohens_d_industry_groups.append({'Industry_1': industries[i], 'Industry_2': industries[j], 'Cohens_d': d})

cohens_d_tech_groups_df = pd.DataFrame(cohens_d_tech_groups)
cohens_d_industry_groups_df = pd.DataFrame(cohens_d_industry_groups)

# Lisää Cohenin d -arvot companies_df DataFrameen
companies_df = companies_df.merge(cohens_d_tech_overall_df, left_on='Technology_Count', right_on='Technology_Count', how='left', suffixes=('', '_Tech'))
companies_df = companies_df.merge(cohens_d_industry_overall_df, left_on='Industry', right_on='Industry', how='left', suffixes=('', '_Industry'))

filtered_companies = companies_df.drop(columns=technology_columns)

# Luo taulukko, joka listaa teknologiakorrelaatiot Account_Id:n kanssa
technology_correlations = companies_df[['Account_Id'] + list(sufficient_data_technologies)]

# Laske pareittaiset korrelaatiot toimialoille
industry_columns = pd.get_dummies(industry_related_df['Industry'])  # Käytä suodatettua datasettiä
industry_corr_matrix = industry_columns.corr().dropna(axis=0, how='any').dropna(axis=1, how='any')

# Tallenna tulokset uusiin CSV-tiedostoihin Power BI -visualisointia varten
filtered_companies.to_csv('filtered_companies_with_normal_distribution.csv', index=False)
technology_correlations.to_csv('technology_correlations_with_Account_Id.csv', index=False)
cohens_d_tech_overall_df.to_csv('cohens_d_technology_overall.csv', index=False)
cohens_d_industry_overall_df.to_csv('cohens_d_industry_overall.csv', index=False)
cohens_d_tech_groups_df.to_csv('cohens_d_technology_groups.csv', index=False)
cohens_d_industry_groups_df.to_csv('cohens_d_industry_groups.csv', index=False)
technology_corr.to_csv('technology_correlation_matrix.csv')
industry_corr_matrix.to_csv('industry_correlation_matrix.csv')

# Tallenna tilastot CSV-tiedostoon
stats_df = pd.DataFrame([stats])
stats_df.to_csv('annual_revenue_statistics.csv', index=False)

# Tulosta ensimmäiset rivit lopullisista DataFrameista
print("Filtered Companies DataFrame with Normal Distribution:")
print(companies_df.head())

print("Cohen's d for Technologies (Overall):")
print(cohens_d_tech_overall_df.head())

print("Cohen's d for Industries (Overall):")
print(cohens_d_industry_overall_df.head())

print("Cohen's d for Technology Groups:")
print(cohens_d_tech_groups_df.head())

print("Cohen's d for Industry Groups:")
print(cohens_d_industry_groups_df.head())

print("Annual Revenue Statistics:")
print(stats_df)

print("Technology Correlation Matrix:")
print(technology_corr.head())

print("Industry Correlation Matrix:")
print(industry_corr_matrix.head())

# Tallenna tulokset Excel-työkirjaan
with pd.ExcelWriter('analysis_results.xlsx') as writer:
    filtered_companies.to_excel(writer, sheet_name='Filtered_Companies', index=False)
    cohens_d_tech_overall_df.to_excel(writer, sheet_name='Cohen_d_Tech_Overall', index=False)
    cohens_d_industry_overall_df.to_excel(writer, sheet_name='Cohen_d_Ind_Overall', index=False)
    cohens_d_tech_groups_df.to_excel(writer, sheet_name='Cohen_d_Tech_Groups', index=False)
    cohens_d_industry_groups_df.to_excel(writer, sheet_name='Cohen_d_Ind_Groups', index=False)
    technology_corr.to_excel(writer, sheet_name='Tech_Corr_Matrix')
    industry_corr_matrix.to_excel(writer, sheet_name='Ind_Corr_Matrix')
    stats_df.to_excel(writer, sheet_name='Annual_Rev_Stats', index=False)
    technology_correlations.to_excel(writer, sheet_name='Tech_Corr_Apollo_ID', index=False)

print("Excel-työkirja 'analysis_results.xlsx' luotiin onnistuneesti.")
```
</details>

Datan käsittely mahdollisti monia asioita kuten vaikutuskokojen täsmällisempää ymmärtämistä, tässä kuvassa toimiala verrataan jokaista toista toimialaa vasten vertailukohteena liikevaihto. Cohen's d ilmaisee efektikokoa. Se on hyvä mittaustapa määrittelemään todellisia vaikutuksia eri asioiden välillä ja tunnistamaan ilmiöitä joilla on nuanssia. 
Jokainen pylväs on siis yhden toimialan kokonaiskuva, jossa on siis pareittain verrattu loput toimialoista ja otettu niiden suhteesta liikevaihtoon Cohen's d.
Jos pylväs on korkea, mutta se menee samanaikaisesti negatiiviselle puolelle, se tarkoittaa, että kyseisellä toimialalla on negatiivisia Cohen's d -arvoja verrattuna muihin toimialoihin positiivisien lisäksi.
Kuvissa voisi olla esim. interaktiinen valitsin joka filtteröi merkittävät vaikutuskoot.


![Cohens1](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-05%20050536.png?raw=true)




Toisessa esimerkissä teknologioiden määrien vaikutuskoot liikevaihtoon

![Cohens2](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-05%20050548.png?raw=true)



Jos katsotaan koko populaatioon vertausta linjana, Cohen's d arvon antamaa efekti kokoa ei näy oikein ollenkaan

![Cohens3](https://github.com/Mauno934/Tyonayte/blob/main/Screenshot%202024-08-05%20050519.png?raw=true)






Ja tässäpä on oikeastaan kaikki!




## Edistynyt data-analyysi PySparkilla ja Azurella
Tässä osiossa tutustun Apache Sparkin sekä Databricksin käyttöön. Kaikki skriptit todellisuudessa vaatisivat enemmän kehitystä.

### Tiedostojen kopiointi DBFS:tä paikalliselle ajurille
Aloitin kopioimalla SQLite-tietokantatiedoston Databricks File Systemistä (DBFS) paikalliselle ajurille, jotta Spark voi käyttää sitä:

```python
# Kopioidaan tiedosto DBFS:stä paikalliselle ajurille
dbutils.fs.cp("dbfs:/dbfs/tmp/Tietokanta.db", "file:/tmp/Tietokanta.db")

# Paikallisen tiedoston polku Sparkille
local_file_path_for_spark = "file:/tmp/Tietokanta.db"
SQLite-datan lataaminen Spark DataFrameen
Käyttämällä JDBC
ä latasimme tiedot SQLite-tietokannasta Spark DataFrameen käsittelyä varten:

# Ladataan SQLite-tiedosto Spark DataFrameen JDBC:n kautta
df = spark.read.format("jdbc").options(
    url=f"jdbc:sqlite:{local_file_path_for_spark}",
    dbtable="Companies",
    driver="org.sqlite.JDBC"
).load()

# Näytetään muutama rivi varmistaaksemme, että data on ladattu oikein
df.show(5)
```

### Lineaarinen regressioanalyysi
Suoritin lineaarisen regressioanalyysin ennustamaan vuosiliikevaihtoa perustuen työntekijöiden määrään ja kunkin yrityksen käyttämien teknologioiden lukumäärään:
```python
from pyspark.sql.functions import size, split, col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

# Oletetaan, että 'Technologies' on sarake, joka sisältää teknologioiden luettelon
# Lisätään uusi sarake "Technology_Count", joka laskee teknologioiden määrän per yritys
df = df.withColumn("Technology_Count", size(split(col("Technologies"), ",")))

# Suodatetaan pois rivit, joissa on NULL-arvoja tarvittavissa sarakkeissa
df_cleaned = df.filter(
    df["Number_of_Employees"].isNotNull() &
    df["Technology_Count"].isNotNull() &
    df["Annual_Revenue"].isNotNull()
)

# Valitaan sarakkeet, joita käytetään ennustamiseen, mukaan lukien "Company"-sarake
df_features = df_cleaned.select("Company", "Number_of_Employees", "Technology_Count", "Annual_Revenue")

# Muodostetaan ominaisuudet ja targetti
assembler = VectorAssembler(inputCols=["Number_of_Employees", "Technology_Count"], outputCol="features")
transformed_data = assembler.transform(df_features)

# Määritetään lineaarinen regressiomalli
lr = LinearRegression(featuresCol="features", labelCol="Annual_Revenue")

# Sovitetaan malli
lr_model = lr.fit(transformed_data)

# Ennustetaan liikevaihto
predictions = lr_model.transform(transformed_data)

# Näytetään yritys, todellinen liikevaihto ja ennustettu liikevaihto
predictions.select("Company", "Annual_Revenue", "prediction").show(10)


# Aseta yhteys Blob Storageen
spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_access_key)
```

### K-Means-klusterointi
Sovelsin K-Means-klusterointia segmentoimaan yritykset työntekijöiden määrän ja vuosiliikevaihdon perusteella:
```python
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

# Valmistellaan data klusterointia varten
assembler = VectorAssembler(inputCols=["Number_of_Employees", "Annual_Revenue"], outputCol="features")
df_kmeans = assembler.transform(df_cleaned)

# Määritetään K-Means-klusterointi, k = 4
kmeans = KMeans(k=4, seed=1)
model = kmeans.fit(df_kmeans)

# Ennustetaan klusterit
clusters = model.transform(df_kmeans)

# Näytetään klusterien ennusteet yrityksittäin
clusters.select("Company", "Number_of_Employees", "Annual_Revenue", "prediction").show(10)
```


### Tallenna klusteroinnin tulokset CSV-muodossa Blob Storageen
clusters.select("Company", "Number_of_Employees", "Annual_Revenue", "prediction").write.mode("overwrite").csv(output_path)

print(f"Klusteroinnin tulokset tallennettu polkuun {output_path}")
###Sentimenttianalyysi SEO-kuvauksille
Käyttäen TextBlob-kirjastoa, tein sentimenttianalyysin SEO-kuvauksille testaamaan yrityksen kuvauksen välittämän tunteen analysointia:
```python
%pip install textblob

from textblob import TextBlob
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType

# Luodaan UDF-funktio sentimenttianalyysille
def analyze_sentiment(text):
    if text:
        blob = TextBlob(text)
        return blob.sentiment.polarity  # Palautetaan sentimentin polariteetti (-1...1)
    return None

# Rekisteröidään UDF (User Defined Function) PySparkille
sentiment_udf = udf(analyze_sentiment, DoubleType())

# Lisätään uusi sentimentti-sarake, joka analysoi SEO-kuvaukset
df_with_sentiment = df.withColumn("Sentiment_Polarity", sentiment_udf(df["SEO_Description"]))

# Näytetään tulokset
df_with_sentiment.select("Company", "SEO_Description", "Sentiment_Polarity").show(10, truncate=False)
Sentimenttianalyysin tulosten tallentaminen
Tallensimme sentimenttianalyysin tulokset Azure Blob Storageen:


output_blob_name = "seo_sentiment_analysis.csv"
output_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/{output_blob_name}"

# Tallenna sentimenttianalyysin tulokset Blob Storageen
df_with_sentiment.select("Company", "SEO_Description", "Sentiment_Polarity").write.mode("overwrite").csv(output_path)

print(f"Sentimenttianalyysin tulokset tallennettu polkuun {output_path}")
```
### Tilastollinen analyysi ja mediaanien laskeminen
Ajattelin tietokantaa perusjoukkoja, ja vertasin yrityksiä joilla on monta rikasta datapistettä perusjoukkoon että tiedän mitä näyte edustavaa, yleisesti näyttää että paremmin dokumentoidut isommat yritykset ovat useammin edustettuja

```python
from pyspark.sql.functions import expr, avg, min, max

# Lasketaan mediaanit käyttäen approx_percentile
mediaanit = df_cleaned.select(
    expr("percentile_approx(Annual_Revenue, 0.5)").alias("Median_Annual_Revenue"),
    expr("percentile_approx(Number_of_Employees, 0.5)").alias("Median_Number_of_Employees"),
    expr("percentile_approx(Total_Funding, 0.5)").alias("Median_Total_Funding")
)

# Lasketaan keskiarvot, minimi- ja maksimiarvot
tilastot = df_cleaned.select(
    avg("Annual_Revenue").alias("Avg_Annual_Revenue"),
    min("Annual_Revenue").alias("Min_Annual_Revenue"),
    max("Annual_Revenue").alias("Max_Annual_Revenue"),
    avg("Number_of_Employees").alias("Avg_Number_of_Employees"),
    min("Number_of_Employees").alias("Min_Number_of_Employees"),
    max("Number_of_Employees").alias("Max_Number_of_Employees"),
    avg("Total_Funding").alias("Avg_Total_Funding"),
    min("Total_Funding").alias("Min_Total_Funding"),
    max("Total_Funding").alias("Max_Total_Funding")
)

# Näytetään mediaanit ja tilastot
mediaanit.show()
tilastot.show()
```
Vertailin myös yrityksiä, joilla on täydet tiedot (tiedot vuosiliikevaihdosta, työntekijöiden määrästä ja kokonaisrahoituksesta) niihin, joilta puuttuu osa tiedoista:

```python

# Yritykset, joilla on tiedot kaikista kolmesta muuttujasta
df_full_info = df_cleaned.filter(
    df_cleaned["Annual_Revenue"].isNotNull() &
    df_cleaned["Number_of_Employees"].isNotNull() &
    df_cleaned["Total_Funding"].isNotNull()
)

# Yritykset, joilta puuttuu rahoitustiedot
df_partial_info = df_cleaned.filter(
    df_cleaned["Annual_Revenue"].isNotNull() &
    df_cleaned["Number_of_Employees"].isNotNull() &
    df_cleaned["Total_Funding"].isNull()
)

# Lasketaan mediaanit molemmille ryhmille
mediaanit_full_info = df_full_info.select(
    expr("percentile_approx(Annual_Revenue, 0.5)").alias("Median_Annual_Revenue"),
    expr("percentile_approx(Number_of_Employees, 0.5)").alias("Median_Number_of_Employees")
)

mediaanit_partial_info = df_partial_info.select(
    expr("percentile_approx(Annual_Revenue, 0.5)").alias("Median_Annual_Revenue"),
    expr("percentile_approx(Number_of_Employees, 0.5)").alias("Median_Number_of_Employees")
)

# Näytetään tilastot molemmille ryhmille
mediaanit_full_info.show()
mediaanit_partial_info.show()
```


### Yritysten teknologiafokuksen analyysi
Tavoite: Analysoida yritysten käyttämien teknologioiden vaikutusta niiden toimintaan.


Aloitin lataamalla yritysdatan relevantit sarakkeet, kuten SEO-kuvauksen, teknologiat ja avainsanat:

```python

df = spark.read.format("jdbc").options(
    url="jdbc:sqlite:/tmp/Tietokanta.db",
    dbtable="Companies",
    driver="org.sqlite.JDBC"
).load()
```
Suodatin pois yritykset, joilla ei ole teknologiatietoja:

```python

df_filtered = df.select("Company", "Technologies").filter(df["Technologies"].isNotNull())
```
Tokenisoin teknologiakentän:

```python

from pyspark.ml.feature import Tokenizer

tokenizer = Tokenizer(inputCol="Technologies", outputCol="Tech_Words")
df_tokenized = tokenizer.transform(df_filtered)
```
Poistin stop-sanat teknologiadataa siivotakseni:

```python

from pyspark.ml.feature import StopWordsRemover

remover = StopWordsRemover(inputCol="Tech_Words", outputCol="Filtered_Tech_Words")
df_cleaned = remover.transform(df_tokenized)
```
Sovelsin TF-IDF-analyysiä teknologioihin selvittääkseni yleisimmät ja vaikuttavimmat teknologiat:

```python

from pyspark.ml.feature import HashingTF, IDF

hashingTF = HashingTF(inputCol="Filtered_Tech_Words", outputCol="RawFeatures", numFeatures=20)
featurizedData = hashingTF.transform(df_cleaned)

idf = IDF(inputCol="RawFeatures", outputCol="Features_TF_IDF")
idfModel = idf.fit(featurizedData)
df_tf_idf = idfModel.transform(featurizedData)
```

Lopuksi klusteroin yritykset K-means-algoritmilla teknologiafokuksen perusteella:

```python

from pyspark.ml.clustering import KMeans

kmeans = KMeans(k=5, seed=1, featuresCol="Features_TF_IDF", predictionCol="Cluster")
model = kmeans.fit(df_tf_idf)
df_clusters = model.transform(df_tf_idf)
```
Yhdistin teknologiasanat yhdeksi tekstikentäksi tulosten tulkintaa helpottaakseni:

```python

from pyspark.sql.functions import concat_ws

df_clusters = df_clusters.withColumn("Tech_Words_Text", concat_ws(",", "Filtered_Tech_Words"))
```

Näin sain ryhmiteltyä yritykset tarkemmin kuin aiemmilla luokilla. 

### SEO-optimointi ja avainsanakeskeinen analyysi
Tavoite: Tutkia SEO-kuvausten ja avainsanojen yhteyttä yritysten menestykseen.



```python

df = spark.read.format("jdbc").options(
    url="jdbc:sqlite:/tmp/Tietokanta.db",
    dbtable="Companies",
    driver="org.sqlite.JDBC"
).load()

from pyspark.sql.functions import regexp_replace

df_cleaned = df.withColumn("SEO_Description_Cleaned", regexp_replace("SEO_Description", "[^a-zA-Z0-9 ]", ""))`
```

Suoritin sentimenttianalyysin TextBlob-kirjaston avulla selvittääkseni SEO-kuvausten sävyn:

```python

from textblob import TextBlob
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def get_sentiment(text):
    if text is None or text == "":
        return "neutral"
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

sentiment_udf = udf(get_sentiment, StringType())
df_sentiment = df_cleaned.withColumn("SEO_Sentiment", sentiment_udf("SEO_Description_Cleaned"))
```

Analysoin avainsanat löytääkseni yleisimmät termit:

```python

from pyspark.sql.functions import split, explode, col

df_keywords = df_sentiment.withColumn("Keywords_Split", split(col("Keywords"), ","))
df_exploded_keywords = df_keywords.withColumn("Keyword", explode("Keywords_Split"))
df_keyword_counts = df_exploded_keywords.groupBy("Keyword").count().orderBy(col("count").desc())
```
Tämän tapainen skripti on hyvä selvittämään parhaita SEO-käytäntöjä mutta huomioitavaa on että versioni on varsin alkeellinen. 

### Tittelien ja organisaatiorakenteen perusteella yritysten mallintaminen
Tavoite: Analysoida yritysten organisaatiorakennetta kontaktien tittelien perusteella.


Latasin kontaktitiedot ja puhdistin tittelit poistamalla erikoismerkit ja muuttamalla tekstin pieniksi kirjaimiksi:

```python

df_contacts = spark.read.format("jdbc").options(
    url="jdbc:sqlite:/tmp/Tietokanta.db",
    dbtable="Contacts",
    driver="org.sqlite.JDBC"
).load()

from pyspark.sql.functions import lower, regexp_replace

df_contacts_cleaned = df_contacts.filter(df_contacts["Title"].isNotNull())
df_contacts_cleaned = df_contacts_cleaned.withColumn("Cleaned_Title", lower(regexp_replace("Title", "[^a-zA-Z0-9]", " ")))
```
Tokenisoin tittelit ja ryhmittelin ne yleisyyden mukaan:

```python

from pyspark.ml.feature import Tokenizer

tokenizer = Tokenizer(inputCol="Cleaned_Title", outputCol="Tokenized_Title")
df_tokenized = tokenizer.transform(df_contacts_cleaned)

df_title_counts = df_tokenized.groupBy("Tokenized_Title").count().orderBy(col("count").desc())
```
Muunsin tittelit numeeriseen muotoon CountVectorizerin avulla ja klusteroin ne K-means-algoritmilla:

```python

from pyspark.ml.feature import CountVectorizer
from pyspark.ml.clustering import KMeans

cv = CountVectorizer(inputCol="Tokenized_Title", outputCol="Title_Features")
cv_model = cv.fit(df_tokenized)
df_title_features = cv_model.transform(df_tokenized)

kmeans = KMeans(k=3, seed=1)
kmeans_model = kmeans.fit(df_title_features)
df_clustered_contacts = kmeans_model.transform(df_title_features)
```

Yhdistin tulokset yritystauluun ja analysoin organisaatiorakenteen eri klustereissa:

```python

df_companies = spark.read.format("jdbc").options(
    url="jdbc:sqlite:/tmp/Tietokanta.db",
    dbtable="Companies",
    driver="org.sqlite.JDBC"
).load()

df_merged = df_companies.join(df_clustered_contacts, "Company", "left")
```
Näin pystyin mallintamaan yritysten organisaatiorakenteen kontaktien tittelien perusteella. Jos skriptiä muokkaisi hieman ja jatkokehittäisi tuloksien perusteella asioita, tämän tapaisella teknologialla voisi ennustaa esim. onko projekti / matriisiyritys.





### Yrityssegmenttien ennustaminen kokonaisvaltaisella lähestymistavalla
Tavoite: Ennustaa yrityssegmenttejä yhdistämällä yritysdatan eri osat.

Tekniikka:

Yhdistin yritysten SEO-kuvaukset, toimialat, teknologiat ja kontaktien tiedot analyysiä varten:

```python

df_companies = spark.read.format("jdbc").options(
    url="jdbc:sqlite:/tmp/Tietokanta.db",
    dbtable="Companies",
    driver="org.sqlite.JDBC"
).load()

df_contacts = spark.read.format("jdbc").options(
    url="jdbc:sqlite:/tmp/Tietokanta.db",
    dbtable="Contacts",
    driver="org.sqlite.JDBC"
).load()
```
Suoritin tekstin tokenisoinnin ja TF-IDF-muunnoksen saadakseni numeerisia ominaisuuksia tekstidatasta:

```python

from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF

df_filtered = df_companies.select("Company", "Short_Description", "Industry", "Number_of_Employees") \
    .filter(df_companies["Short_Description"].isNotNull())

tokenizer = Tokenizer(inputCol="Short_Description", outputCol="tokens")
df_tokenized = tokenizer.transform(df_filtered)

remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tokens")
df_filtered_tokens = remover.transform(df_tokenized)

hashingTF = HashingTF(inputCol="filtered_tokens", outputCol="raw_features", numFeatures=10000)
featurized_data = hashingTF.transform(df_filtered_tokens)

idf = IDF(inputCol="raw_features", outputCol="tfidf_features")
idf_model = idf.fit(featurized_data)
df_tfidf = idf_model.transform(featurized_data)
```
Yhdistin ominaisuudet ja klusteroin yritykset K-means-algoritmilla:

```python

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

assembler = VectorAssembler(inputCols=["tfidf_features", "Number_of_Employees"], outputCol="features")
df_features = assembler.transform(df_tfidf)

kmeans = KMeans(k=5, seed=1)
kmeans_model = kmeans.fit(df_features)
df_clusters = kmeans_model.transform(df_features)
```
Analysoin ja visualisoin tulokset eri segmenttien ja klustereiden mukaan, mikä auttoi ymmärtämään yritysten jakautumista eri markkinasegmentteihin:

```python

df_clusters.select("Company", "Industry", "Number_of_Employees", "prediction").show(20)
```
Näin sain kokonaisvaltaisen kuvan yritysten segmentoinnista yhdistämällä eri datalähteet ja analyysimenetelmät.








