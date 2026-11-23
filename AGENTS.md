# AGENTS.md — Création de produit physique

Ce repo sert à concevoir un produit physique : **3D + électronique + liste de courses**.
Il est lu par Claude Code (via `CLAUDE.md`), GitHub Copilot (VS Code) et OpenCode.

## Principes

1. **Les fichiers sont la mémoire.** Tout ce qui compte est écrit dans `projet/`. Les agents ne se « parlent » pas : ils lisent et écrivent les mêmes fichiers.
2. **Une seule source de vérité pour les cotes :** `projet/interfaces.toml`. Aucune dimension en dur ailleurs.
3. **Tout est vérifiable.** Avant de dire « fini », lancer `scripts/verifier.sh`. Un travail non vérifié n'est pas fini.
4. **On ne s'auto-évalue pas.** La validation finale est faite par l'agent `relecteur`, qui n'a pas produit le travail.
5. **Ne rien inventer.** Une référence de composant, un prix ou une commande CLI non vérifiés sont marqués `A_VERIFIER`. Consulter la doc officielle (KiCad, build123d, datasheets) plutôt que deviner.
6. **L'humain tranche.** Conflit entre 3D et électronique, dépassement de budget, choix irréversible (commande, fabrication PCB) → on s'arrête et on demande.

## Fichiers du projet

| Fichier | Rôle | Qui écrit |
|---|---|---|
| `projet/spec.md` | Le besoin + critères d'acceptation | planification (validé par l'humain) |
| `projet/interfaces.toml` | Contrat 3D ↔ électronique : cotes PCB, trous, connecteurs, dissipation | électronique (la 3D propose, l'humain tranche) |
| `projet/bom.csv` | Liste de courses | sourcing |
| `projet/decisions.md` | Choix faits et pourquoi | tout le monde |
| `projet/revue.md` | Rapports du relecteur, itération par itération | relecteur |
| `projet/retro.md` | Ce qui a coincé → améliorations du système | rétro |
| `cad/` | Modèles 3D en code (build123d) | 3D |
| `elec/` | Projet KiCad | électronique |
| `exports/` | STEP, STL, Gerber, rapports (généré, ne pas éditer) | scripts |

## Workflow : planifier → produire → évaluer (boucle)

La session principale joue l'**orchestrateur**. Détail dans le skill `nouveau-produit`.

1. **Planifier** — transformer l'idée en `spec.md` (avec critères d'acceptation chiffrés) et en premier jet de `interfaces.toml`. Faire valider par l'humain avant la suite.
2. **Produire en parallèle** — une fois `interfaces.toml` validé, lancer dans le même tour :
   - `concepteur-3d` → `cad/`, exports STEP/STL
   - `electronicien` → choix composants, calculs, `elec/`, met à jour `interfaces.toml`
   - `sourceur` → `bom.csv` (peut lancer plusieurs recherches en parallèle)
3. **Évaluer** — lancer `scripts/verifier.sh`, puis l'agent `relecteur` qui écrit son verdict dans `projet/revue.md`.
4. **Boucler** — corriger ce que le relecteur signale, revenir en 3. **Maximum 3 itérations**, ensuite on remonte à l'humain avec ce qui bloque.
5. **Rétro** — à la fin (ou à la fin d'une session), lancer le skill `retro`.

## Commandes

```bash
pip install -r requirements.txt   # build123d
scripts/verifier.sh               # build CAO + check d'encombrement + ERC/DRC (si KiCad) + check BOM
python cad/boitier.py             # régénère seulement la 3D
```

## Limites connues (à respecter)

- Le **routage et le placement PCB** se font par l'humain (ou l'autorouteur). L'IA propose, relit, lance l'ERC/DRC.
- Les STL sont **presque prêts à imprimer** : le slicer et les réglages d'impression restent à l'humain.
- Les prix et la disponibilité changent : toujours noter la date de relevé dans `bom.csv`.
