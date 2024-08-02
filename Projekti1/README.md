# Power BI -testaus ja datan käsittely

Testasin Power BI:tä tuomalla SQL-tietokannasta dataa CSV-muodossa. Kokeilin Power BI:n erilaisia ominaisuuksia datan käsittelyyn ja opin paljon ohjelmasta sekä sen rajoituksista:

- **Datan tuominen**: Loin yhteyden SQL-tietokantaan ja tallensin datan CSV-tiedostoksi. Tämä mahdollisti datan jatkokäsittelyn Power BI:ssä.
- **Datan yhdistäminen**: Yhdistin `contacts` ja `companies` -taulut `Apollo_Account_Id`-sarakkeen perusteella.
- **Datan suodatus ja muokkaus**: Suodatin pois virheelliset arvot ja muunsin sarakkeiden tietotyyppejä. Huomasin, että Power BI:ssä ei ole suoraa "for each" -lausetta, mikä rajoittaa joitakin monimutkaisia käsittelyjä.
- **Visualisoinnit**: Loin erilaisia visualisointeja, kuten pylväsdiagrammeja ja piirakkakaavioita, jotka auttoivat ymmärtämään datan jakaumia ja yhteyksiä. Törmäsin myös joihinkin rajoituksiin, kuten vaikeuksiin käsitellä osastoarvoja, jotka olivat virheellisiä (esim. puhelinnumeroita).

## Pythonilla luodut datanäytteet

Loin Pythonilla erilaisia näytteitä datasta, jotta voisin tutkia ja analysoida sitä tarkemmin:

### Datan esikäsittely
Käytin Pandas-kirjastoa datan lataamiseen ja käsittelyyn. Tämä sisälsi virheellisten arvojen suodattamisen, puuttuvien arvojen täyttämisen ja sarakkeiden uudelleenmuotoilun.

```python
import pandas as pd

# Datan lataaminen CSV-tiedostosta
data = pd.read_csv('data.csv')

# Virheellisten arvojen suodattaminen
data = data[data['Department'].apply(lambda x: not x.isnumeric() and len(x) < 10)]

# Puuttuvien arvojen käsittely
data.fillna('Unknown', inplace=True)
```

### Tilastollinen analyysi
Suoritin perusanalyysiä, kuten keskiarvon, mediaanin ja hajonnan laskemista eri osastoille.

