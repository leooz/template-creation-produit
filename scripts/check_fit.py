"""Vérifie que l'électronique rentre dans le boîtier.

- Si exports/pcb.step existe (export KiCad), il est utilisé, sinon exports/enveloppe_pcb.step.
- Contrôle les collisions PCB <-> boîtier et PCB <-> couvercle.
- Contrôle quelques règles simples tirées de interfaces.toml.

Code de sortie : 0 si tout est OK, 1 sinon.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "cad"))

from build123d import Pos, import_step  # noqa: E402

from boitier import EXPORTS, charger, geometrie  # noqa: E402

SEUIL_MM3 = 0.01
erreurs = []


def ok(msg):
    print(f"OK      {msg}")


def ko(msg):
    print(f"ERREUR  {msg}")
    erreurs.append(msg)


def regles(p):
    pcb, b = p["pcb"], p["boitier"]
    L, W = pcb["longueur"], pcb["largeur"]
    for t in pcb["trous"]:
        r = b["diametre_entretoise"] / 2
        if not (r <= t["x"] <= L - r and r <= t["y"] <= W - r):
            ko(f"trou ({t['x']}, {t['y']}) : l'entretoise dépasse du PCB")
        if t["diametre"] <= b["diametre_trou_vis"]:
            ko(f"trou ({t['x']}, {t['y']}) : diamètre PCB {t['diametre']} <= trou de vis {b['diametre_trou_vis']}")
    if b["hauteur_entretoises"] < pcb["hauteur_composants_dessous"] + 0.5:
        ko("entretoises trop basses pour les composants sous le PCB (marge < 0,5 mm)")
    for c in p.get("connecteurs", []):
        limite = W if c["face"] in ("x-", "x+") else L
        if not (c["largeur"] / 2 <= c["position"] <= limite - c["largeur"] / 2):
            ko(f"connecteur {c['nom']} : ouverture hors de la face")
    if not erreurs:
        ok("règles d'interfaces.toml")


def collisions(p):
    g = geometrie(p)
    pcb_step = EXPORTS / "pcb.step"
    if pcb_step.exists():
        # Hypothèse : export KiCad avec origine au coin bas-gauche du PCB (voir skill conception-3d).
        pcb = Pos(0, 0, g["z_pcb"]) * import_step(str(pcb_step))
        source = "pcb.step (KiCad)"
    else:
        pcb = g["enveloppe_pcb"]
        source = "enveloppe calculée (pas encore de pcb.step)"
    print(f"INFO    PCB testé : {source}")
    for nom in ("boitier", "couvercle"):
        inter = pcb & g[nom]
        vol = inter.volume if inter is not None else 0.0
        if vol > SEUIL_MM3:
            ko(f"collision PCB <-> {nom} : {vol:.2f} mm³")
        else:
            ok(f"pas de collision PCB <-> {nom}")


if __name__ == "__main__":
    params = charger()
    regles(params)
    collisions(params)
    sys.exit(1 if erreurs else 0)
