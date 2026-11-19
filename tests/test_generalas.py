import generalas
from conftest import futtat


def test_ketszer_futtatva_ugyanazt_adja(skill, capsys):
    kod, ki, _ = futtat(generalas, ["--gyoker", str(skill)], capsys)
    assert kod == 0
    elotte = {p.name: p.read_text(encoding="utf-8") for p in (skill / "references").glob("*.md")}
    kod, ki, _ = futtat(generalas, ["--gyoker", str(skill)], capsys)
    assert kod == 0 and "nincs változás" in ki
    utana = {p.name: p.read_text(encoding="utf-8") for p in (skill / "references").glob("*.md")}
    assert elotte == utana


def test_ellenoriz_jelzi_az_elavult_fajlt(skill, capsys):
    (skill / "references" / "szabalyok.md").write_text("régi", encoding="utf-8")
    kod, _, hiba = futtat(generalas, ["--gyoker", str(skill), "--ellenoriz"], capsys)
    assert kod == 1 and "elavult" in hiba
    assert (skill / "references" / "szabalyok.md").read_text(encoding="utf-8") == "régi"
