# Informació

Aquest programa permet ajuntar fitxers PDF d'acord amb les dades proporcionades
a través d'un fitxer en [format CSV](https://ca.wikipedia.org/wiki/CSV).

## Format del fixer

El fitxer CVS ha de tenir almenys 4 columnes, la primera és la carpeta on
es troben els fitxers, la segona el número del primer fitxer, la tercera
el número del darrer fitxer, i finalment la quarta el nom del fitxer resultant.

| Carpeta | PDF inicial  | PDF final | Nom PDF |
|---------|--------------|-----------|---------|
| 680     |       4      |      10   |    1    |

### Exemple
```
110,1,4,1
234,2,3,2
680,5,9,3
```

## Ús del programa

La manera més bàsica és proporcionar el fixer CSV com a primer paràmetre
```
python ajunta-pdf.py dades.csv
[...]
```

## Mode de prova

Es pot executar el fitxer en mode de prova indicant `--dry-mode` a la línia d'ordres.
Això vol dir que **no s'escriurà cap fitxer PDF**, simplement s'indicaran quins fitxers
es crearien, d'acord amb les dades proporcionades, i quins fitxers es farien servir per
crear-los.
```
python ajunta-pdf.py --dry-mode dades.csv
```

## Prefix

Es pot afegir un prefix a tots els fitxers de sortida mitjançant `--prefix` a la
línia d'ordres:
```
python ajunta-pdf.py --prefix exemple_ dades.csv
```

Podeu afegir `--dry-run` per veure com quedarien els noms de fitxer final.

També podeu fer servir això per posar tots els fitxers de sortida en un directori
determinat, per exemple `sortida`:

**Linux** (i variants d'UNIX):
```
python ajunta-pdf.py --prefix sortida/exemple_ dades.csv
```

**Windows**
```
python ajunta-pdf.py --prefix sortida\exemple_ dades.csv
```

# Instal·lació

Aquest és un programa escrit en [Python](https://www.python.org/downloads/) que depèn del mòdul
pypdf. Per instal·lar-lo:
```
pip3 install pypdf
```

