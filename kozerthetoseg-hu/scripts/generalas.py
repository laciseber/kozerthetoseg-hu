#!/usr/bin/env python3
"""A generált referenciák előállítása a TOML-adatokból.

Három fájlt ír újra: references/szabalyok.md, references/forrasok.md és
references/lefedettseg.md. Kétszer futtatva ugyanazt adja, mert nem tesz
bele időbélyeget, és minden listát rendez.

Használat:
    python scripts/generalas.py            # a fájlok újraírása
    python scripts/generalas.py --ellenoriz # csak megnézi, frissek-e
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kozos  # noqa: E402

FEJLEC = (
    "<!-- GENERÁLT FÁJL. Ne szerkeszd kézzel: a forrása az assets/adatok/ mappa "
    "TOML-fájljai. Újragenerálás: python scripts/generalas.py -->"
)
KOR_NEV = {"altalanos": "általános", "jogi": "csak jogi szövegnél"}


def horgony(azonosito: str) -> str:
    return azonosito.lower().replace("#", "-")


def tetel_hivatkozas(adatok: kozos.Adatok, tid: str) -> str:
    fid, _, szam = tid.partition("#")
    f = adatok.forrasok.get(fid)
    if not f:
        return tid
    tetel = next((t for t in f.adat.get("tetel", []) if t.get("azonosito") == tid), None)
    oldal = f", {kozos.oldal_jel(tetel['oldal'])}" if tetel and tetel.get("oldal") else ""
    return f"[{f.adat.get('rovid', fid)}{oldal}](forrasok.md#{horgony(tid)})"


def esc(szoveg: str) -> str:
    """Táblázatcellába: a függőleges vonal és a sortörés nem törheti el a táblát."""
    return str(szoveg).replace("|", "\\|").replace("\n", " ").strip()


def szabalyok_md(a: kozos.Adatok) -> str:
    verzio = a.katalogus.adat.get("verzio", "?") if a.katalogus else "?"
    aktiv = [s for s in a.szabalyok if a.szabalyok[s].adat.get("allapot") == "aktiv"]
    vissza = [s for s in a.szabalyok if a.szabalyok[s].adat.get("allapot") == "visszavont"]
    sorrend = kozos.szabaly_sorrend(a.szabalyok)
    s = [FEJLEC, "", "# Szabálykatalógus", ""]
    s.append(f"Katalógusverzió: {verzio}. Aktív szabályok: {len(aktiv)}. Visszavont szabályok: {len(vissza)}.")
    s.append("")
    s.append(
        "Minden szabálynál: mit kér, miért segít az olvasónak, egy saját rossz és jó példa, "
        "a kivételek, és hogy melyik forrás mondja ki (oldalszámmal, a forrásleltár tételére mutatva). "
        "A „csak jogi szövegnél” jelölésű szabályokat a jogi modul alkalmazza."
    )
    s.append("")
    s.append("## Csoportok")
    s.append("")
    csoport_szab: dict[str, list[str]] = defaultdict(list)
    for sid in sorrend:
        csoport_szab[a.szabalyok[sid].adat.get("csoport", "")].append(sid)
    for c, nev in kozos.CSOPORTOK.items():
        if csoport_szab.get(c):
            ids = csoport_szab[c]
            s.append(f"- [{nev}](#{c}): {', '.join(f'[{i}](#{i.lower()})' for i in ids)}")
    s.append("")
    for c, nev in kozos.CSOPORTOK.items():
        ids = csoport_szab.get(c)
        if not ids:
            continue
        s.append(f'<a id="{c}"></a>')
        s.append("")
        s.append(f"## {nev}")
        s.append("")
        for sid in ids:
            d = a.szabalyok[sid].adat
            s.append(f'<a id="{sid.lower()}"></a>')
            s.append("")
            jel = " (visszavonva)" if d.get("allapot") == "visszavont" else ""
            s.append(f"### {sid} {d.get('cim', '')}{jel}")
            s.append("")
            if d.get("allapot") == "visszavont":
                s.append(f"Visszavonva, helyette: [{d.get('utod')}](#{str(d.get('utod', '')).lower()}). "
                         f"Ok: {d.get('visszavonas_oka', 'nincs megadva')}")
                s.append("")
            s.append(f"Szabály: {d.get('szabaly', '')}")
            s.append("")
            s.append(f"Miért segít: {d.get('miert', '')}")
            s.append("")
            p = d.get("pelda", {})
            s.append(f"- Rossz: {p.get('rossz', '')}")
            s.append(f"- Jó: {p.get('jo', '')}")
            if p.get("megjegyzes"):
                s.append(f"- Megjegyzés a példához: {p['megjegyzes']}")
            s.append("")
            if d.get("kivetelek"):
                s.append("Kivételek:")
                s.append("")
                s.extend(f"- {k}" for k in d["kivetelek"])
                s.append("")
            sor = f"Kör: {KOR_NEV.get(d.get('alkalmazasi_kor', ''), d.get('alkalmazasi_kor', ''))}."
            if d.get("meres"):
                sor += " Mérés (meres.py): " + ", ".join(d["meres"]) + "."
            s.append(sor)
            s.append("")
            forr = d.get("forrasok", [])
            if forr:
                s.append("Források: " + "; ".join(tetel_hivatkozas(a, t) for t in forr) + ".")
                s.append("")
            for e in d.get("elteres", []):
                s.append("Ha a források eltérnek: " + e.get("leiras", "") + " "
                         + "A skill döntése: " + e.get("dontes", "") + " ("
                         + "; ".join(tetel_hivatkozas(a, t) for t in e.get("forrasok", [])) + ")")
                s.append("")
    return "\n".join(s).rstrip() + "\n"


def forrasok_md(a: kozos.Adatok) -> str:
    s = [FEJLEC, "", "# Forráskatalógus és forrásleltár", ""]
    s.append(
        "A skill szabályai az alábbi forrásokra épülnek. Minden forrásnál a bibliográfiai adatok, "
        "a felhasználási feltétel, majd a leltár: a forrás minden szabálya, ajánlása, ellenőrzőlista-pontja, "
        "tilalma és példája saját szavakkal, oldalszámmal. A leltártétel vagy egy szabályra, vagy egy "
        "referenciafájl adott pontjára mutat, vagy indoklással ki van hagyva. Szövegrészt a leltár nem "
        "vesz át; a forrás eredetijét a megadott hivatkozáson lehet elolvasni."
    )
    s.append("")
    s.append("| Forrás | Prioritás | Tételek |")
    s.append("|---|---|---|")
    for fid in sorted(a.forrasok, key=lambda x: (a.forrasok[x].adat.get("prioritas", "Z"), x)):
        d = a.forrasok[fid].adat
        s.append(f"| [{esc(d.get('rovid', fid))}](#{fid}) {esc(d.get('cim', ''))} | {d.get('prioritas', '')} "
                 f"| {len(d.get('tetel', []))} |")
    s.append("")
    for fid in sorted(a.forrasok, key=lambda x: (a.forrasok[x].adat.get("prioritas", "Z"), x)):
        d = a.forrasok[fid].adat
        s.append(f'<a id="{fid}"></a>')
        s.append("")
        s.append(f"## {d.get('rovid', fid)}: {d.get('cim', '')}")
        s.append("")
        s.append(f"- Azonosító: `{fid}`")
        s.append(f"- Hivatkozás: {d.get('hivatkozas', '')}")
        if d.get("url"):
            s.append(f"- Elérhetőség: {d['url']}")
        if d.get("doi"):
            s.append(f"- DOI: {d['doi']}")
        if d.get("isbn"):
            s.append(f"- ISBN: {d['isbn']}")
        s.append(f"- Felhasználási feltétel: {d.get('licenc', '')}")
        s.append(f"- Feldolgozott kiadás: {d.get('kiadas', '')}")
        s.append(f"- Oldalszámozás a leltárban: {d.get('oldalszamozas', '')}")
        s.append(f"- Feldolgozva: {d.get('feldolgozas_datuma', '')}, "
                 f"{'teljesen' if d.get('feldolgozottsag', 'teljes') == 'teljes' else 'részlegesen'}")
        s.append(f"- Prioritás: {d.get('prioritas', '')}")
        if d.get("megjegyzes"):
            s.append(f"- Megjegyzés: {d['megjegyzes']}")
        s.append("")
        fejezetek = {f["azonosito"]: f for f in d.get("fejezet", [])}
        tetelek_fejezetenkent: dict[str, list[dict]] = defaultdict(list)
        for t in d.get("tetel", []):
            tetelek_fejezetenkent[t.get("fejezet", "")].append(t)
        for fej_id, fej in fejezetek.items():
            s.append(f"### {fej.get('cim', '')} ({kozos.oldal_jel(fej.get('oldal', ''))})")
            s.append("")
            ts = tetelek_fejezetenkent.get(fej_id, [])
            if not ts:
                s.append(f"Nincs leltártétel. Ok: {fej.get('tetel_nelkul', 'nincs megadva')}")
                s.append("")
                continue
            s.append("| Tétel | Oldal | Fajta | Tartalom | Leképezés |")
            s.append("|---|---|---|---|---|")
            for t in ts:
                tid = t.get("azonosito", "")
                fajta, cel = kozos.lekepezes(t)
                if fajta == "szabalyok":
                    lek = ", ".join(f"[{x}](szabalyok.md#{x.lower()})" for x in cel)
                elif fajta == "referencia":
                    fajl, _, anc = str(cel).partition("#")
                    lek = f"[{Path(fajl).name}#{anc}]({Path(fajl).name}#{anc})"
                elif fajta == "kihagyva":
                    lek = "kihagyva: " + esc(cel)
                else:
                    lek = "HIBÁS LEKÉPEZÉS"
                s.append(f'| <a id="{horgony(tid)}"></a>{tid.split("#")[1]} | {esc(t.get("oldal", ""))} '
                         f"| {kozos.TETEL_TIPUSOK.get(t.get('tipus', ''), t.get('tipus', ''))} "
                         f"| {esc(t.get('tartalom', ''))} | {lek} |")
            s.append("")
    return "\n".join(s).rstrip() + "\n"


def lefedettseg_md(a: kozos.Adatok) -> str:
    s = [FEJLEC, "", "# Lefedettség", ""]
    s.append(
        "Ez a fájl gépileg mutatja meg, hogy a forrásleltár minden tétele célba ért-e: szabályba, "
        "referenciafájlba, vagy indokolt kihagyásba. Az „összevont” oszlop azokat a tételeket számolja, "
        "amelyek olyan szabályra mutatnak, amelyet más forrás is kimond."
    )
    s.append("")
    szabaly_forrasai: dict[str, set[str]] = defaultdict(set)
    for fid, _, t, _ in a.tetelek():
        fajta, cel = kozos.lekepezes(t)
        if fajta == "szabalyok":
            for sid in cel:
                szabaly_forrasai[sid].add(fid)
    s.append("| Forrás | Tételek | Szabályba | ebből összevont | Referenciába | Kihagyva | Leképezetlen |")
    s.append("|---|---|---|---|---|---|---|")
    ossz = Counter()
    for fid in sorted(a.forrasok, key=lambda x: (a.forrasok[x].adat.get("prioritas", "Z"), x)):
        c = Counter()
        for t in a.forrasok[fid].adat.get("tetel", []):
            fajta, cel = kozos.lekepezes(t)
            c["tetel"] += 1
            if fajta == "szabalyok":
                c["szabaly"] += 1
                if any(len(szabaly_forrasai[x]) > 1 for x in cel):
                    c["osszevont"] += 1
            elif fajta == "referencia":
                c["referencia"] += 1
            elif fajta == "kihagyva":
                c["kihagyva"] += 1
            else:
                c["hibas"] += 1
        ossz.update(c)
        s.append(f"| [{esc(a.forrasok[fid].adat.get('rovid', fid))}](forrasok.md#{fid}) | {c['tetel']} | "
                 f"{c['szabaly']} | {c['osszevont']} | {c['referencia']} | {c['kihagyva']} | {c['hibas']} |")
    s.append(f"| Összesen | {ossz['tetel']} | {ossz['szabaly']} | {ossz['osszevont']} | "
             f"{ossz['referencia']} | {ossz['kihagyva']} | {ossz['hibas']} |")
    s.append("")
    s.append("## Fejezetek")
    s.append("")
    s.append("Minden forrás minden fejezete: hány tétel került belőle a leltárba. Ha egy sem, az ok a fejezetnél áll.")
    s.append("")
    for fid in sorted(a.forrasok, key=lambda x: (a.forrasok[x].adat.get("prioritas", "Z"), x)):
        d = a.forrasok[fid].adat
        db = Counter(t.get("fejezet") for t in d.get("tetel", []))
        s.append(f"### {d.get('rovid', fid)}")
        s.append("")
        if d.get("feldolgozottsag") == "reszleges":
            s.append("Részlegesen feldolgozott forrás: csak az alábbi fejezetek kerültek leltárba.")
            s.append("")
        for f in d.get("fejezet", []):
            n = db.get(f["azonosito"], 0)
            if n:
                s.append(f"- {f['cim']} ({kozos.oldal_jel(f['oldal'])}): {n} tétel")
            else:
                s.append(f"- {f['cim']} ({kozos.oldal_jel(f['oldal'])}): nincs tétel. {f.get('tetel_nelkul', '')}")
        s.append("")
    s.append("## Szabályok forrásai")
    s.append("")
    s.append("| Szabály | Források száma | Leltártételek | Eltérés jelölve |")
    s.append("|---|---|---|---|")
    for sid in sorted(a.szabalyok):
        d = a.szabalyok[sid].adat
        if d.get("allapot") != "aktiv":
            continue
        s.append(f"| [{sid}](szabalyok.md#{sid.lower()}) {esc(d.get('cim', ''))} | "
                 f"{len({x.split('#')[0] for x in d.get('forrasok', [])})} | {len(d.get('forrasok', []))} | "
                 f"{'igen' if d.get('elteres') else ''} |")
    s.append("")
    return "\n".join(s).rstrip() + "\n"


CELOK = {
    "szabalyok.md": szabalyok_md,
    "forrasok.md": forrasok_md,
    "lefedettseg.md": lefedettseg_md,
}


def generalt_tartalmak(adatok: kozos.Adatok) -> dict[str, str]:
    return {nev: fv(adatok) for nev, fv in CELOK.items()}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="generalas.py",
        description="A references/ generált fájljainak előállítása az assets/adatok/ TOML-fájljaiból.",
    )
    p.add_argument("--gyoker", type=Path, default=kozos.SKILL_GYOKER,
                   help="a skill mappája (alapérték: a szkript fölötti mappa)")
    p.add_argument("--ellenoriz", action="store_true",
                   help="nem ír, csak jelzi, ha egy generált fájl elavult (kilépési kód: 1)")
    a = p.parse_args(argv)
    adatok = kozos.adatok_betolt(a.gyoker)
    if adatok.olvasasi_hibak:
        for h in adatok.olvasasi_hibak:
            print(f"Hiba: {h.szoveg()}", file=sys.stderr)
        print("Hiba: az adatfájlok nem olvashatók, a generálás leállt.", file=sys.stderr)
        return 1
    tartalmak = generalt_tartalmak(adatok)
    ref = a.gyoker / "references"
    elavult = []
    for nev, tartalom in tartalmak.items():
        ut = ref / nev
        regi = ut.read_text(encoding="utf-8") if ut.exists() else None
        if regi != tartalom:
            elavult.append(nev)
            if not a.ellenoriz:
                ut.write_text(tartalom, encoding="utf-8")
    if a.ellenoriz:
        if elavult:
            for nev in elavult:
                print(f"Hiba: references/{nev} elavult; futtasd: python scripts/generalas.py", file=sys.stderr)
            return 1
        print("A generált fájlok frissek.")
        return 0
    print("Frissítve: " + (", ".join(f"references/{n}" for n in elavult) if elavult else "nincs változás"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
