# Userscript fuer Frogger (frogger.mic) auf dem ESP2090 Studio
# Setzt die Farbmatrix und endet. Einmal nach dem Einschalten des ESP starten ("Run"), die Matrix muss
# eingeschaltet sein ("LED on"). Danach RESET, RUN am 2090. Fuer weitere Spiele nicht noetig.
# Noch einmal starten: nach einer Aenderung der Farben hier, wenn ein anderes Programm die Farben
# veraendert hat, oder nach RESET mitten im Spiel (dann bleibt sonst ein gruenes oder rotes Pixel stehen).
#
# Das Programm benutzt selbst nur Farbe 4 (gruen: Frosch) und 1 (rot: verlorener Frosch).
# setColors kennt nur zehn Farbnamen. Deshalb legt das Script eigene Farbwerte (r, g, b) auf einige
# dieser Namen. Das gilt bis zum Neustart des ESP, auch fuer andere Programme.

STAMM = (6, 2, 0)       # braun, auf "orange"
HECKE = (0, 3, 0)       # dunkelgruen, auf "tuerkis"

setPalette(2, STAMM)
setPalette(5, HECKE)

U = "violett"           # Ufer: Start und Mittelstreifen
H = "tuerkis"           # Hecke zwischen den Buchten
B = "gruen"             # Bucht (leuchtet erst, wenn ein Frosch darin sitzt)
S = "orange"            # Baumstamm
A1, A2, A3 = "gelb", "weiss", "magenta"   # Autos Reihe 2, Lastwagen Reihe 3, Autos Reihe 4

farben = [
    [H,  B,  H,  B,  B,  H,  B,  H],   # Reihe 8: Ziel
    [S,  S,  S,  S,  S,  S,  S,  S],   # Reihe 7: Fluss
    [S,  S,  S,  S,  S,  S,  S,  S],   # Reihe 6: Fluss
    [U,  U,  U,  U,  U,  U,  U,  U],   # Reihe 5: Mittelstreifen
    [A3, A3, A3, A3, A3, A3, A3, A3],  # Reihe 4: Strasse
    [A2, A2, A2, A2, A2, A2, A2, A2],  # Reihe 3: Strasse
    [A1, A1, A1, A1, A1, A1, A1, A1],  # Reihe 2: Strasse
    [U,  U,  U,  U,  U,  U,  U,  U],   # Reihe 1: Start
]

setColors([c for zeile in farben for c in zeile])
log("Frogger: Farben gesetzt")
