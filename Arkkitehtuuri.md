```mermaid
flowchart TD
 subgraph DataComponents["DataComponents"]
        SQLperusjoukko["SQL Perusjoukko ilman toimenpiteitä"]
        SQLSeg["SQL Segmentti kohdistuneilla toimenpiteillä"]
        PythonSQL["Python SQL CombinedMethods Python + OpenAI + Azure"]
        MasterDataUnit["Master Data Unit yhdistetty tietojoukko"]
  end
 subgraph Segmentointi["Segmentointi"]
        Project["Project"]
        Valence["Valence"]
  end
 subgraph Validointi["Validointi"]
        DatanHakeminen["Datan hakeminen"]
        Varasto["Varastosta"]
        UusiTieto["Uuden tiedon lisääminen"]
        TietokantaHallinta["Tietokannan hallinta methodit"]
        DatanRikastus["Datan rikastus"]
        VientiCRM["Viedään data Monday CRM"]
  end
 subgraph Ylläpito["Ylläpito"]
        Testaus["Testaus"]
        Kontaktidata["Kontaktidatan testaus"]
        DomainTest["Domainin testaus"]
        SkriptiTest["Skriptien tulosten testaus"]
        ValidointiTest["Validoinnin testaus"]
        LinkitysHallinta["Linkityksen hallinta"]
        MondayLinkitys["Monday linkityksen hallinta min prosenttia"]
        SQLLinkitys["SQL linkityksen hallinta SQLSeg min prosenttia"]
  end
 subgraph Uudistaminen["Uudistaminen"]
        Skriptit["Skriptit Pythonilla"]
        MuokkausData["Muokkaavat dataa konsultoinnin mukaisesti"]
        YleinenAsiakaskohtainen["Yleisellä tasolla ja asiakaskohtaisesti"]
        RikastaminenData["Rikastavat dataa"]
        DataSelitys["Kertovat datasta"]
        Raportointi["Valmistelevat datan raportointia varten"]
        GUI["Graafinen käyttöliittymä"]
        KonsultinKaytto["Konsultin käytössä"]
        AsiakasValinta["Asiakkaan valinta"]
        YleisetToiminnot["Yleiset operaatiot"]
        DatanTuonti["Datan tuonti toiminnanohjausjärjestelmään"]
  end
 subgraph Tekoäly["Tekoäly"]
        BingOpenAI["Bing Search API ja Open AI API"]
        ManuaalistenTehtavien["Automatisoi manuaalisia tehtäviä"]
        UusiTietoTallennus["Uuden tiedon tallennus uuteen formaattiin"]
        Ennakkokasittely["Ennakkokäsittelee vastauksia listaan"]
        Regex["Vähentää regex-työmäärää"]
        ProjektinTiedot["Projektin tiedot Monday CRM:ään ja MasterDataan"]
        OpenAIAPI["Open AI API"]
        PaikallinenKonsultointi["Paikallinen konsultointi Monday ja SQL/MasterData"]
        ValidointiToimet["Osittainen validointi dataan"]
        Parametrit["Toimii ohjeilla ja parametreilla"]
        SisallonLuonti["Räätälöidyn sisällön luonti esim. kampanjaan"]
        Segmentointi
        ChatGPT["ChatGPT eli CustomGPT"]
        Valivaihe["Toimii välivaiheena ennen täyttä automaatiota"]
        KehittyminenTehtavaan["Kehittyy tehtävään"]
        DynaaminenArkkitehtuuri["Soveltuu dynaamiseen arkkitehtuuriin"]
  end
 subgraph Prosessit["Prosessit"]
        Ylläpito
        Uudistaminen
        Tekoäly
  end
    DatanHakeminen --> Varasto & UusiTieto & TietokantaHallinta & DatanRikastus
    DatanRikastus --> VientiCRM & VientiCRM
    Testaus --> Kontaktidata & DomainTest & SkriptiTest & ValidointiTest
    LinkitysHallinta --> MondayLinkitys & SQLLinkitys
    Skriptit --> MuokkausData & YleinenAsiakaskohtainen & RikastaminenData & DataSelitys & Raportointi
    GUI --> KonsultinKaytto & AsiakasValinta & YleisetToiminnot & DatanTuonti
    BingOpenAI --> ManuaalistenTehtavien & UusiTietoTallennus & Ennakkokasittely & Regex & ProjektinTiedot
    OpenAIAPI --> PaikallinenKonsultointi & ValidointiToimet & Parametrit & SisallonLuonti & Segmentointi
    ChatGPT --> Valivaihe & KehittyminenTehtavaan & DynaaminenArkkitehtuuri
    SQLperusjoukko --> MasterDataUnit
    SQLSeg --> MasterDataUnit
    PythonSQL --> MasterDataUnit
    Segmentointi --> MasterDataUnit
    Validointi --> MasterDataUnit
    Uudistaminen --> MasterDataUnit
    Ylläpito --> MasterDataUnit
    Tekoäly --> MasterDataUnit
    Ylläpito -- Testaus ja linkityksen hallinta --> VientiCRM
    Uudistaminen -- Data- ja raportointivalmistelut --> VientiCRM
    Tekoäly -- Automaatio ja rikastus --> VientiCRM
    style MasterDataUnit fill:#FFD54F,stroke:#FF6F00,stroke-width:2px
    style VientiCRM fill:#B3E5FC,stroke:#0288D1,stroke-width:2px
    style Segmentointi fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px
    style Ylläpito fill:#E1BEE7,stroke:#8E24AA,stroke-width:1px
    style Uudistaminen fill:#FFEBEE,stroke:#E53935,stroke-width:1px
    style Tekoäly fill:#E0F7FA,stroke:#00ACC1,stroke-width:1px
    style Validointi fill:#E8F5E9,stroke:#43A047,stroke-width:2px
    style DataComponents fill:#E3F2FD,stroke:#2196F3,stroke-width:2px
    style Prosessit fill:#F3E5F5,stroke:#8E24AA,stroke-width:2px
