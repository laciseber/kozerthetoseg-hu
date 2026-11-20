# Változásnapló

Minden lényeges változás ebben a fájlban szerepel. A formátum a
[Keep a Changelog](https://keepachangelog.com/hu/1.1.0/) ajánlását követi,
a verziózás a [Szemantikus verziókezelést](https://semver.org/lang/hu/).

Verzióemelés: új forrás vagy új szabály: minor; megfogalmazás-javítás:
patch; szabály visszavonása vagy parancs átnevezése: major.

## [Kiadatlan]

## [1.2.0] - 2026-11-20

### Hozzáadva

- Tömör szabályindex (`references/szabaly-index.md`, kb. 10 KB) és csoportonkénti részletfájlok (`references/szabalyok-<csoport>.md`). A skill ezeket tölti be a 96 KB-os teljes katalógus helyett.
- Generált ellenőrző lista (`references/ellenorzo-lista.md`): minden szabály új `kerdes` mezőt kapott, egy eldöntendő kérdést. Az `atiras` utolsó lépése ezzel ellenőriz.
- Modalitás a hűségellenőrzésben: az `atiras` leltára a „kell”, „köteles”, „jogosult”, „-hat/-het”, „tilos” és hasonló elemeket is gyűjti. A 2. eval ezt ellenőrzi.
- Fejlesztési terv: ROADMAP.md.

- SECURITY.md és issue-sablon-beállítás (config.yml).
- Külön licencfájl a két licenc teljes szövegével (LICENSE-MIT, LICENSE-CC-BY-4.0); a LICENSE áttekintést ad.
- Jelvények a README elején.

### Javítva

- Az issue-sablonok a repó meglévő címkéit használják.
- README: a skill saját `audit` és `atiras` parancsával átnézve. Új rész arról, mi az a skill és hogyan kezdd; lépésenkénti telepítés; kérdés formájú alcímek; az elsődleges források helyes száma (öt).
- A referenciákban „jogszabály által” helyett „jogszabályban” (K042).
- README: új rész a tudásbázis 17 forrásáról, forrásonként a hivatkozással, a felhasználás céljával, a tételszámmal és az elérhetőséggel. Egy teszt ellenőrzi, hogy minden forrás szerepel benne.
- A NAV két kötetének forrásrekordja megkapta a kiadó nyilvános oldalát.

## [1.1.0] - 2026-11-20

### Hozzáadva

- Új forrás: Világos Beszéd: Hogyan írjunk közérthetően? Kézikönyv (Budapest Főváros Főpolgármesteri Hivatal, 2025), a kisokos bővített változata. 13 fejezet, 125 leltártétel; a tételek meglévő szabályokba olvadtak, új szabály nem kellett.
- Eltérésbejegyzés a K020 (mondathossz) és a K023 (tagmondatok száma) szabályban: a kézikönyv mondathossz-küszöbe szigorúbb, a tagmondatszáma engedékenyebb.

### Javítva

- A forrássablon és a `forras-felvetel` leírása egyértelműen mondja meg, mit kell írni a licencmezőbe, ha a forrás nem nevez meg licencet.

## [1.0.0] - 2026-11-20

### Hozzáadva

- A skill első kiadása hat paranccsal: `audit`, `atiras`, `meres`, `proba`, `forras-felvetel`, `ellenorzes`.
- Szabálykatalógus 83 szabállyal (K001–K083), 11 csoportban, saját példákkal.
- Forráskatalógus 16 forrással és 342 leltártétellel; a négy elsődleges dokumentum (Világos Beszéd kisokos, NAV: Az érthető hivatal 1–2., Európai Bizottság: A pontos fogalmazás művészete) teljes leltára.
- Jogi modul (Jszr., Jat., Air., Ptk. 6:102–6:103., GDPR 12. cikk, WP260, EUB C-26/13).
- Szövegtípus-döntés (Balogh, Bennion, NAV) és KÉK-határ.
- Szkriptek: `meres.py`, `ellenorzes.py`, `generalas.py`, `uj_forras.py`, `uj_szabaly.py`; pytest-tesztek; CI.

[Kiadatlan]: https://github.com/zoltankis-arch/kozerthetoseg-hu/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/zoltankis-arch/kozerthetoseg-hu/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/zoltankis-arch/kozerthetoseg-hu/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/zoltankis-arch/kozerthetoseg-hu/releases/tag/v1.0.0
