---
name: conception-3d
description: Conception 3D paramétrique en Python (build123d) d'un boîtier ou d'une pièce, pilotée par projet/interfaces.toml, avec export STEP/STL et vérification d'encombrement. À utiliser pour toute modélisation, modification de boîtier, ou intégration d'un PCB KiCad dans la 3D.
---

# Conception 3D

## Règles

- Tout passe par du code dans `cad/` (build123d). Pas de cote en dur : tout vient de `projet/interfaces.toml`.
- Besoin d'un nouveau paramètre ? Ajoute-le dans `interfaces.toml` (section `[boitier]` ou nouvelle section), avec un commentaire.
- Avant d'utiliser une fonction build123d dont tu n'es pas sûr, vérifie dans la doc officielle : https://build123d.readthedocs.io

## Workflow

1. Lis `projet/spec.md` (contraintes, fabrication) et `projet/interfaces.toml`.
2. Modifie / étends `cad/boitier.py` (ou crée une pièce dans `cad/<piece>.py` sur le même modèle : `charger()` → `geometrie()` → exports).
3. Lance `python cad/boitier.py` puis `python scripts/check_fit.py`.
4. Corrige jusqu'à ce que le check passe. Une collision = un vrai problème, ne l'ignore pas.
5. Note dans `projet/decisions.md` tout choix de forme non évident.

## Intégrer le vrai PCB KiCad

Quand l'électronicien a un PCB :
1. Dans KiCad, place l'origine de perçage (ou de grille) au coin bas-gauche du PCB.
2. Exporte le STEP vers `exports/pcb.step` avec `kicad-cli pcb export step`. **Vérifie les options d'origine disponibles avec `kicad-cli pcb export step -h`** (elles varient selon la version de KiCad) et utilise celle qui correspond à l'origine choisie.
3. Relance `python scripts/check_fit.py` : il utilise automatiquement `pcb.step` au lieu de l'enveloppe.
4. Si le PCB apparaît décalé (collision partout), c'est un problème d'origine : vérifie l'étape 1 avant de toucher à la 3D.

## Impression (presque prêt)

- Épaisseurs de paroi ≥ 2 mm pour du PLA/PETG standard, sauf contrainte dans la spec.
- Le jeu d'emboîtement vient de `tolerance_impression`.
- Évite les surplombs > 45° non supportés, ou signale-les.
- Le STL est livré ; l'orientation et les réglages du slicer restent à l'humain. Note les recommandations (orientation, supports) dans `decisions.md`.
