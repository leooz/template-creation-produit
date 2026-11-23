"""Boîtier paramétrique généré depuis projet/interfaces.toml.

Aucune cote en dur ici : tout vient de interfaces.toml.
Sorties (dans exports/) :
  boitier.step / boitier.stl        — le fond avec entretoises et découpes connecteurs
  couvercle.step / couvercle.stl    — le couvercle à emboîter (positionné en place pour l'assemblage)
  enveloppe_pcb.step                — volume réservé au PCB + composants (sert au check si pas de STEP KiCad)

Usage : python cad/boitier.py
"""

import pathlib
import tomllib

from build123d import Align, Box, Cylinder, Pos, export_step, export_stl

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"
MIN = (Align.MIN, Align.MIN, Align.MIN)
CCM = (Align.CENTER, Align.CENTER, Align.MIN)


def charger():
    with open(ROOT / "projet" / "interfaces.toml", "rb") as f:
        return tomllib.load(f)


def geometrie(p):
    pcb, b = p["pcb"], p["boitier"]
    e, j = b["epaisseur_paroi"], b["jeu_interne"]
    L, W = pcb["longueur"], pcb["largeur"]

    z_pcb = e + b["hauteur_entretoises"]  # face inférieure du PCB
    z_dessus_pcb = z_pcb + pcb["epaisseur"]
    levre_h = b["hauteur_levre"]
    # hauteur intérieure : entretoises + PCB + composants + jeu + place pour la lèvre du couvercle
    h_int = b["hauteur_entretoises"] + pcb["epaisseur"] + pcb["hauteur_composants_dessus"] + j + levre_h

    # --- Fond -------------------------------------------------------------
    ext = Pos(-j - e, -j - e, 0) * Box(L + 2 * j + 2 * e, W + 2 * j + 2 * e, e + h_int, align=MIN)
    cavite = Pos(-j, -j, e) * Box(L + 2 * j, W + 2 * j, h_int + 1, align=MIN)
    boitier = ext - cavite

    for t in pcb["trous"]:
        boitier += Pos(t["x"], t["y"], e) * Cylinder(
            b["diametre_entretoise"] / 2, b["hauteur_entretoises"], align=CCM
        )
        boitier -= Pos(t["x"], t["y"], e) * Cylinder(
            b["diametre_trou_vis"] / 2, b["hauteur_entretoises"] + 0.01, align=CCM
        )

    # --- Découpes connecteurs --------------------------------------------
    for c in p.get("connecteurs", []):
        zc = z_dessus_pcb + c["z"]
        if c["face"] in ("x-", "x+"):
            x = -j - e / 2 if c["face"] == "x-" else L + j + e / 2
            boitier -= Pos(x, c["position"], zc) * Box(e + 2, c["largeur"], c["hauteur"])
        else:
            y = -j - e / 2 if c["face"] == "y-" else W + j + e / 2
            boitier -= Pos(c["position"], y, zc) * Box(c["largeur"], e + 2, c["hauteur"])

    # --- Couvercle (plaque + lèvre qui s'emboîte) -------------------------
    tol = b["tolerance_impression"]
    z_haut = e + h_int
    ec = b["epaisseur_couvercle"]
    couvercle = Pos(-j - e, -j - e, z_haut) * Box(L + 2 * j + 2 * e, W + 2 * j + 2 * e, ec, align=MIN)
    levre = Pos(-j + tol, -j + tol, z_haut - levre_h) * Box(L + 2 * j - 2 * tol, W + 2 * j - 2 * tol, levre_h, align=MIN)
    creux = Pos(-j + tol + 1.5, -j + tol + 1.5, z_haut - levre_h - 0.01) * Box(
        L + 2 * j - 2 * tol - 3, W + 2 * j - 2 * tol - 3, levre_h + 0.01, align=MIN
    )
    couvercle = couvercle + levre - creux

    if p.get("thermique", {}).get("aeration"):
        n, fente_l, fente_w = 5, L * 0.6, 2.0
        pas = W / (n + 1)
        for i in range(1, n + 1):
            couvercle -= Pos(L / 2, pas * i, z_haut + ec / 2) * Box(fente_l, fente_w, ec + 2)

    # --- Enveloppe PCB (conservatrice) ------------------------------------
    enveloppe = Pos(0, 0, z_pcb) * Box(L, W, pcb["epaisseur"] + pcb["hauteur_composants_dessus"], align=MIN)
    dessous = Pos(0, 0, z_pcb - pcb["hauteur_composants_dessous"]) * Box(L, W, pcb["hauteur_composants_dessous"], align=MIN)
    for t in pcb["trous"]:  # pas de composants sous le PCB autour des entretoises
        dessous -= Pos(t["x"], t["y"], z_pcb - pcb["hauteur_composants_dessous"] - 0.01) * Cylinder(
            b["diametre_entretoise"] / 2 + 0.5, pcb["hauteur_composants_dessous"] + 0.02, align=CCM
        )
    enveloppe += dessous

    return {"boitier": boitier, "couvercle": couvercle, "enveloppe_pcb": enveloppe, "z_pcb": z_pcb}


def main():
    EXPORTS.mkdir(exist_ok=True)
    g = geometrie(charger())
    for nom in ("boitier", "couvercle", "enveloppe_pcb"):
        export_step(g[nom], str(EXPORTS / f"{nom}.step"))
    for nom in ("boitier", "couvercle"):
        export_stl(g[nom], str(EXPORTS / f"{nom}.stl"))
    print(f"OK  exports générés dans {EXPORTS.relative_to(ROOT)}/ (PCB posé à z = {g['z_pcb']:.2f} mm)")


if __name__ == "__main__":
    main()
