# kozerthetoseg-hu

Ez a skill segít, hogy egy magyar szöveg olvasója megértse és használni tudja azt, amit kapott: hivatali levelet, tájékoztatót, adatkezelési tájékoztatót, ÁSZF-et, határozatot. Nyelvészeknek, jogászoknak, hivatali szövegíróknak és fejlesztőknek készült, és minden javaslata nyilvános forrásra épül, oldalszámmal.

A skill az [Agent Skills](https://agentskills.io/specification) szabványt követi, így a Claude-ban és más, ezt a szabványt ismerő eszközben is használható.

## Mit tud?

Hat parancsa van. Ha nem nevezed meg a parancsot, a kérésedből választ: ha véleményt kérsz, jelentést ad; ha átírást, átír.

| Parancs | Mit csinál |
|---|---|
| `audit` | Jelentést ad a szövegről, nem írja át. Minden észrevételnél megmondja, hol van a gond, melyik szabályt sérti, miért baj az olvasónak, hogyan lehetne jobb, és mennyire sürgős. |
| `atiras` | Átírja a szöveget, utána ellenőrzi, hogy minden tény, szám, határidő, feltétel és jogi kifejezés megmaradt-e. |
| `meres` | Lefuttatja a mérőszkriptet (mondathossz, főnevesítés, „kerül”-szerkezetek és társaik). A szám jelzés, nem ítélet. |
| `proba` | Olvasói próbatervet ír: 6–9 ember a célcsoportból elolvassa a szöveget, és saját szavaival elmondja, mit értett. |
| `forras-felvetel` | Új forrást vesz fel a skill tudásbázisába, szabványos lépésekkel. |
| `ellenorzes` | Ellenőrzi, hogy a tudásbázis teljes és ellentmondásmentes. |

### Példák

`audit`. Bemenet: „A kérelem elbírálásra került, a határozat postai úton megküldésre kerül.” Kimenet (részlet):

| Hol | Szabály | Mi a baj az olvasónak | Javaslat | Prioritás |
|---|---|---|---|---|
| „elbírálásra került” | K043 | Nem derül ki, ki döntött, és mi a döntés. | „Elbíráltuk a kérelmét: …” | magas |

`atiras`. Bemenet: „…befizetésére a határozat kézhezvételétől számított 15 napon belül kerül sor…” Kimenet: „Fizesse be a határozat kézhezvételétől számított 15 napon belül.”, és egy táblázat, amely szerint a határidő változatlanul megmaradt.

`meres`. A `python kozerthetoseg-hu/scripts/meres.py kozerthetoseg-hu/evals/szovegek/03-hatosagi-level.md` parancs egy hiánypótlási felhívásra ezt adja (részlet): „A mérőszám jelzés, nem ítélet. … Leghosszabb mondat: 37 szó. 20 szó feletti mondatok: 2. „-ásra/-ésre kerül”: 5.”

`proba`. Bemenet: egy parkolási tájékoztató. Kimenet: 7 résztvevő a kerület autótartó lakói közül; megállási pontok; kérdések, például „Ha az engedélye március 3-án jár le, mikortól kérheti az újat?”

`forras-felvetel`. Bemenet: egy új útmutató. Kimenet: új forrásfájl a leltárral, a tételek meglévő vagy új szabályokba sorolva, frissített referenciák, zöld ellenőrzés és javaslat a verzióemelésre.

`ellenorzes`. `python kozerthetoseg-hu/scripts/ellenorzes.py` Kimenet: „Rendben: 17 forrás, 467 leltártétel, 83 aktív és 0 visszavont szabály.”

## Telepítés

A skill maga a `kozerthetoseg-hu/` mappa a repóban.

- Claude Code: másold a mappát a `~/.claude/skills/` (személyes) vagy a projekt `.claude/skills/` mappájába, például: `git clone https://github.com/zoltankis-arch/kozerthetoseg-hu && cp -r kozerthetoseg-hu/kozerthetoseg-hu ~/.claude/skills/`.
- claude.ai: tömörítsd a `kozerthetoseg-hu/` mappát ZIP-be, és töltsd fel a claude.ai beállításaiban, a skillek között.
- Más eszköz, amely az Agent Skills szabványt követi: az eszköz leírása szerint add hozzá a mappát; a skill nem függ a Claude-tól.

A szkriptekhez Python 3.11 vagy újabb kell. Külső csomag és hálózat nem kell. A HuSpaCy opcionális: ha telepítve van, a `meres.py --huspacy` a függőségi mélységet és a beágyazott tagmondatokat is méri.

## Módszertan és források

A skill tudásbázisa négy elsődleges dokumentumra épül, amelyeket fejezetről fejezetre leltároztunk:

- Világos Beszéd: Hogyan írjunk közérthetően? Kisokos (Budapest Főváros Főpolgármesteri Hivatal, 2025), az 1.1.0 óta a bővített kézikönyvvel együtt;
- NAV: Az érthető hivatal 1. és 2. (2024);
- Európai Bizottság: A pontos fogalmazás művészete (2013).

Ezeket egészítik ki:

- Horváth Péter (2021), Balogh Dorka (2023), Gerencsér Balázs Szabolcs (2023) és Üveges István (2026) tanulmánya;
- a WP260 adatvédelmi iránymutatás és az Inclusion Europe alapelvei a könnyen érthető kommunikációról;
- a jogszabályszerkesztési rendelet, a jogalkotási törvény, az adóigazgatási rendtartás, a Ptk. és a GDPR vonatkozó szakaszai;
- az Európai Bíróság C-26/13. számú ítélete.

A források minden szabálya, ajánlása és példája egy-egy leltártétel, saját szavakkal, oldalszámmal. Minden tétel vagy egy szabályra mutat, vagy egy referenciafájl adott pontjára, vagy indoklással ki van hagyva. Ha két forrás ellentmond egymásnak (például a mondathossz küszöbén), a szabály kimondja, melyiket követi a skill és miért. A teljes katalógus: [forrasok.md](kozerthetoseg-hu/references/forrasok.md), a szabályok: [szabalyok.md](kozerthetoseg-hu/references/szabalyok.md), a lefedettség: [lefedettseg.md](kozerthetoseg-hu/references/lefedettseg.md).

A forrásokból a skill nem vesz át szövegrészt: a mintázatot veszi át, a példák a saját példái.

## Korlátok

- A skill nem ad jogi tanácsot. Jogi szövegnél a jogi tartalom változatlanságáért a szakember felel.
- Kötelező szöveget (jogszabály, előírt formula, kamarai egységes szöveg) nem ír át, csak jelzi, hogy kötelező.
- A mérőszám jelzés, nem ítélet. A felszíni jegyekből nem dönthető el megbízhatóan, hogy egy mondat közérthető-e: Üveges (2026) magyar hivatali korpuszán az erre épített modell F1 = 0,58-at ért el.
- A könnyen érthető kommunikáció (KÉK) más szabályrendszer. A skill felismeri, ha az olvasónak KÉK-szöveg kell, de nem készít ilyet.
- A skill nem pótolja az olvasói próbát.

## Bővítés

Új forrás felvétele öt lépés. A forrásrekordba kerülnek a bibliográfiai adatok és a felhasználási feltétel. A leltárba fejezetről fejezetre minden szabály, ajánlás, tilalom és példa, oldalszámmal, saját szavakkal. Az összevonásnál a meglévő szabályt kimondó tétel ahhoz a szabályhoz kapcsolódik, az ellentmondás külön bejegyzést kap. A leképezésnél minden tétel célt kap (szabály, referencia vagy indokolt kihagyás). A példáknál a skill a mintázatot veszi át, nem a szöveget. A szkriptek ezt adatfelvitellé teszik, az ellenőrzés gépileg mutatja meg, hogy semmi nem maradt ki. A részletek és a parancssorok: [CONTRIBUTING.md](CONTRIBUTING.md).

### Miért így épül fel?

- Az adat és a szöveg külön van. A szabályok és a források TOML-fájlokban élnek, a `references/` Markdown-fájljait szkript generálja belőlük. Egy új forrás felvétele így adatfelvitel, és a lefedettség gépileg ellenőrizhető.
- A TOML-t a Python 3.11 óta a standard könyvtár olvassa, a skill futtatásához nem kell külső csomag. A JSON Schema fájlok dokumentálják a mezőket; az ellenőrzés külső függőség nélkül validál.
- Minden adat a skill mappáján belül van, ezért a skill bárhová telepítve önálló, és a bővítés telepítés után is működik.

## Licenc és hivatkozás

A kód (szkriptek, tesztek, CI) MIT, a szöveges tartalom (szabályok, referenciák, dokumentáció) [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.hu) licenc alatt áll; részletek: [LICENSE](LICENSE). Hivatkozás: [CITATION.cff](CITATION.cff).

Szerző: Kis Zoltán ([github.com/zoltankis-arch](https://github.com/zoltankis-arch)).

## Köszönet

A skill ezekre a munkákra épül; a hibák a skill hibái. Köszönet a források szerzőinek és kiadóinak:

- a Világos Beszédnek és Budapest Főváros Főpolgármesteri Hivatalának;
- a Nemzeti Adó- és Vámhivatal Közérthetőségi Programirodájának;
- az Európai Bizottság Fordítási Főigazgatóságának;
- Horváth Péternek, Balogh Dorkának, Gerencsér Balázs Szabolcsnak és Üveges Istvánnak;
- a 29. cikk szerinti adatvédelmi munkacsoportnak és az Inclusion Europe-nak.

## In English

kozerthetoseg-hu is an [Agent Skills](https://agentskills.io/specification) skill for checking and improving the plain-language quality of Hungarian texts: official letters, notices, privacy notices, terms and conditions, administrative decisions. It offers six commands (audit, rewrite with a fidelity check, surface metrics, a reader-test plan, adding a new source, consistency check) and a separate legal module. Every rule is traced to a public source with page numbers; the catalogue is built from a full chapter-by-chapter inventory of four Hungarian and EU guides plus supporting research and legislation. The skill gives no legal advice, does not rewrite mandatory texts, treats metrics as signals rather than verdicts, and recognises but does not produce easy-to-read (KÉK) texts. Scripts need Python 3.11+ only. Code: MIT; content: CC BY 4.0.
