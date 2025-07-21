# Genera PDF a partir d'un fitxer CSV amb el següent format:
#    codi_tematic_1,fitxa_1.pdf
#    codi_tematic_1,fitxa_2.pdf
#    codi_tematic_2,fitxa_3.pdf
#    codi_tematic_2,fitxa_4.pdf
#
# Els fitxers generats duen el nom del codi temàtic
#
# Per exemple:
# python3 ajunta-fitxes.py test/fitxes.cvs
#
import argparse
import csv
import os
import warnings
warnings.filterwarnings('ignore', module='.*pypdf.*')
import pypdf
import re

ROW_FIELDS=('codi_tematic', 'fitxa')

class Fitxa:
    def __init__(self, nom: str):
        self.nom = nom
        self.pagines = [] # llista de fitxers que s'han d'incloure en aquesta fitxa

    # Genera un PDF per aquesta fitxa en concret
    def GeneraPdf(self):
        nom_fitxer = f"{self.nom}.pdf"
        if os.path.isfile(nom_fitxer):
            print(f"Error: el fitxer {nom_fitxer} ja existeix, no se sobreescriurà")
            return
        pdf = pypdf.PdfWriter(nom_fitxer)
        print(f"S'està escrivint {nom_fitxer}")
        for pagina in self.pagines:
            pdf.append(pagina)
        pdf.write(nom_fitxer)
        pdf.close()
        print()

    # pagina és el nom del fitxer sencer (p.ex. 500_01.pdf)
    def AfegeixPagina(self, pagina: str):
        self.pagines.append(pagina)

    def __repr__(self):
        return f"Fitxa('{self.nom}', {self.pagines})"


class Calaixera:
    def __init__(self):
        self.fitxes = {}
        self.regexp = re.compile(r'(.*)_(.*).pdf')

    def AfegeixFitxa(self, codi: str, fitxer_pdf: str):
        fitxa = self.fitxes.setdefault(codi, Fitxa(codi))
        fitxa.AfegeixPagina(fitxer_pdf)

    def GeneraFitxes(self):
        for k, fitxa in self.fitxes.items():
            fitxa.GeneraPdf()

    def MostraFitxes(self):
        for _, fitxa in self.fitxes.items():
            print(fitxa)


def read_file(cvs_file, dry_run: bool):
    calaix = Calaixera()
    reader = csv.DictReader(cvs_file, fieldnames=ROW_FIELDS, restkey='__invalid__')
    for data in reader:
        codi = data.get(ROW_FIELDS[0])
        fitxer_pdf = data.get(ROW_FIELDS[1])
        if codi and fitxer_pdf and os.path.isfile(fitxer_pdf):
            calaix.AfegeixFitxa(codi, fitxer_pdf)
        else:
            print("Error, potser el fitxer {fitxer_pdf} no existeix")

    if dry_run:
        calaix.MostraFitxes()
    else:
        calaix.GeneraFitxes()


# Defineix els arguments del programa
parser = argparse.ArgumentParser(description='Ajunta Fitxes')
parser.add_argument('cvs_file', help='Fitxer en format CVS', metavar='Fitxer',
                    type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('--prova', help='No crea cap fitxer. Només indica quines accions es durien a terme', action='store_true')

args = parser.parse_args()

read_file(args.cvs_file, args.prova)
