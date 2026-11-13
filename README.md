# Frogger2090

Frogger für den Busch Microtronic 2090 mit dem [ESP2090 Studio](https://github.com/rab-berlin/ESP2090) (8x8-LED-Matrix mit Farben) und 4 Tastern: den Frosch über die Straße und den Fluss in eine der vier Buchten bringen.

- 256 Programmschritte, alle belegt
- Dateien: [frogger.mic](frogger.mic), das kommentierte Listing, und das Userscript [frogger_farben.py](frogger_farben.py) für die Farben
- Getestet im [Emulator2090](https://github.com/rab-berlin/Emulator2090), noch nicht am Gerät

![Ein Spiel im Emulator2090](bilder/spiel.gif)

## Spiel

| Reihe | | |
|---|---|---|
| 8 | Ziel | Hecke, dazwischen vier Buchten (Spalte 2, 4, 5, 7) |
| 7 | Fluss | Baumstämme (3 lang), treiben jeden Takt nach rechts |
| 6 | Fluss | Baumstämme (2 lang), treiben nach links |
| 5 | Mittelstreifen | sicher |
| 4 | Straße | Autos (magenta), fahren nach rechts |
| 3 | Straße | Lastwagen (weiß, 2 lang), fahren nach links |
| 2 | Straße | Autos (gelb), fahren nach rechts |
| 1 | Start | sicher |

- **Frosch:** grün, startet unten in Spalte 4.
- **Fluss:** Auf einem Stamm fährt der Frosch mit. Wasser ist dunkel; wer hineinspringt, ist verloren, ebenso wer auf dem Stamm über den Rand getragen wird.
- **Straße:** Ein Auto auf dem Feld des Froschs ist sein Ende. Der Verkehr stockt zufällig: Jede Fahrspur bleibt in etwa jedem vierten Takt stehen. Fährt ein Auto gerade auf den Frosch zu, entkommt er mit einem Sprung nach vorn, zurück oder zur Seite in Fahrtrichtung. Gegen die Fahrtrichtung springt er in das Auto hinein.
- **Fluss:** Auch die Stämme in Reihe 6 stocken zufällig; der Frosch darauf bleibt dann mit stehen. Wohin er oben springt, ist dadurch nicht ganz sicher, aber er kann jederzeit auf den Mittelstreifen zurück. Reihe 7 treibt gleichmäßig, damit man die Buchten anpeilen kann.
- **Ziel:** Ein Sprung in eine freie Bucht gibt einen Punkt, die Bucht leuchtet grün. Gegen die Hecke oder in eine volle Bucht ist der Frosch verloren.
- **Verloren:** Der Frosch leuchtet etwa 3 Sekunden rot, dann kommt ein neuer von unten.
- **Stufen:** Sind alle vier Buchten voll, beginnt die nächste Stufe, ein wenig schneller (bis Stufe 5).
- **Ende:** Nach 5 verlorenen Fröschen zeigt die Anzeige die Punkte (hexadezimal), und das Programm steht.

## Start

1. Matrix einschalten („LED on“ in der Weboberfläche).
2. Einmal nach dem Einschalten des ESP: das Userscript `frogger_farben.py` mit **Run** starten. Es setzt die Farben und endet sofort.
3. RESET, `HALT` `NEXT` `00` `RUN`.

Neues Spiel: RESET, RUN. Am Spielende hinterlässt das Programm saubere Farben. Kam der RESET mitten im Spiel, das Userscript noch einmal starten, sonst bleibt an der letzten Stelle des Froschs ein grünes (oder rotes) Pixel stehen. Ebenso, wenn die Farben im Script geändert wurden oder ein anderes Programm die Farben der Matrix verändert hat.

Die Matrix darf beim Start wach sein oder schlafen.

**Ohne Userscript** läuft das Programm auch: Autos, Stämme, Ufer, Hecke und volle Buchten sind dann alle rot, die Standardfarbe der Matrix. Nur den Frosch färbt das Programm selbst grün. So sieht es auch im Emulator2090 aus, der keine Userscripts kennt.

## Bedienung

| Taster | Pfeiltaste im Emulator | Wirkung |
|---|---|---|
| Eingang 1 | runter (umbelegen, siehe unten) | zurück |
| Eingang 2 | hoch | vor |
| Eingang 3 | links (umbelegen, siehe unten) | links |
| Eingang 4 | rechts | rechts |

- Ein Takt dauert etwa 1 Sekunde, mit Sprung etwa 1,3 Sekunden. Je Takt springt der Frosch höchstens einmal; Vorrang hat zurück, dann vor, links, rechts.
- Die Taster werden mehrmals je Takt abgefragt und gesammelt. Ein Druck sollte etwa eine halbe Sekunde dauern, damit er sicher ankommt. Gehalten springt der Frosch jeden Takt weiter.
- Am linken und rechten Rand geschieht nichts, ebenso bei zurück in der untersten Reihe.
- **Eingang 1** ist zugleich die Leitung, auf der die Matrix ihre Bereitschaft (REQ) meldet. Das Programm legt die Matrix deshalb nach jedem Befehl schlafen (siehe unten). Ist zurück gedrückt, wenn ein Befehl an die Matrix ansteht, wartet es, bis der Taster losgelassen ist. Solange zurück gehalten wird, steht das Spiel.
- **Emulator2090:** Taster 1 und 3 hängen dort anfangs an Pfeil links und Pfeil runter. Umbelegen: `t`, dann `1` `1` (Taster 1: Pfeil runter), `3` `3` `3` (Taster 3: Pfeil links), dann `t`.

## Farben ändern

- **Im Userscript:** die Farbnamen je Reihe in `farben`, Stamm und Hecke als Farbwerte (r, g, b) in `STAMM` und `HECKE`. Nach einer Änderung das Script noch einmal starten, dann RESET und RUN.
- **Wie das geht:** `setColors` kennt nur zehn Farbnamen. Das Script legt deshalb mit `setPalette` eigene Werte auf „orange“ (Stamm braun) und „tuerkis“ (Hecke dunkelgrün). Das gilt bis zum Neustart des ESP, auch für andere Programme.
- **Im Programm:** Frosch an Adresse 02 und 15, Befehl `14F` (Farbe 4, grün); verlorener Frosch an Adresse 6E, Befehl `11F` (Farbe 1, rot). Die Buchten sind im Userscript grün und sollten zum Frosch passen.

## Einstellen

- **Leben:** Adresse 81, Befehl `950` (`CMPI #5`): das Spiel endet beim 5. verlorenen Frosch.
- **Verkehr:** Adresse 07-0B: die Muster der Reihen 2, 3, 4, 6, 7 (`119`, `13A`, `12B`, `13C`, `170`). Jede Reihe wiederholt sich alle 4 Spalten; der Wert ist das Muster in Spalte 1-4, Bit 1 = Spalte 1. Mehr Bits = mehr Autos bzw. längere Stämme.
- **Tempo:** Adresse 2A, Befehl `15F`: Wartezeit je Takt, 6 - Stufe Runden zu 37 ms.

## Wie es gemacht ist

Der 2090 kennt keine indirekte Adressierung: Ein Programm kann nicht „das Register in Reihe y“ ansprechen. Das bestimmt fast alles an diesem Programm.

- **Eine Reihe, ein Register.** Jede Fahrspur wiederholt ihr Muster alle 4 Spalten. So reicht ein Register je Reihe, und im Bild wird es für die linke und die rechte Hälfte zweimal gesendet. Drehen nach rechts kostet nur `SHL`, `ADC`, nach links `SHR` und bei Übertrag `ADDI 8`.
- **Der Frosch steckt nicht im Bild.** Je Takt geht ein Bild im Blockmodus an die Matrix, nur mit Autos, Stämmen, Ufern und Buchten. Den Frosch dort hineinzurechnen hieße, je nach Reihe ein anderes Register zu ändern, und in seiner Reihe kämen beide Hälften aus demselben Register.
- **Grün ohne Flackern.** Steht der Frosch auf Ufer oder Stamm, ist sein Pixel im Bild ohnehin an. Das Programm färbt es vorher grün, nur in den Farben der Matrix, und das Bild zeigt beides zugleich. Nur auf der Straße ist sein Pixel dunkel; dort zeichnet es ihn gleich nach dem Bild (er flackert dabei ganz kurz).
- **Farben zurück.** Am Start legt das Programm die Farben des Userscripts auf den Stapel der Matrix. Hat sich der Frosch bewegt, holt es sie vor dem nächsten Bild zurück, damit sein altes Pixel nicht grün bleibt. Steht er still, entfällt das, und der Takt ist kürzer.
- **Treffer mit einem UND.** Der Frosch steht als Spalte (0-7) und als Bit in seiner Hälfte. Weil beide Hälften einer Reihe gleich sind, ist „Spur UND Bit“ ungleich 0 genau dann, wenn unter ihm ein Auto oder ein Stamm ist.
- **Vier Taster an vier Eingängen.** Eingang 1 ist eigentlich die REQ-Leitung der Matrix. Die Firmware des ESP2090 kann aber schlafen: Jeder Befehl weckt die Matrix mit einem gehaltenen F an den Ausgängen, sie meldet REQ, nimmt genau diesen einen Befehl und schläft danach von selbst wieder. Zwischen den Befehlen ist Eingang 1 also frei für einen Taster. Vor dem Wecken prüft das Programm, ob Eingang 1 gedrückt ist; dann wartet es, sonst hielte es den Taster für REQ.
- **Zufall fast umsonst.** `RND` schreibt immer in RD, RE und RF. Dort liegen nur Hilfsregister, deshalb kostet die Zufallszahl einen Befehl je Takt. E UND F setzt jedes Bit mit etwa 1/4; je Fahrspur entscheidet ein Bit, ob sie stehen bleibt. Die Ziffer D taugt dafür nicht: Der Zähler hinter `RND` läuft je Befehl um 3 weiter, ein Takt hat fast immer gleich viele Befehle, und D wiederholte sich alle 8 Takte.
- **Zufall nur, wo er fair ist.** Ein simulierter Spieler, der zwei Takte vorausrechnet, prüft jede Regel. Gegen die Wand lief zum Beispiel eine ältere Regel: Ein Auto, das auf den Frosch zufährt, trifft ihn vor seinem Sprung. Mit Zufall war das eine Falle; jetzt gilt sie nur noch für Sprünge gegen die Fahrtrichtung, denn nur dann tauschen Frosch und Auto die Plätze. Mit der Fahrt rücken beide eine Spalte weiter, und der Frosch bleibt vorn. So schafft der vorsichtige Spieler über 100 Buchten je verlorenem Frosch. Reihe 7 bleibt gleichmäßig, sonst wäre der Sprung in die Bucht Glückssache.

## Geschichte

*Frogger* kam 1981 von Konami in die Spielhallen, in Nordamerika vertrieben von Sega/Gremlin. Das Spielfeld dort ist genauso aufgebaut: unten eine Straße mit fünf Fahrspuren, in der Mitte ein sicherer Streifen, oben ein Fluss mit Stämmen und Schildkröten und ganz oben fünf Buchten. Auf 8x8 LEDs sind es drei Fahrspuren, zwei Fluss-Reihen und vier Buchten geworden.
