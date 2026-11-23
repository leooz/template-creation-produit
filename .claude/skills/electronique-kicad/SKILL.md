---
name: electronique-kicad
description: Conception électronique d'un produit — architecture, choix de composants, calculs (alim, courant LED, résistances, dissipation), schéma et PCB KiCad avec ERC/DRC. À utiliser pour tout choix de composant, calcul électrique, schéma ou PCB.
---

# Électronique

## Règles

- **Chaque calcul est écrit** dans `projet/decisions.md` : formule, valeurs, marge. Exemple : courant total LED, puissance alim, résistance série, puissance dissipée.
- **Marges par défaut** : alim chargée à ≤ 80 %, composants de puissance à ≤ 70 % de leur valeur max.
- **Composants** : préférer des références courantes et disponibles (LCSC, Mouser, Digikey). Une référence non vérifiée sur une datasheet est marquée `A_VERIFIER`.
- **Ne pas inventer** de brochage, de tension max ou de footprint : lire la datasheet. Si tu n'y as pas accès, dis-le.

## Workflow

1. Lis `projet/spec.md`.
2. Écris l'architecture (blocs : alim, contrôle, puissance, connecteurs) et les calculs dans `decisions.md`.
3. Liste les composants choisis dans `decisions.md` (réf fabricant + rôle) : le sourceur s'en sert.
4. **Mets à jour `projet/interfaces.toml`** : taille PCB, trous de fixation, hauteur max des composants (dessus/dessous), connecteurs qui sortent du boîtier, `puissance_dissipee_w`. Note la raison dans `decisions.md`.
5. Schéma et PCB dans `elec/` (KiCad). Si un serveur MCP KiCad est configuré, utilise-le ; sinon, propose le schéma sous forme de netlist / liste de connexions lisible et l'humain le saisit.
6. Lance `scripts/verifier.sh` : l'ERC/DRC passe par `kicad-cli` (KiCad 8+).

## Limites assumées

- **Placement et routage PCB** : l'humain (ou l'autorouteur) les fait. Toi, tu proposes un placement (connecteurs en bord, découplage près des CI, pistes de puissance larges) et tu relis.
- **Haute tension / secteur 230 V** : ne pas concevoir la partie secteur. Utiliser une alim externe certifiée et le signaler dans la spec.
