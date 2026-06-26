# GameOfLife

Rozšíření Conwayovy [Hry života](https://cs.wikipedia.org/wiki/Hra_%C5%BEivota) o lokální multiplayer, herní módy a speciální buňky.

## Přehled

Klasická Hra života simuluje vývoj buněčných kolonií podle jednoduchých pravidel. Tato implementace přidává kompetitivní vrstvu, kde hráči soupeří o dominanci nad mřížkou, průběžně upgradují své organismy a ovlivňují průběh simulace.

## Funkce

### Multiplayer
- Lokální multiplayer pro 2–6 hráčů na jednom zařízení
- Každý hráč ovládá vlastní kolonii buněk s odlišnou barvou
- Po každých **X ticích** (nastavitelný interval) nastane **fáze akce** – hráč může:
  - Přidat nové buňky na mřížku
  - Vylepšit vlastnosti svých organismů
  - Umístit speciální budovy
  - Prodat vlastní buňky za částečný refund
  
### Vylepšení organismů
| Upgrade | Efekt |
|---|---|
| Agresivita | +0.5 váhy na každého souseda při obsazování nové buňky |
| Odolnost | +5 % šance na přežití mimo normální podmínky (max 90 %) |
| *(další plánované)* | ... |

### Speciální buňky
Budovy se umísťují během fáze akce a mění lokální pravidla simulace.

| Budova | Umístění | Efekt | Cena | Údržba |
|---|---|---|---|---|
| Sýpka | na vlastní buňku | Chrání okolní buňky stejného hráče před smrtí přelidněním | 100 | 25 / fázi |
| Mina | na prázdné pole | Po aktivaci (1 tick) exploduje při kontaktu s buňkou a zničí okolí | 50 | — |
| Továrna | na vlastní buňku | Generuje pasivní příjem každý tick | 150 | — |

### Ekonomika

Hráči získávají body za:
- Počet živých buněk na konci každého simulačního cyklu
- Továrny (pasivní příjem každý tick)
- Prodej vlastních buněk a budov (50 % refund)

Body se utrácejí za:
- Umísťování buněk
- Nákup upgradů
- Stavbu speciálních budov
- Údržby buňek

## Herní módy

**Dominance**
Zvítězí hráč s nejvíce živými buňkami po uplynutí X tiků.

**Eliminace**
Zvítězí poslední hráč, jehož kolonie přežije.

**Získání vlajek**
Na mřížce jsou rozmístěny speciální pozice (vlajky). Hráč, který pozici ovládá, průběžně získává body. Zvítězí hráč s nejvyšším skóre po X ticích.

*(další plánované)*

## Ovládání

### Fáze akce
| Klávesa | Akce |
|---|---|
| Klik | Umístit buňku / speciální budovu |
| `A` | Koupit upgrade Agresivita |
| `S` | Koupit upgrade Odolnost |
| `G` | Vybrat Sýpku pro umístění |
| `M` | Vybrat Minu pro umístění |
| `F` | Vybrat Továrnu pro umístění |
| `Backspace` | Přepnout režim mazání buněk |
| `Enter` | Potvrdit tah a předat na dalšího hráče |

### Simulace
| Klávesa | Akce |
|---|---|
| `R` | Resetovat mřížku (nové náhodné rozložení) |

### Konec hry
| Klávesa | Akce |
|---|---|
| `R` | Nová hra (návrat do menu) |

## Instalace

```bash
git clone git@github.com:thematycer/GameOfLife.git
cd GameOfLife
pip install pygame numpy
```

## Požadavky

- Python 3.10+
- pygame
- numpy

## Použití
Hra jde spustit pomocí:
```bash
python main.py
```

Po spuštění se zobrazí setup obrazovka kde lze nastavit:
- Počet hráčů (2–6)
- Herní mód (Dominance / Eliminace / Vlajky)
- Délku hry (neplatí pro eliminaci)
- Počáteční skóre
- Interval fáze akce
- Počáteční rozložení (náhodné / prázdné)
- Velikost mřížky (Malá / Střední / Velká)

## Testování

Testy jdou spustit pomocí příkazu: 

```bash
pytest .\test_main.py -v 
```

## Struktura projektu

```
GameOfLife/
├── main.py       # vstupní bod, game loop
├── game.py       # hlavní herní logika
├── grid.py       # simulace mřížky (GoL pravidla)
├── player.py     # hráč, upgrady, ekonomika
├── modes.py      # herní módy (Dominance, Eliminace, Vlajky)
├── special.py    # speciální buňky a jejich efekty
├── ui.py         # vykreslování panelů
├── setup.py      # setup obrazovka
├── config.py     # konstanty a nastavení
└── test_main.py  # testy
```

