import os
import pypdf
import re

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
        print(f"S'està escrivint la fitxa {self.nom} a {nom_fitxer}")
        for pagina in sorted(self.pagines):
            pdf.append(pagina)
        pdf.write(nom_fitxer)
        pdf.close()
        print()

    # pagina és el nom del fitxer sencer (p.ex. 500_01.pdf)
    def AfegeixPagina(self, pagina: str):
        self.pagines.append(pagina)


class Calaixera:
    def __init__(self):
        self.fitxes = {}
        self.regexp = re.compile(r'(.*)_(.*).pdf')

    def Afegeix(self, nom_fitxer: str):
        m = self.regexp.fullmatch(nom_fitxer)
        if m:
            nom_fitxa = m.group(1)
            fitxa = self.fitxes.setdefault(nom_fitxa, Fitxa(nom_fitxa))
            fitxa.AfegeixPagina(nom_fitxer)

    def GeneraFitxes(self):
        for k, fitxa in self.fitxes.items():
            fitxa.GeneraPdf()

calaix = Calaixera()

# Fes una llista dels fitxers en aquest directori
for fitxer in os.listdir('.'):
    calaix.Afegeix(fitxer)

# Genera els Pdf per a cada fitxa
calaix.GeneraFitxes()
