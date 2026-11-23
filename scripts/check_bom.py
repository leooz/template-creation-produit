"""Vérifie projet/bom.csv : champs obligatoires, lignes à vérifier, total vs budget de spec.md.

Code de sortie : 0 si OK (avertissements possibles), 1 en cas d'erreur.
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OBLIGATOIRES = ["designation", "reference_fabricant", "quantite", "prix_unitaire_eur", "fournisseur", "lien", "date_releve"]

erreurs, total = 0, 0.0
with open(ROOT / "projet" / "bom.csv", newline="", encoding="utf-8") as f:
    lignes = list(csv.DictReader(f))

if not lignes:
    print("ATTENTION  bom.csv est vide")

for i, l in enumerate(lignes, start=2):
    nom = l.get("designation") or f"ligne {i}"
    manquants = [c for c in OBLIGATOIRES if not (l.get(c) or "").strip()]
    if manquants:
        print(f"ERREUR     {nom} : champs manquants {manquants}")
        erreurs += 1
        continue
    if "A_VERIFIER" in ",".join(l.values()).upper():
        print(f"ATTENTION  {nom} : marqué A_VERIFIER")
    try:
        total += float(l["quantite"]) * float(l["prix_unitaire_eur"].replace(",", "."))
    except ValueError:
        print(f"ERREUR     {nom} : quantité ou prix non numérique")
        erreurs += 1

print(f"INFO       total BOM : {total:.2f} €")

spec = (ROOT / "projet" / "spec.md").read_text(encoding="utf-8")
m = re.search(r"Budget composants max \(€\)\s*:\s*([\d.,]+)", spec)
if m:
    budget = float(m.group(1).replace(",", "."))
    if total > budget:
        print(f"ERREUR     total {total:.2f} € > budget {budget:.2f} €")
        erreurs += 1
    else:
        print(f"OK         total dans le budget ({budget:.2f} €)")
else:
    print("ATTENTION  pas de budget renseigné dans spec.md")

sys.exit(1 if erreurs else 0)
