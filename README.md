# Ohjelmistotekniikka, harjoitustyö

Tämän projektin idea on luoda alusta **hahmorekisterille**. Kun joku luo tarinaa, jossa esiintyy paljon hahmoja, on hyödyllistä pitää kirjaa niistä ja niiden relaatioista.

## Linkit
- [Vaatimusmäärittely](/dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](/dokumentaatio/tuntikirjanpito.md)
- [Changelog](/dokumentaatio/changelog.md)

## Asennus

1. Riippuvuudet:

```
poetry install
```

2. Build:

```
poetry run invoke build
```

3. Käynnistys:

```
poetry run invoke start
```

## Muut komennot

### Testaus

```
poetry run invoke test
```

### Testikattavuus

```
poetry run invoke coverage-report
```

Tiedosto *index.html* löytyy hakemistosta *htmlcov* juurikansiossa.
