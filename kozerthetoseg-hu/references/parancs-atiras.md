# Parancs: `atiras`

Közérthetőre írja át a szöveget, majd hűségellenőrzést végez: megnézi, hogy minden tény, szám, határidő, feltétel, kivétel és jogi kifejezés megmaradt-e.

## Mikor kell

Ha a hívó átírást, egyszerűsítést, közérthetőbb változatot kér egy magyar szövegből. Ha csak véleményt kér, az `audit` fut.

Kötelező szöveget (jogszabály, előírt formula, jogszabályban megállapított feltétel, kamarai egységes szöveg) a parancs nem ír át: kimondja, hogy kötelező, és hogy a forrásával kell egyeznie. A köré írt tájékoztatót átírhatja, vagy rövid magyarázatot írhat mellé.

## Bemenet

- Az átírandó szöveg.
- Olvasó és cél; ha hiányzik, egy kérdésben kérdezz rá.
- Elhagyható: megszólítás (alapértelmezés a magázás, ha a szöveg nem dönt), terjedelmi korlát, kötelezően megtartandó elemek listája.

## Lépések

1. Végezd el az audit 1–4. lépését (olvasó és cél, szövegtípus, KÉK-határ, a négy kérdés). Kötelező szövegnél itt állj meg, és csak a jelzést add.
2. Leltár az átírás előtt: gyűjtsd ki a szövegből az összes tényt, számot, összeget, dátumot és határidőt, feltételt, kivételt, jogkövetkezményt, jogszabályhelyet és jogi kifejezést. Ez a hűségellenőrzés alapja.
3. Átírás a [szabalyok.md](szabalyok.md) szerint, ebben a sorrendben: tartalom és felépítés (fő üzenet, teendő, sorrend, alcímek), mondatok, szavak és szerkezetek, végül forma. Jogi szövegnél a [szovegtipusok.md](szovegtipusok.md#szocsere) szerint a szerkezeti átírás az elsődleges; jogi kifejezést csak magyarázattal együtt cserélj, ha egyáltalán.
4. Mérés az átírt szövegen (`scripts/meres.py`), összevetve az eredetivel.
5. Hűségellenőrzés: menj végig a 2. lépés leltárán, és jelöld minden elemnél, hogy megvan-e változatlanul, átfogalmazva (azonos tartalommal), megváltozott-e, vagy kimaradt. Ami megváltozott vagy kimaradt, külön listában szerepeljen, indoklással.
6. Jogi szövegnél: zárómondat a [jogi.md](jogi.md) szerint.

## Kimenet formája

<a id="kimenet"></a>

A kimenet négy része, ebben a sorrendben:

1. Az átírt szöveg.
2. A fő változtatások listája, a szabályazonosítókkal (például „K043: a „megküldésre kerül” helyett cselekvő ige”). Ahogy a NAV a mintái bemutatásánál is teszi: az eredeti és az átírt elem mellett álljon, mit és miért változtattál.
3. Hűségtáblázat:

   | Elem | Eredetiben | Átírtban | Állapot |
   |---|---|---|---|
   | határidő | „a kézhezvételtől számított 15 napon belül” | „a levél kézhezvételétől számított 15 napon belül” | megvan |

   Az állapot lehet: megvan, átfogalmazva, megváltozott, kimaradt. A megváltozott és kimaradt elemeket a táblázat alatt külön is sorold fel, indoklással.
4. Mérés előtte–utána, és jogi szövegnél a zárómondat.

## Mit nem csinál

- Nem ír át kötelező szöveget.
- Nem told hozzá új tényt, számot vagy feltételt. Ha az olvasónak szüksége volna egy hiányzó adatra (például a határidőre), jelöld helyőrzővel („[határidő: kérdezd meg a kiadótól]”), ne találd ki.
- Nem dönti el, hogy a jogi tartalom helyes-e; a hűségellenőrzés csak azt mutatja meg, hogy az átírás megtartotta-e.
- Nem készít könnyen érthető (KÉK) változatot.

## Példa

Bemenet: „Tájékoztatjuk, hogy a 2026. évi gépjárműadó befizetésére a határozat kézhezvételétől számított 15 napon belül kerül sor; amennyiben a befizetés elmarad, késedelmi pótlék kerül felszámításra.”

Átírt szöveg: „Fizesse be a 2026-os gépjárműadót a határozat kézhezvételétől számított 15 napon belül. Ha nem fizet határidőre, késedelmi pótlékot számítunk fel.”

Hűség: adónem és év megvan; határidő (15 nap a kézhezvételtől) megvan; jogkövetkezmény (késedelmi pótlék) megvan. Megváltozott vagy kimaradt elem nincs.
