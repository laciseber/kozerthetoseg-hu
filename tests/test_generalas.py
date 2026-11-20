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


def test_index_csoportfajlok_es_ellenorzo_lista(skill, capsys):
    futtat(generalas, ["--gyoker", str(skill)], capsys)
    ref = skill / "references"
    index = (ref / "szabaly-index.md").read_text(encoding="utf-8")
    lista = (ref / "ellenorzo-lista.md").read_text(encoding="utf-8")
    assert len(index.encode("utf-8")) < 15_000, "az index túl nagy a betöltéshez"
    for i in range(1, 84):
        sid = f"K{i:03d}"
        assert f"[{sid}](szabalyok-" in index
        assert f"[{sid}](szabalyok-" in lista
    assert lista.count("- [ ] ") == 83
    assert "#k043" in (ref / "szabalyok-szerkezet.md").read_text(encoding="utf-8").lower() or \
        'id="k043"' in (ref / "szabalyok-szerkezet.md").read_text(encoding="utf-8")
