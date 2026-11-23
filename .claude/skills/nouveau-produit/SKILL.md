---
name: nouveau-produit
description: Orchestre la conception d'un produit physique (3D + électronique + BOM) avec la boucle planifier → produire → évaluer. À utiliser quand l'utilisateur démarre un produit, décrit une idée d'objet à fabriquer, ou demande de faire avancer le projet.
---

# Orchestration d'un produit

Tu es l'orchestrateur. Tu ne fais pas tout toi-même : tu planifies, tu délègues aux agents spécialisés, tu fais évaluer, tu boucles.

## 1. Planifier (avec l'humain)

1. Lis `projet/spec.md`, `projet/interfaces.toml`, `projet/decisions.md`. S'ils sont déjà remplis, reprends où on en était (dernier état dans `projet/revue.md`).
2. Sinon, interviewe l'humain : usage, alimentation, dimensions max, budget, mode de fabrication. **Une question à la fois, 5 maximum.**
3. Remplis `spec.md`, y compris des **critères d'acceptation chiffrés** que le relecteur pourra vérifier.
4. Fais un premier jet de `interfaces.toml` (même approximatif : taille PCB estimée, connecteurs qui sortent du boîtier).
5. **Stop : fais valider spec + interfaces par l'humain.** Pas de production avant.

## 2. Produire (en parallèle)

Lance dans le **même tour** les sous-agents, chacun avec une consigne courte qui pointe vers les fichiers :

- `electronicien` : « Conçois l'électronique selon projet/spec.md. Mets à jour projet/interfaces.toml si les cotes changent et note pourquoi dans decisions.md. »
- `concepteur-3d` : « Génère le boîtier selon projet/interfaces.toml et projet/spec.md. »
- `sourceur` : « Remplis projet/bom.csv à partir des composants choisis (attends ou relis la liste de l'électronicien). »

Si l'électronicien change `interfaces.toml`, relance le concepteur 3D après lui (dépendance).

## 3. Évaluer

1. Lance `scripts/verifier.sh`.
2. Lance le sous-agent `relecteur` : « Évalue le projet contre projet/spec.md. Écris ton verdict dans projet/revue.md. »

## 4. Boucler

- Verdict `OK` → passe à 5.
- Verdict `A_CORRIGER` → donne chaque point au bon agent, reviens en 3.
- **Après 3 itérations sans OK** → arrête-toi et présente à l'humain ce qui bloque et les options.
- Conflit 3D ↔ électronique (place, chaleur) → ne tranche pas seul : présente les deux options à l'humain.

## 5. Clôturer

- Résume à l'humain : ce qui est prêt (STL, BOM, Gerber éventuels), ce qui reste manuel (routage, slicer, commande).
- Propose de lancer le skill `retro`.

## Interdits

- Passer une commande, payer, envoyer un PCB en fabrication : c'est l'humain qui le fait.
- Mettre une cote en dur ailleurs que dans `interfaces.toml`.
