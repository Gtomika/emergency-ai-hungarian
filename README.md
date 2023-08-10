# Segélyhívó AI asszisztens

Ez a program egy demó, ami egy segélyhívó telefonközpontos AI 
lehetséges működését mutatja be.

1. A felvétel átiratának elkészítése (OpenAI speech).
2. Adatok kinyerése a felvételből (ChatGPT).
3. Megfelelő válasz generálása a hívónak.
4. A válasz felolvasása.

A ChatGPT system prompt megtekinthető a `chatgpt.py` fájlban.

A kinyert adatok (vészhelyzet típusa, esemény helye) alapján más 
programok további lépéseket tehetnek.

Itt csak egy hívás-válasz pár van implementálva, de kis módosításokkal a 
program képes beszélgetni is a hívóval: például pontosítást kér a címről, 
ami alapján megismétli az adatok kinyerését.

# Példák

Figyelem, a ChatGPT által generált pontos válaszok mindig változnak, 
ezért nem biztos hogy pontosan ezek a válaszok reprodukálhatóak. Továbbá, 
angol nyelv használatára tervezték, magyar esetén gyengébb képességeket 
mutat.

## Vészhelyzet | mentők

Átirat:
```
Jó napot! Pécsen a Búza téren egy munkás leesett az építés alatt állá ház tetejéről! Nem tud mozogogni, jöjjenek gyorsan!
```

Eredmény:
```
- Típus: EmergencyType.AMBULANCE
- Hely: Búza tér, Pécs
- Javasolt válasz: Azonnal küldünk egy mentőt a Búza térre, Pécsre. Azt mondja, hogy egy munkás leesett az építés alatt álló ház tetejéről és nem tud mozogni. Kérjük, maradjon a helyszínen és próbálja megnyugtatni az áldozatot. Segítség már úton van!
```

## Vészhelyzet | rendőrség

Átirat:
```
A kocsim ablakát betörték, és ellopták a telefonomat! Itt vagyok az autónál a Kasza utcában, Dunaújvárosban. A házszám azt hiszem 13 vagy 14.
```

Eredmény:
```
- Típus: EmergencyType.POLICE
- Hely: Kasza utca, Dunaújváros
- Javasolt válasz: Azonnal küldünk rendőrséget a helyszínre a betörés és lopás miatt. Kérjük, maradjon az autónál és várjon a rendőrök megérkezéséig. Az pontos címét is kérjük, ha nincs benne az üzenetben.
```

## Vészhelyzet | tűzoltóság

Átirat (itt a hívó nem adta meg a címet):
```
A szemközti házból füst szivárog. Most mit tegyek?
```

Eredmény:
```
- Típus: EmergencyType.FIRE_DEPARTMENT
- Hely: szemközti ház
- Javasolt válasz: Kérjük, maradjon biztonságban és távolodjon el a veszélyes területről. Mentőcsapatot fogunk küldeni azonnal a helyszínre az ön és mások védelme érdekében. Amennyiben nem említette, pontosítaná a pontos címet, hogy mielőbb odaérhessünk?
```

## Nem vészhelyzet | indokolatlan hívás

Átirat:
```
Egy mókus ugrál itt a kertemben, most mégis mit csináljak?
```

Eredmény:
```
- Típus: EmergencyType.NOT_EMERGENCY
- Hely: Nem azonosítható
- Javasolt válasz: Kedves hívó, köszönöm, hogy értesített. A mókusok gyakran előfordulnak a kertekben és általában nem jelentenek veszélyt. Ha nem okoznak kárt vagy zavart, akkor nem kell tenni semmit. Ha szeretné, hogy eltávolítsuk, kérjük, adja meg a pontos címet, hogy segíthessünk.
```

# Használt technológiák

 - OpenAI Speech to Text (beszédfelismerés)
 - OpenAI ChatGPT (3.5 modell)
 - Google Cloud Text to Speech (szöveg szintetizálás)

Ezek nem ingyenesek, de erre a demó alkalmazásra lényegében nem
generálnak költségeket.

# Futtatás

Szükséges egy Google Cloud fiók és projekt, és az ehhez hozzáférés beállítása 
a gépen. Kell egy OpenAI Platform fiók is, ahol a fizetős szolgáltatások 
be vannak kapcsolva.

# Lehetséges javítások

Érdemes kipróbálni az OpenAI által nyújtott többi modellt is, lehet, hogy 
más modellek jobb eredményeket adnak. Más szolgáltatók is kínálnak ilyen 
szolgáltást, azokat is érdemes megnézni: Google Cloud, AWS, stb.