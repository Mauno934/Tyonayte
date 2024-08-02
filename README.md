# Tyonayte

Yhteenveto Oppimistani Asioista, Skripteistä ja Visualisoinneista
Tärkeimmät Oppimiskohdat
Tietojen Esikäsittely ja Suodatus:

Tietojen esikäsittelyssä käytin pandas-kirjastoa CSV-tiedostojen lataamiseen ja käsittelemiseen.
Suodattamalla pois yritykset, joilta puuttui vuotuinen liikevaihto, varmistin, että analyysini oli tarkka ja merkityksellinen.
Teknologioiden Erittely ja Käsittely:

Eritin teknologiat yksittäisiksi kohteiksi käyttämällä pandas-kirjaston str.split ja stack -toimintoja.
Muutin teknologioiden läsnäolo- tai poissaolotiedot DataFrame-muotoon käyttämällä pd.get_dummies -toimintoa.
Korrelaatioanalyysi:

Laskin korrelaatiot eri teknologioiden ja vuotuisen liikevaihdon välillä.
Laskin myös korrelaation teollisuuden ja vuotuisen liikevaihdon välillä.
Suorituskyvyn Parantaminen:

Optimoidakseni koodia käytin vektorisoituja operaatioita lambda-toimintojen sijaan, mikä paransi suorituskykyä ja selkeyttä.
Käytin pd.concat -toimintoa tehokkaaseen DataFrame-käsittelyyn ja vältyin mahdollisilta suorituskykyongelmilta.
Visualisoinnit ja Tietojen Esittäminen:

Loihin visualisointeja Power BI
ä, jotka auttoivat ymmärtämään korrelaatioita eri teknologioiden, teollisuuksien ja vuotuisen liikevaihdon välillä.
Tärkeimmät Skriptit ja Niihin Tehdyt Suorituskykyparannukset
Perusskriptit Tietojen Käsittelyyn:

Lataaminen ja suodattaminen:
python
Kopioi koodi
companies_df = pd.read_csv("C:\\Users\\Juhom\\Downloads\\Companies.csv")
companies_with_revenue_df = companies_df[companies_df['Annual_Revenue'].notna()].copy()
Teknologioiden erittely:
python
Kopioi koodi
all_technologies = companies_with_revenue_df['Technologies'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
unique_technologies = all_technologies.unique()
Teknologioiden Läsnäolon Käsittely:

pd.get_dummies -toiminnon käyttö:
python
Kopioi koodi
technology_presence_df = pd.get_dummies(all_technologies, prefix='', prefix_sep='').groupby(level=0).max()
technology_presence_df = technology_presence_df.reindex(columns=unique_technologies, fill_value=0)
companies_with_revenue_df = pd.concat([companies_with_revenue_df.reset_index(drop=True), technology_presence_df], axis=1)
Korrelatiivinen Analyysi:

Korrelaatioiden laskeminen:
python
Kopioi koodi
correlation_with_revenue = final_df[unique_technologies.tolist() + ['Annual_Revenue']].corr()['Annual_Revenue'].drop('Annual_Revenue')
industry_correlation = pd.get_dummies(final_df['Industry'])
industry_correlation['Annual_Revenue'] = final_df['Annual_Revenue']
industry_correlation_corr = industry_correlation.corr()['Annual_Revenue'].drop('Annual_Revenue')
Suorituskykyä Parantavat Muutokset:

Vektorisoitujen operaatioiden käyttö:
python
Kopioi koodi
tech_corr_matrix = final_df[unique_technologies].values * correlation_with_revenue.values
final_df['Tech_Correlation_with_revenue'] = tech_corr_matrix.sum(axis=1)
Lisätyt Tiedot CSV-tiedostoihin:

Keskiarvon ja mediaanin laskeminen:

python
Kopioi koodi
avg_revenue = final_df['Annual_Revenue'].mean()
median_revenue = final_df['Annual_Revenue'].median()
normalized_median_revenue = round(median_revenue, 2)
Tallentaminen CSV-tiedostoihin:

python
Kopioi koodi
correlation_with_revenue_df['Average_Revenue'] = avg_revenue
correlation_with_revenue_df['Median_Revenue'] = median_revenue
correlation_with_revenue_df['Normalized_Median_Revenue'] = normalized_median_revenue
correlation_with_revenue_df.to_csv('technology_revenue_correlation_all.csv', index=False)
industry_correlation_df['Average_Revenue'] = avg_revenue
industry_correlation_df['Median_Revenue'] = median_revenue
industry_correlation_df['Normalized_Median_Revenue'] = normalized_median_revenue
industry_correlation_df.to_csv('industry_revenue_correlation.csv', index=False)
Visualisoinnit Power BI
ä
Gauge Visualization:

Käytin mittarivisualisointia näyttämään yhteyshenkilöiden prosenttiosuutta, joilla on Apollo_Account_Id liitettynä yritykseen.
Korrelatiiviset Visualisoinnit:

Loihin pylväsdiagrammeja näyttämään eri teknologioiden korrelaatiot vuotuisen liikevaihdon kanssa.
Loihin myös visualisointeja eri teollisuuksien ja vuotuisen liikevaihdon korrelaatioista.
Yhteenvetotiedot:

Lisäsin korttivisualisointeja näyttämään keskiarvoisen ja mediaanisen liikevaihdon sekä normalized median revenuen.
Näiden parannusten avulla sain tehokkaamman ja selkeämmän skriptin, joka tuotti hyödyllisiä ja helposti visualisoitavia tuloksia Power BI
ä. Tämä auttoi minua ymmärtämään paremmin yritysten ja teknologioiden välisiä suhteita sekä niiden vaikutuksia vuotuiseen liikevaihtoon.
