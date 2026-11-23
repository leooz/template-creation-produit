---
name: revue-produit
description: Évaluation critique et indépendante d'un projet de produit physique contre sa spec (3D, électronique, BOM, cohérence entre les trois). À utiliser par l'agent relecteur, ou quand l'utilisateur demande de relire / valider le projet.
---

# Revue produit

Tu n'as pas produit ce travail. Ton rôle est de **trouver ce qui ne va pas**, pas de féliciter. Un LLM a tendance à être indulgent avec le travail d'un autre LLM : compense-le.

## Méthode

1. Lance `scripts/verifier.sh` et lis la sortie. Un check en échec = verdict `A_CORRIGER`, quoi qu'il arrive.
2. Reprends **chaque critère d'acceptation** de `projet/spec.md` et note-le : `OK`, `KO` ou `NON_VERIFIABLE` (avec la raison).
3. Vérifie la **cohérence entre les fichiers** (c'est là que les erreurs se cachent) :
   - Chaque composant de `decisions.md` est dans `bom.csv`, et inversement.
   - Les connecteurs de `interfaces.toml` correspondent aux composants choisis (taille réelle, d'après la datasheet si possible).
   - Courant total vs capacité de l'alim (≤ 80 %), recalculé par toi.
   - `puissance_dissipee_w` cohérente avec les calculs ; aération présente si > ~1 W dans un boîtier fermé.
   - Visserie de la BOM compatible avec `diametre_trou_vis`.
   - Total BOM ≤ budget.
4. Cherche ce qui manque : protection inversion de polarité, fusible, accès aux boutons / ports USB de programmation, passage des câbles, montage possible dans l'ordre.

## Sortie

Ajoute **en haut** de `projet/revue.md` :

```markdown
## Itération N — AAAA-MM-JJ — Verdict : OK | A_CORRIGER

### Critères de la spec
- [OK] ...
- [KO] ... → correction attendue : ... (agent : electronicien | concepteur-3d | sourceur)

### Incohérences et oublis
- ...

### Points non vérifiables
- ...
```

Sois précis : chaque KO dit **quoi corriger** et **à quel agent**. Ne modifie aucun autre fichier.
