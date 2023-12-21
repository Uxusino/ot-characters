# Changelog

## Viikko 3

- Käyttäjä näkee kaikki tarinat pääsivussa
- Käyttäjä voi lisätä tarinoita, antaa niille nimen ja kuvauksen (ei vielä näy missään)
- Käyttäjä voi poistaa kaikki tarinat
- Käyttäjä pääsee tarinan sivulle, jossa lukee tarinoiden lukumäärä, tarinan id ja nimi
- Lisätty luokat:
    - Database: vastaa tietokantaoperaatioista
    - StoryService: vastaa sovelluslogiikasta luokasta Story. Eli yhdistää tarinaolioita ja tietokantaa
- Testattu StoryService:
    - Tarinan luominen
    - Tarinoiden luominen liian pitkällä tai puuttuvalla nimellä
    - Tarinoiden määrän laskeminen
    - Tarinoiden haku

## Viikko 4

- Lisätty pylint
- Käyttäjä voi lisätä hahmoja ja antaa niille kaikki perustiedot
    - Kuvia ei vielä saa lisätä
- Tarinan sivulla nyt näkyy lista hahmoja
- Lisätty luokat:
    - CharacterService: vastaa sovelluslogiikasta luokasta Character; yhdistää hahmo-olioita ja tietokantaa
- Testattu CharacterService:
    - Hahmon luominen
    - Hahmojen haku

## Viikko 5

- Käyttäjä voi lisätä kuvan luomaansa hahmoon
- Lisätty luokka Repository joka hoitaa kuvien poistamisesta
- Uusi näkymä: CharacterView
- Käyttäjä pääsee hahmon sivulle, missä näkyy hahmon tiedot

## Viikko 6

- Käyttäjä voi lisätä suhteen yhdelle hahmolle toisen hahmon kanssa (tai itsensä kanssa)
- Kaksisuuntainen suhde päivittää automaattisesti myös toisen hahmon suhteet
- Lisätty tilasto tarinan hahmojen keski-iälle

## Viikko 7

- Uusi luokka Formatter, joka käsittelee merkkijonoja
- Käyttäjä voi muokata tarinan nimeä ja kuvausta
- Käyttäjä voi poistaa yksittäisen tarinan
- Käyttäjältä kysytään, haluaako hän oikeasti poistaa tarinan tai tarinat
- Luokka Database jaettu kahteen luokkaan: StoryDatabase ja CharacterDatabase. Alkuperäinen moduuli alkoi olla liian pitkä
- Lisätty tilastot sukupuoliprosentteille, keskipituudelle, keskipainolle ja hahmojen täyteysprosentteille
- Käyttäjä voi poistaa yksittäisen hahmon
- Käyttäjä voi muokata hahmon tietoja ja kuvaa
- Käyttäjä voi poistaa hahmon yksittäisiä suhteita