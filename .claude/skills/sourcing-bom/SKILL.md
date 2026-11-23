---
name: sourcing-bom
description: Recherche de composants et de fournitures (prix, disponibilité, fournisseurs, liens) et remplissage de projet/bom.csv. À utiliser pour faire la liste de courses d'un projet, comparer des fournisseurs ou chiffrer le coût.
---

# Sourcing et BOM

## Workflow

1. Lis la liste des composants dans `projet/decisions.md` et les contraintes de `projet/spec.md` (budget, délai).
2. N'oublie pas ce qui n'est pas sur le schéma : visserie (vis du boîtier, cf. `diametre_trou_vis`), câbles, connecteurs mâles d'en face, filament, alim externe, PCB lui-même.
3. Pour chaque ligne, cherche **au moins 2 fournisseurs** (ex. LCSC, Mouser, Digikey, Farnell, AliExpress pour le générique). Recherches indépendantes → lance-les en parallèle.
4. Remplis `projet/bom.csv` : une ligne par composant, avec `date_releve` (AAAA-MM-JJ).
5. Lance `python scripts/check_bom.py`.

## Règles

- Ne jamais inventer un prix ou un lien. Pas trouvé → `statut = A_VERIFIER` et une note.
- Prix unitaire **à la quantité achetée** (attention aux lots minimum : note-le dans `notes`).
- Un équivalent moins cher ou plus dispo → propose-le dans `notes`, ne remplace pas sans validation de l'électronicien.
- Ne jamais commander ni ajouter au panier : l'humain achète.

## Colonnes de bom.csv

`ref_schema` (R1, U2…), `designation`, `reference_fabricant`, `quantite`, `prix_unitaire_eur`, `fournisseur`, `lien`, `date_releve`, `statut` (OK / A_VERIFIER / ALTERNATIVE), `notes`.
