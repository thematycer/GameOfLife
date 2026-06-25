# GameOfLife

Rozšíření Conwayovy [Hry života](https://cs.wikipedia.org/wiki/Hra_%C5%BEivota) o lokální multiplayer, herní módy a speciální buňky.

## Přehled

Klasická Hra života simuluje vývoj buněčných kolonií podle jednoduchých pravidel. Tato implementace přidává kompetitivní vrstvu, kde hráči soupeří o dominanci nad mřížkou, průběžně upgradují své organismy a ovlivňují průběh simulace.

## Funkce

### Multiplayer
- Lokální multiplayer pro více hráčů na jednom zařízení
- Každý hráč ovládá vlastní kolonii buněk s odlišnou barvou
- Po každých **X ticích** (nastavitelný interval) nastane **fáze akce** – hráč může:
  - Přidat nové buňky na mřížku
  - Vylepšit vlastnosti svých organismů

### Vylepšení organismů
| Upgrade | Popis |
|---|---|
| Agresivita | Zvýšená šance na obsazení pole sousedního organismu |
| Frekvence | Změna intervalu vyhodnocování pravide |
| Odolnost | Vyšší tolerance vůči přelidnění / osamělosti / agresivitě soupeře |
| *(další plánované)* | ... |

### Speciální buňky
Buňky s unikátními vlastnostmi, které mění lokální pravidla simulace.

| Buňka | Efekt |
|---|---|
| sýpka | Zabrání okolním buňkám zemřít hladem (přelidněním) |
| *(další plánované)* | ... |

Speciální buňky lze získat:
- Ručním umístěním hráčem během fáze akce
- Náhodnou **mutací** při simulaci

## Herní módy

**Dominance**
Zvítězí hráč s nejvíce živými buňkami po uplynutí X tiků.

**Eliminace**
Zvítězí poslední hráč, jehož kolonie přežije.

**Získání vlajek**
Na mřížce jsou rozmístěny speciální pozice (vlajky). Hráč, který pozici ovládá, průběžně získává body. Zvítězí hráč s nejvyšším skóre po X ticích.

*(další plánované)*
## Instalace

```bash
git clone https://github.com/uzivatel/game-of-life-multiplayer
cd game-of-life-multiplayer
...
```

## Požadavky

- Python 3.10+

## Použití

```bash

```

