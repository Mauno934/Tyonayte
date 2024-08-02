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

### Tilastollinen analyysi
Suoritin perusanalyysiä, kuten keskiarvon, mediaanin ja hajonnan laskemista eri osastoille.

```python
# Keskiarvon laskeminen
average_contacts = data.groupby('Department').size().mean()

# Mediaanin laskeminen
median_contacts = data.groupby('Department').size().median()

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

### Syvällinen analyysi
Analysoin dataa tarkemmin luomalla pivot-tauluja ja ristiintaulukoita, jotka auttoivat ymmärtämään yhteyksiä eri muuttujien välillä.

```python
# Pivot-taulu osastojen kontaktimääristä
pivot_table = data.pivot_table(index='Department', values='Contact_ID', aggfunc='count')

