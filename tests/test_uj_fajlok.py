"""Az uj_forras.py és az uj_szabaly.py, és egy teljes forrásfelvétel a szkriptekkel."""

import re

import ellenorzes
import generalas
import uj_forras
import uj_szabaly
from conftest import futtat


def test_uj_forras_letrehoz_es_ellenoriz(skill, capsys):
    kod, ki, _ = futtat(uj_forras, ["minta-lap-2026", "--cim", "Minta lap", "--kiado", "Minta Kiadó",
                                    "--ev", "2026", "--gyoker", str(skill), "--datum", "2026-11-19"], capsys)
    assert kod == 0 and "Létrehozva" in ki
    ut = skill / "assets" / "adatok" / "forrasok" / "minta-lap-2026.toml"
    szoveg = ut.read_text(encoding="utf-8")
    assert 'azonosito = "minta-lap-2026#001"' in szoveg
    assert "url =" not in szoveg
    kod, _, hiba = futtat(uj_forras, ["minta-lap-2026", "--gyoker", str(skill)], capsys)
    assert kod == 1 and "már létezik" in hiba
    futtat(generalas, ["--gyoker", str(skill)], capsys)
    kod, _, hiba = futtat(ellenorzes, ["--gyoker", str(skill)], capsys)
    assert kod == 1 and "KITÖLTENDŐ" in hiba


def test_uj_forras_hibas_bemenet(skill, capsys):
    assert futtat(uj_forras, ["Rossz_Azonosito", "--gyoker", str(skill)], capsys)[0] == 2
    assert futtat(uj_forras, ["jo-azonosito", "--ev", "26", "--gyoker", str(skill)], capsys)[0] == 2
    assert futtat(uj_forras, ["jo-azonosito", "--url", "ftp://x", "--gyoker", str(skill)], capsys)[0] == 2
    assert futtat(uj_forras, ["--gyoker", str(skill)], capsys)[0] == 2


def test_kovetkezo_tetel(skill, capsys):
    kod, ki, _ = futtat(uj_forras, ["--kovetkezo-tetel", "vilagos-beszed-kisokos-2025", "--gyoker", str(skill)], capsys)
    assert kod == 0 and ki.strip() == "vilagos-beszed-kisokos-2025#052"
    kod, _, hiba = futtat(uj_forras, ["--kovetkezo-tetel", "nincs", "--gyoker", str(skill)], capsys)
    assert kod == 1


def test_uj_szabaly(skill, capsys):
    kod, ki, _ = futtat(uj_szabaly, ["--kovetkezo", "--gyoker", str(skill)], capsys)
    assert ki.strip() == "K084"
    kod, ki, _ = futtat(uj_szabaly, ["--cim", "Teszt", "--csoport", "mondat", "--gyoker", str(skill)], capsys)
    assert kod == 0
    assert (skill / "assets" / "adatok" / "szabalyok" / "K084.toml").is_file()
    kod, ki, _ = futtat(uj_szabaly, ["--kovetkezo", "--gyoker", str(skill)], capsys)
    assert ki.strip() == "K085"
    assert futtat(uj_szabaly, ["--cim", "x", "--gyoker", str(skill)], capsys)[0] == 2


def test_teljes_forrasfelvetel(skill, capsys):
    """A 10. eval szkriptes része: forrás felvétele, összevonás, eltérés, zöld ellenőrzés."""
    elotte = len(list((skill / "assets" / "adatok" / "forrasok").glob("*.toml")))
    futtat(uj_forras, ["mintavaros-levelirasi-lap-2026", "--cim", "Levélírási lap",
                       "--kiado", "Mintaváros Önkormányzata", "--ev", "2026",
                       "--gyoker", str(skill), "--datum", "2026-11-19"], capsys)
    ut = skill / "assets" / "adatok" / "forrasok" / "mintavaros-levelirasi-lap-2026.toml"
    sz = ut.read_text(encoding="utf-8")
    sz = re.sub(r'rovid = ".*"', 'rovid = "Mintaváros 2026"', sz)
    sz = re.sub(r'szerzo = ".*"', 'szerzo = "Mintaváros Önkormányzata"', sz)
    sz = re.sub(r'hivatkozas = ".*"', 'hivatkozas = "Mintaváros Önkormányzata: Levélírási lap. 2026."', sz)
    sz = re.sub(r'licenc = ".*"', 'licenc = "A forrás megjelölésével szabadon terjeszthető."', sz)
    sz = re.sub(r'kiadas = ".*"', 'kiadas = "2026, egy oldal."', sz)
    sz = re.sub(r'oldalszamozas = ".*"', 'oldalszamozas = "nyomtatott oldalszám"', sz)
    sz = sz.replace('cim = "KITÖLTENDŐ"', 'cim = "Levélírás a mintavárosi hivatalban"')
    sz = sz.replace('oldal = "KITÖLTENDŐ"', 'oldal = "1"')
    sz = sz[: sz.index("[[tetel]]")]
    tetelek = [
        (1, "A levél első mondata mondja meg, miről szól.", "K002"),
        (2, "Egy mondat legfeljebb 18 szóból álljon.", "K020"),
        (3, "Az „amennyiben” helyett „ha”.", "K036"),
    ]
    for n, t, k in tetelek:
        sz += (f'[[tetel]]\nazonosito = "mintavaros-levelirasi-lap-2026#{n:03d}"\nfejezet = "f01"\n'
               f'oldal = "1"\ntipus = "szabaly"\ntartalom = "{t}"\nszabalyok = ["{k}"]\n\n')
    ut.write_text(sz, encoding="utf-8")
    sdir = skill / "assets" / "adatok" / "szabalyok"
    for n, _, k in tetelek:
        p = sdir / f"{k}.toml"
        s = p.read_text(encoding="utf-8")
        s = s.replace("forrasok = [\n", f'forrasok = [\n  "mintavaros-levelirasi-lap-2026#{n:03d}",\n', 1)
        p.write_text(s, encoding="utf-8")
    p = sdir / "K020.toml"
    p.write_text(p.read_text(encoding="utf-8") + (
        '\n[[elteres]]\nforrasok = ["mintavaros-levelirasi-lap-2026#002", "eu-pontos-fogalmazas-2013#022"]\n'
        'leiras = "A lap 18 szavas felső határt ad, az uniós útmutató átlagot."\n'
        'dontes = "A skill továbbra is az átlagot követi."\n'), encoding="utf-8")
    kod, _, _ = futtat(generalas, ["--gyoker", str(skill)], capsys)
    assert kod == 0
    kod, ki, hiba = futtat(ellenorzes, ["--gyoker", str(skill)], capsys)
    assert kod == 0, hiba
    assert f"{elotte + 1} forrás" in ki
    assert "mintavaros-levelirasi-lap-2026" in (skill / "references" / "forrasok.md").read_text(encoding="utf-8")
