# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla käyttäjä voi hallita omia hahmojaan tietyssä tarinassa. Sovelluksessa voi alustaa tarinan ja lisätä siihen hahmoja: antaa niistä perustietoja, kuvia ja muodostaa hahmojen välisiä suhteita. Sovellus on tarkoitettu vain yhdelle käyttäjälle.

## Suunnitelut toiminnallisuudet

### Pääsivu

Pääsivussa näkyy lista omista tarinoita.

- Pääsivulle voi lisätä uusia tarinoita.
- Tarinalle annetaan nimi ja vapaaehtoinen kuvaus.
- Tarinan nimi ja kuvaus voidaan muokata.
- Voi poistaa tarinoita, mikä poistaa myös kaikki tarinan hahmoja.

Pääsivusta pääsee jonkin tarinan sivulle.

### Tarinan sivu

Tarinan sivussa näkyy lista hahmoja ja hahmojen tilasto (esim. keski-ikä, keskipituus, miten paljon on nais- tai mieshahmoja jne.)

- Voi luoda uusia hahmoja. Hahmojen mahdollisia ominaisuuksia:
    - Nimi
    - Sukupuoli (nainen, mies tai tuntematon)
    - Syntymäpäivä
    - Ikä
    - Pituus
    - Paino
    - Ulkonäön kuvaus
    - Luonteen kuvaus
    - Historia (mitä tapahtuu hahmolle tarinassa)
    - Kuva (ladataan käyttäjän koneelta)
    - Lisätietoa
- Hahmon luomisen jälkeen näkyy lista kaikkia hahmoja ja niiden omalle sivulle pääsee klikkaamalla.
- Sivun alapuolella näkyy tilasto, jossa voi tarkistaa:
    - Hahmojen keski-ikä
    - Montako prosentteja naisia, miehiä tai ei tiedossa olevia sukupuolia
    - Keskipituus
    - Keskipaino

### Hahmon sivu

Sivussa näkyy kaikki yllä mainitut tiedot. On mahdollista:

- Poistaa hahmon
- Muokata kumpi tahansa kohta
- Lisätä suhteita olemassaolevien hahmojen väliin
    - Jos lisätään kaksisuuntainen suhde (esim. "parent"), myös toisen hahmon sivu päivitetään
    - On mahdollista lisätä yksisuuntaisia suhdeita (esim. "love interest")

Mahdolliset suhteet ovat:

- Kaksisuuntaiset:
    - Parent/child
    - Grandparent/grandchild
    - Sibling
    - Cousin
    - Step-parent/stepchild
    - Wife/Husband
    - Girlfriend/Boyfriend
    - Friend
    - Collegue
    - Classmate
- Yksisuuntaiset:
    - Love interest
    - Enemy
    - Fan

Hahmolla voi olla muutama suhde toisen hahmon kanssa, mikäli se ei ole fyysisesti mahdoton suhde (esim. joku ei voi olla samalla toisen henkilön lapsi ja vanhempi).