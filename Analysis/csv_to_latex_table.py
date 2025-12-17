import pandas as pd
import pyperclip
import os


def csv_to_latex(file_path, copy_to_clipboard=True):
    """Fait des tableaux LaTeX à partir de fichiers CSV. 
    Les tableaux sont un peu moche mais c'est une base (évide de devoir pitonner les valeurs du csv au moins)"""
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier '{file_path}' est introuvable.")
        return None

    try:
        df = pd.read_csv(file_path)

        # C'est ici que ça change : on utilise .style.to_latex
        latex_code = df.style.format(precision=2)\
            .hide(axis='index')\
            .to_latex(
                hrules=True,
                column_format="c" * len(df.columns), 
                position="h"
            )
        
        print(latex_code)

        if copy_to_clipboard:
            pyperclip.copy(latex_code)
            print("Copié dans le presse-papier !")

        return latex_code

    except Exception as e:
        print(f"Erreur : {e}")
        return None


if __name__ == "__main__":
    mon_fichier = 'Analysis\\resultats_stratification_v2.csv'
    csv_to_latex(mon_fichier, copy_to_clipboard=False)