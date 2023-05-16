import argparse
import csv
import os
import glob
from pypdf import PdfMerger

ROW_FIELDS = ('folder', 'begin', 'end', 'name')

class PdfConcatenator:
    def __init__(self, folder:str, begin:int, end:int, name:str, prefix_out:str=''):
        self.folder = folder
        self.begin = begin
        self.end = end
        self.name = f'{prefix_out}{name}.pdf'
        self.input_files = []
        self.missing = True

    def add_files(self):
        for n, pdf_file in enumerate(sorted(glob.glob(os.path.join(self.folder, '*.pdf'))), start=1):
            if n >= self.begin and n<= self.end:
                self.input_files.append(pdf_file)

        missing = (self.end - self.begin + 1) - len(self.input_files)

        if missing != 0:
            print(f"{self.name}: Manquen {missing} fitxers PDF")
        else:
            self.missing = False


class PdfConcatDryRunner(PdfConcatenator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def concatenate(self):
        if self.missing:
            print("ERROR: Manquen PDFs per crear el fitxer {self.name}:")
        else:
            print(f"\nEs crearia el fitxer {self.name} amb aquests PDF:")
        for f in self.input_files:
            print(f'\t{f}')
        print()


class PdfConcatFiles(PdfConcatenator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def concatenate(self):
        if self.missing:
            print("ERROR: Manquen PDFs per crear el fitxer {self.name}. No es pot continuar.")
            return

        merger = PdfMerger()
        for f in self.input_files:
            merger.append(f)

        merger.write(self.name)
        merger.close()
        print(f"S'ha desat el fitxer {self.name}")


def check_row(data: dict) -> bool:
    valid = True

    if data['folder'] is None:
        print('Manca el nom de la carpeta')
        valid = False
    elif not os.path.isdir(data['folder']):
        print('La carpeta {} no és vàlida'.format(data['folder']))
        valid = False

    if data['begin'] is None or data['end'] is None:
        print("Manca el PDF de destí o el d'orígen")
        valid = False
    else:
        # Make sure we got integers
        try:
            begin = int(data['begin'])
            end = int(data['end'])
        except ValueError:
            print("El camp d'inici o final no són nombres")
            valid = False
        else:
            data['begin'] = begin
            data['end'] = end

        if valid and (begin > end):
            print('El número de PDF inicial ({}) és més gran que el final ({})'.format(data['begin'], data['end']))
            valid = False
        elif valid and ((begin <= 0) or (end <= 0)):
            print('El número de PDF inicial ({}) o el final ({}) són negatius o zero'.format(data['begin'], data['end']))
            valid = False

    if data['name'] is None:
        print('Manca el nom del fitxer de destí')
        valid = False

    return valid


def process_row(data: dict, row_nr: int, dry_run: bool, prefix: str):
    if not check_row(data):
        print("Error a la línia {}".format(row_nr))
    else:
        if dry_run:
            concatenator = PdfConcatDryRunner(**data, prefix_out=prefix)
        else:
            concatenator = PdfConcatFiles(**data, prefix_out=prefix)
        concatenator.add_files()
        concatenator.concatenate()


def read_file(cvs_file, dry_run: bool, prefix: str):
    reader = csv.DictReader(cvs_file, fieldnames=ROW_FIELDS, restkey='__invalid__')
    for row_nr, data in enumerate(reader, start=1):
        process_row(data, row_nr, dry_run, prefix)


# Define arguments
parser = argparse.ArgumentParser(description='Ajunta PDF')
parser.add_argument('cvs_file', help='Fixer en format CVS', metavar='Fixer', type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('--dry-run', help='No crea cap fitxer. Només indica quines accions es durien a terme', action='store_true')
parser.add_argument('--prefix', help='Afegeix aquest prefix a cada fitxer', default='')

args = parser.parse_args()

read_file(args.cvs_file, args.dry_run, args.prefix)

