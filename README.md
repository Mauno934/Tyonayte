# Työnäyte, Python / SQL / Power BI / AI / Suorituskyky

Ajattelin tutustua yhteen työpaikkakuvauksessa mainittuun teknologiaan ja tehdä sen ympärille työnäytteen jossa näkyy jo olemassa olevia taitoja sekä tehtyä työtä. En halunnut jakaa dataa sellaisena että
siinä olisi mitään kyseenalaista tietoturvan tai muun kannalta, joka koski myös erilaisia sarakkeita sekä lähteitä. Nykyisessä työpaikassa visualisointi ei ole ollut prioriteetti joten tästä tuli mielenkiintoinen kokeilu. 
Sisällytin kuitenkin myös paljon omaa koodia tähän jotka loin aikapitkälti lennosta, tai yhdistämällä joitain aiemmin luotuja komponentteja. 
Koko homma on tehty melko dynaamiseksi ja kehittyväksi mutta johtuen siitä että on ollut vain muutama päivä aikaa, koodini ei vastaa asynkronoitua ja monesti refakturoitua koodia. 
# Python ja Power BI -työnäyte: Osastojen Analyysi, Pisteytysjärjestelmä ja IndustryMapping

Tässä työnäytteessä esittelen Pythonilla ja Power BI:llä tekemiäni datan käsittely- ja visualisointitehtäviä. Työssä käytin olemassa olevia taitojani ja kehitin uusia, erityisesti datan analysoinnissa ja visualisoinnissa. Tämä dokumentti sisältää esimerkkejä Python-koodista ja Power BI -visualisoinneista, jotka on luotu tukemaan päätöksentekoa.

## Osastojen Analyysi Pythonilla

### Datan Esikäsittely

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

department_summary.to_csv('department_summary.csv', index=False)
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

# Pisteytysjärjestelmän Kehitys

## Datan Pisteytys
Kehitin pisteytysjärjestelmän, joka ottaa huomioon eri tekijöitä kontaktien ja yritysten laadun arvioimiseksi. Käytin vektorisoituja operaatioita tehokkuuden parantamiseksi.

### Kontaktien Pisteytys
```python
contacts_df['Has_Proper_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & (~contacts_df['Last_Name'].str.contains(r'^\w\.$'))
contacts_df['Has_Abbreviated_Name'] = contacts_df['First_Name'].notna() & contacts_df['Last_Name'].notna() & contacts_df['Last_Name'].str.contains(r'^\w\.$')
contacts_df['Has_Proper_Title'] = contacts_df['Title'].notna() & (~contacts_df['Title'].str.contains(r'\bat\b|\b/\b'))
contacts_df['Company_Match'] = contacts_df['Apollo_Account_Id'].map(company_name_mapping) == contacts_df['Company']
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
### Yritysten Pisteytys
```python
companies_df['Contact_Company_Match'] = companies_df.apply(
    lambda row: row['Company'] in contact_company_names.get(row['Apollo_Account_Id'], set()), axis=1
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
