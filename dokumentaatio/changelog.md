# Changelog

## Viikko 3

- Käyttäjä näkee kaikki tarinat pääsivussa
- Käyttäjä voi lisätä tarinoita, antaa niille nimen ja kuvauksen (ei vielä näy missään)
- Käyttäjä voi poistaa kaikki tarinat
- Käyttäjä pääsee tarinan sivulle, jossa lukee tarinoiden lukumäärä, tarinan id ja nimi
- Lisätty luokat:
    - Database: vastaa tietokantaoperaatioista
    - StoryService: vastaa solluslogiikasta luokasta Story. Eli yhdistää tarina-olioita ja tietokantaa
- Testattu StoryService:
    - Tarinan luominen
    - Tarinoiden luominen liian pitkällä tai puuttuvalla nimellä
    - Tarinoiden määrän laskeminen
    - Tarinoiden haku

## Viikko 4

- Lisätty pylint