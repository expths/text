from typing import Iterator
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
import csv


def smilesToSVG(smile: str) -> str:
    mol = Chem.MolFromSmiles(smile)
    d2d = rdMolDraw2D.MolDraw2DSVG(300, 300)
    d2d.DrawMolecule(mol)
    d2d.FinishDrawing()
    return d2d.GetDrawingText()


def write_to_ChemicalEquationFile(smile_name: str, svg: str) -> None:
    with open(f'./Chemical_equation_{smile_name}.svg', mode='w')as file:
        file.write(svg)


def generate_and_write_SVG(CSV_file_name: str) -> None:
    with open(CSV_file_name, mode='r')as smiles_file:
        smiles = csv.reader(smiles_file, delimiter=',')
        for smile in smiles:
            print(smile[0])
            svg = smilesToSVG(smile=smile[1])
            write_to_ChemicalEquationFile(smile[0], svg=svg)


generate_and_write_SVG('./smiles.csv')
