#!/usr/bin/env bash
# Lance toutes les vérifications automatiques. À exécuter avant de dire « fini ».
# Code de sortie : 0 si tout passe, 1 sinon.
set -u
cd "$(dirname "$0")/.."
mkdir -p exports
echec=0

etape() { printf '\n== %s ==\n' "$1"; }

etape "3D : génération du boîtier"
python3 cad/boitier.py || echec=1

etape "3D : encombrement PCB / boîtier"
python3 scripts/check_fit.py || echec=1

etape "Électronique : ERC / DRC KiCad"
sch=$(ls elec/*.kicad_sch 2>/dev/null | head -n1)
pcb=$(ls elec/*.kicad_pcb 2>/dev/null | head -n1)
if ! command -v kicad-cli >/dev/null 2>&1; then
  echo "IGNORÉ  kicad-cli introuvable (installer KiCad 8+ et l'ajouter au PATH)"
elif [ -z "$sch$pcb" ]; then
  echo "IGNORÉ  pas encore de projet KiCad dans elec/"
else
  if [ -n "$sch" ]; then
    kicad-cli sch erc --exit-code-violations -o exports/erc.rpt "$sch" \
      && echo "OK      ERC sans violation" \
      || { echo "ERREUR  ERC : voir exports/erc.rpt"; echec=1; }
  fi
  if [ -n "$pcb" ]; then
    kicad-cli pcb drc --exit-code-violations -o exports/drc.rpt "$pcb" \
      && echo "OK      DRC sans violation" \
      || { echo "ERREUR  DRC : voir exports/drc.rpt"; echec=1; }
  fi
fi

etape "BOM"
python3 scripts/check_bom.py || echec=1

echo
if [ "$echec" -eq 0 ]; then echo "VERDICT  tout passe"; else echo "VERDICT  des vérifications échouent"; fi
exit "$echec"
