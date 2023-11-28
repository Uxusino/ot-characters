# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla käyttäjä voi hallita omia hahmojaan tietyssä tarinassa. Sovelluksessa voi alustaa tarinan ja lisätä siihen hahmoja: antaa niistä perustietoja, kuvia ja muodostaa hahmojen välisiä suhteita. Sovellus on tarkoitettu vain yhdelle käyttäjälle.

## Suunnitelut toiminnallisuudet

### Pääsivu

Pääsivussa näkyy lista omista tarinoita.

- Pääsivulle voi lisätä uusia tarinoita. *(tehty)*
- Tarinalle annetaan nimi ja vapaaehtoinen kuvaus. *(tehty)*
- Tarinan nimi ja kuvaus voidaan muokata.
- Voi poistaa tarinoita, mikä poistaa myös kaikki tarinan hahmoja.
- Voi poistaa kaikki tarinat yhdellä klikkauksella. *(tehty)*

Pääsivusta pääsee jonkin tarinan sivulle.

### Tarinan sivu

Tarinan sivussa näkyy lista hahmoja ja hahmojen tilasto (esim. keski-ikä, keskipituus, miten paljon on nais- tai mieshahmoja jne.)

- Voi luoda uusia hahmoja. Hahmojen mahdollisia ominaisuuksia:
    - Nimi *(tehty)*
    - Sukupuoli (nainen, mies tai tuntematon) *(tehty)*
    - Syntymäpäivä *(tehty)*
    - Ikä *(tehty)*
    - Pituus *(tehty)*
    - Paino *(tehty)*
    - Ulkonäön kuvaus *(tehty)*
    - Luonteen kuvaus *(tehty)*
    - Historia (mitä tapahtuu hahmolle tarinassa) *(tehty)*
    - Kuva (ladataan käyttäjän koneelta)
    - Lisätietoa *(tehty)*
- Hahmon luomisen jälkeen näkyy lista kaikkia hahmoja. *(tehty)*
- Hahmon sivulle pääsee klikkaamalla.
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
    - Aunt/uncle - niece/nephew
    - Step-parent/stepchild
    - Relative (jos ei ole läheinen sukulainen)
    - Wife/Husband
    - Girlfriend/Boyfriend
    - Friend
    - Collegue
    - Classmate
    - Alter ego
    - Creator/creation
- Yksisuuntaiset:
    - Love interest
    - Enemy
    - Fan

Hahmolla voi olla muutama suhde toisen hahmon kanssa. On mahdollista lisätä "former" (entinen) jokaiseen suhteeseen.