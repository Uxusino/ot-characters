# Changelog

## Viikko 3

- Käyttäjä näkee kaikki tarinat pääsivussa
- Käyttäjä voi lisätä tarinoita, antaa niille nimen ja kuvauksen (ei vielä näy missään)
- Käyttäjä voi poistaa kaikki tarinat
- Lisätty luokat:
    - Database: vastaa tietokantaoperaatioista
    - StoryService: vastaa solluslogiikasta luokasta Story. Eli yhdistää tarina-olioita ja tietokantaa
- Testattu StoryService:
    - Tarinan luominen
    - Tarinoiden luominen liian pitkällä tai puuttuvalla nimellä
    - Tarinoiden määrän laskeminen
    - Tarinoiden haku