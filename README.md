# Template — création de produit physique

Template de repo pour concevoir un produit physique **avec des agents IA** : boîtier 3D, électronique KiCad, liste de courses. Il est vérifiable à chaque étape et s'améliore à chaque projet.

Il marche avec **Claude Code**, **GitHub Copilot (VS Code)** et **OpenCode** : les skills et les agents sont des fichiers Markdown standards.

## Démarrer un produit

1. Sur GitHub : **Use this template → Create a new repository**.
2. Clone, puis `pip install -r requirements.txt` (Python 3.11+).
3. Ouvre ton outil dans le dossier et dis : *« Nouveau produit : <ton idée> »*. Le skill `nouveau-produit` prend la main.

## Comment ça marche

```
        ┌──────────── toi (tu valides, tu tranches) ─────────────┐
        ▼                                                        │
  1. PLANIFIER ── spec.md + interfaces.toml ──► validation humaine
        │
  2. PRODUIRE (en parallèle)
        ├─ concepteur-3d ──► cad/ → exports/*.step|stl
        ├─ electronicien ──► elec/ + interfaces.toml + calculs
        └─ sourceur      ──► bom.csv
        │
  3. ÉVALUER ── scripts/verifier.sh + relecteur ──► revue.md
        │
  4. BOUCLER jusqu'à OK (3 itérations max, sinon retour à l'humain)
        │
  5. RÉTRO ──► améliore skills / checks / template
```

- **Les agents ne se parlent pas, ils partagent des fichiers.** `projet/interfaces.toml` est le contrat entre la 3D et l'électronique : c'est la seule source de vérité pour les cotes.
- **Tout est vérifiable** : `scripts/verifier.sh` génère la 3D, contrôle les collisions PCB ↔ boîtier, lance l'ERC/DRC KiCad et vérifie la BOM (champs, budget).
- **Évaluation séparée** : le `relecteur` n'a pas produit le travail, donc il ne s'auto-félicite pas.

## Structure

| Chemin | Contenu |
|---|---|
| `AGENTS.md` | Règles communes et workflow (lu par Copilot et OpenCode ; `CLAUDE.md` l'importe pour Claude Code) |
| `.claude/skills/` | Les compétences : `nouveau-produit`, `conception-3d`, `electronique-kicad`, `sourcing-bom`, `revue-produit`, `retro` |
| `.claude/agents/` | Les sous-agents (lus par Claude Code **et** VS Code Copilot) |
| `.opencode/agents/` | Les mêmes sous-agents au format OpenCode |
| `projet/` | spec, interfaces, BOM, décisions, revues, rétros |
| `cad/boitier.py` | Boîtier paramétrique build123d (fond + couvercle + entretoises + découpes + aération) |
| `scripts/` | `verifier.sh`, `check_fit.py`, `check_bom.py` |

## Prérequis

- **Python 3.11+** et `build123d` (via `requirements.txt`)
- **KiCad 8+** avec `kicad-cli` dans le PATH, pour l'ERC/DRC et l'export STEP du PCB
- Optionnel : un **serveur MCP KiCad** pour que l'agent lise et écrive le schéma ou le PCB, par exemple [mcp-server-kicad](https://pypi.org/project/mcp-server-kicad/). Exemple pour Claude Code (`.mcp.json`) :
  ```json
  { "mcpServers": { "kicad": { "command": "uvx", "args": ["--from", "mcp-server-kicad", "mcp-server-kicad"] } } }
  ```
  Pour Copilot ou OpenCode, la forme du fichier de config MCP change : voir leur doc.

## Selon l'outil

- **Claude Code** : rien à faire. Les skills et agents de `.claude/` sont chargés automatiquement.
- **VS Code + Copilot** : mode Agent. Les skills de `.claude/skills` et les agents de `.claude/agents` sont détectés. Selon ta version et les règles de ton organisation, il faudra peut-être activer les Agent Skills dans les réglages, ou ils seront bloqués.
- **OpenCode** : les skills de `.claude/skills` sont lus, les agents viennent de `.opencode/agents/`. Appelle-les avec `@relecteur`, etc.

## Ce que ça ne fait pas (volontairement)

- Le placement et le routage PCB : tu les fais toi (ou l'autorouteur). L'IA propose et relit.
- Le slicing : le STL est presque prêt, l'orientation et les réglages restent à toi.
- Les commandes : l'IA prépare la liste de courses, c'est toi qui achètes.

## Améliorer le template

À la fin de chaque projet, lance la rétro (*« on fait la rétro »*). Les améliorations marquées `template` sont à reporter ici, pour que le prochain produit démarre avec.
