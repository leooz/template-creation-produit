---
name: retro
description: Rétrospective de fin de session ou de projet pour améliorer le système (skills, agents, AGENTS.md, scripts). À utiliser quand l'utilisateur dit "rétro", "on fait le bilan", ou à la fin d'un projet.
---

# Rétro — la boucle d'auto-amélioration

Objectif : qu'une erreur corrigée une fois ne revienne jamais.

## Méthode

1. Relis la session : `projet/revue.md` (ce que le relecteur a dû signaler), `projet/decisions.md`, et la conversation.
2. Liste, sans enjoliver :
   - ce qui a coincé ou a demandé plusieurs itérations ;
   - ce que l'humain a dû corriger ou préciser ;
   - ce qui a été deviné au lieu d'être vérifié ;
   - les checks qui auraient pu attraper un problème plus tôt.
3. Pose **une** question à l'humain : « Qu'est-ce qui t'a le plus agacé ou fait perdre du temps ? »
4. Pour chaque problème, propose **un changement concret** dans un fichier précis :
   - une règle ajoutée à un skill (`.claude/skills/*/SKILL.md`) ;
   - un critère ajouté au relecteur (`revue-produit`) ;
   - un check automatisé dans `scripts/` (le meilleur : il ne dépend plus de la mémoire de personne) ;
   - un paramètre ajouté à `interfaces.toml`.
5. Écris le tout dans `projet/retro.md`.
6. **Applique les changements seulement après validation de l'humain.**

## Remonter au template

Ce repo est une copie du template `template-creation-produit`. Une amélioration générale (pas propre à ce produit) doit aussi aller dans le template, sinon le prochain projet repartira sans elle. Indique pour chaque changement : `local` ou `template`, et rappelle à l'humain de reporter les `template` (ou propose une PR sur le repo template si tu y as accès).

## Hygiène

Un skill trop long n'est plus suivi. Si un fichier grossit, propose de fusionner ou de supprimer des règles devenues inutiles plutôt que d'empiler.