```python
# Keskiarvon laskeminen
average_contacts = data.groupby('Department').size().mean()

# Mediaanin laskeminen
median_contacts = data.groupby('Department').size().median()
```
### Visualisoinnit
Käytin Matplotlib- ja Seaborn-kirjastoja luodakseni visualisointeja, kuten histogrammeja ja boxplotteja, jotka auttoivat ymmärtämään datan jakaumaa.

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Histogrammi osastojen kontaktimääristä
plt.figure(figsize=(10, 6))
sns.histplot(data['Department'], bins=30)
plt.title('Distribution of Contacts per Department')
plt.xlabel('Department')
plt.ylabel('Number of Contacts')
plt.show()
```
### Syvällinen analyysi
Analysoin dataa tarkemmin luomalla pivot-tauluja ja ristiintaulukoita, jotka auttoivat ymmärtämään yhteyksiä eri muuttujien välillä.

```python
# Pivot-taulu osastojen kontaktimääristä
pivot_table = data.pivot_table(index='Department', values='Contact_ID', aggfunc='count')
```
### Yhteenveto Oppimistani Asioista, Skripteistä ja Visualisoinneista

#### Tärkeimmät Oppimiskohdat

1. **Tietojen Esikäsittely ja Suodatus**:
   - Tietojen esikäsittelyssä käytin pandas-kirjastoa CSV-tiedostojen lataamiseen ja käsittelemiseen.
   - Suodattamalla pois yritykset, joilta puuttui vuotuinen liikevaihto, varmistin, että analyysini oli tarkka ja merkityksellinen.

2. **Teknologioiden Erittely ja Käsittely**:
   - Eritin teknologiat yksittäisiksi kohteiksi käyttämällä pandas-kirjaston `str.split` ja `stack` -toimintoja.
   - Muutin teknologioiden läsnäolo- tai poissaolotiedot DataFrame-muotoon käyttämällä `pd.get_dummies` -toimintoa.

3. **Korrelaatioanalyysi**:
   - Laskin korrelaatiot eri teknologioiden ja vuotuisen liikevaihdon välillä.
   - Laskin myös korrelaation teollisuuden ja vuotuisen liikevaihdon välillä.

4. **Suorituskyvyn Parantaminen**:
   - Optimoidakseni koodia käytin vektorisoituja operaatioita `lambda`-toimintojen sijaan, mikä paransi suorituskykyä ja selkeyttä.
   - Käytin `pd.concat` -toimintoa tehokkaaseen DataFrame-käsittelyyn ja vältyin mahdollisilta suorituskykyongelmilta.

5. **Visualisoinnit ja Tietojen Esittäminen**:
   - Loihin visualisointeja Power BI:ssä, jotka auttoivat ymmärtämään korrelaatioita eri teknologioiden, teollisuuksien ja vuotuisen liikevaihdon välillä.

#### Tärkeimmät Skriptit ja Niihin Tehdyt Suorituskykyparannukset

1. **Perusskriptit Tietojen Käsittelyyn**:
   - Lataaminen ja suodattaminen:
     ```python
     companies_df = pd.read_csv("C:\\Users\\Juhom\\Downloads\\Companies.csv")
     companies_with_revenue_df = companies_df[companies_df['Annual_Revenue'].notna()].copy()
     ```
   - Teknologioiden erittely:
     ```python
     all_technologies = companies_with_revenue_df['Technologies'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
     unique_technologies = all_technologies.unique()
     ```

2. **Teknologioiden Läsnäolon Käsittely**:
   - `pd.get_dummies` -toiminnon käyttö:
     ```python
     technology_presence_df = pd.get_dummies(all_technologies, prefix='', prefix_sep='').groupby(level=0).max()
     technology_presence_df = technology_presence_df.reindex(columns=unique_technologies, fill_value=0)
     companies_with_revenue_df = pd.concat([companies_with_revenue_df.reset_index(drop=True), technology_presence_df], axis=1)
     ```

3. **Korrelatiivinen Analyysi**:
   - Korrelaatioiden laskeminen:
     ```python
     correlation_with_revenue = final_df[unique_technologies.tolist() + ['Annual_Revenue']].corr()['Annual_Revenue'].drop('Annual_Revenue')
     industry_correlation = pd.get_dummies(final_df['Industry'])
     industry_correlation['Annual_Revenue'] = final_df['Annual_Revenue']
     industry_correlation_corr = industry_correlation.corr()['Annual_Revenue'].drop('Annual_Revenue')
     ```

4. **Suorituskykyä Parantavat Muutokset**:
   - Vektorisoitujen operaatioiden käyttö:
     ```python
     tech_corr_matrix = final_df[unique_technologies].values * correlation_with_revenue.values
     final_df['Tech_Correlation_with_revenue'] = tech_corr_matrix.sum(axis=1)
     ```

5. **Lisätyt Tiedot CSV-tiedostoihin**:
   - Keskiarvon ja mediaanin laskeminen:
     ```python
     avg_revenue = final_df['Annual_Revenue'].mean()
     median_revenue = final_df['Annual_Revenue'].median()
     normalized_median_revenue = round(median_revenue, 2)
     ```

   - Tallentaminen CSV-tiedostoihin:
     ```python
     correlation_with_revenue_df['Average_Revenue'] = avg_revenue
     correlation_with_revenue_df['Median_Revenue'] = median_revenue
     correlation_with_revenue_df['Normalized_Median_Revenue'] = normalized_median_revenue
     correlation_with_revenue_df.to_csv('technology_revenue_correlation_all.csv', index=False)
     industry_correlation_df['Average_Revenue'] = avg_revenue
     industry_correlation_df['Median_Revenue'] = median_revenue
     industry_correlation_df['Normalized_Median_Revenue'] = normalized_median_revenue
     industry_correlation_df.to_csv('industry_revenue_correlation.csv', index=False)
     ```

#### Visualisoinnit Power BI:ssä

1. **Gauge Visualization**:
   - Käytin mittarivisualisointia näyttämään yhteyshenkilöiden prosenttiosuutta, joilla on `Apollo_Account_Id` liitettynä yritykseen.

2. **Korrelatiiviset Visualisoinnit**:
   - Loihin pylväsdiagrammeja näyttämään eri teknologioiden korrelaatiot vuotuisen liikevaihdon kanssa.
   - Loihin myös visualisointeja eri teollisuuksien ja vuotuisen liikevaihdon korrelaatioista.

3. **Yhteenvetotiedot**:
   - Lisäsin korttivisualisointeja näyttämään keskiarvoisen ja mediaanisen liikevaihdon sekä normalized median revenuen.

Näiden parannusten avulla sain tehokkaamman ja selkeämmän skriptin, joka tuotti hyödyllisiä ja helposti visualisoitavia tuloksia Power BI:ssä. Tämä auttoi minua ymmärtämään paremmin yritysten ja teknologioiden välisiä suhteita sekä niiden vaikutuksia vuotuiseen liikevaihtoon.

