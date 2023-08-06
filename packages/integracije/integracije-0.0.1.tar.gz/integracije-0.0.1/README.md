# Integracije

This package uses the graph drawing software Graphviz and engine dot to construct a graph showing
the interfaces between aplications and their components in a system as well as 
any additional information about them or the interfaces that connect them.
It reads the data from an Excel file, which should include two sheets, 
'Seznam sistemov', containing information about aplications and their components, and
'Tabela integracij', containing information about interfaces, that connect the aplications.

Paket integracije s pomočjo programske opreme Graphviz in algoritma dot izriše graf aplikacij in
njihovih komponent, ki jih povezujejo vmesniki. Informacije pridobi iz Excel datoteke z dvema listoma.
Prvi list, imenovan 'Seznam sistemov', vsebuje seznam aplikacij in komponent aplikacij ter njihove lastnosti.
Drugi list, 'Tabela integracij', vsebuje seznam vmesnikov in dodatne informacije o njih.

## Namestitev

pip install integracije

import integracije

## Primer Excel datoteke

Podatki naj bodo zapisani v .xlsx datoteki z dvema listoma, Seznam sistemov in Tabela integracij. V Seznam sistemov so podatki o aplikacijah in njihovih komponentah, v Tabela integracij pa podatki o vmesnikih.

V prvi vrstici obeh listov naj bodo navedena imena stolpcev. Med temi morajo v Seznam sistemov biti stolpec imen aplikacij in stolpec imen komponent aplikacij. V eni vrstici naj bo navedena samo ena aplikacija oz. komponenta. Komponente aplikacije z imenom X naj bodo zapisane v obliki X.ime_komponente. Tabela integracij naj ima v vrsticah navedene povezave med pari aplikacij oz. vmesnikov. Eden od stolpcev naj vsebuje izvore podatkov, drugi ponore in tretji smer toka podatkov. Oba lista lahko vsebujeta več stolpcev za dodatne podatke.

## Primer uporabe

Graf se izriše s funkcijo integracije, ki ima naslednje parametre:

1. podatki - pot do excel datoteke
2. excel_Aplikacije_stolpca - imeni stolpcev za aplikacije in komponente v obliki string ter ločeni z vejico, privzeti imeni sta 'Aplikacija/sistem' in 'Komponenta'
3. dodatno_Aplikacije - imena stolpcev z dodatnimi informacijami o aplikacijah v obliki string ter ločena z vejico, privzeta vrednost je ""
4. excel_Vmesniki_stolpci - imena stolpcev za izvore, ponore in smeri v obliki string ter ločeni z vejico, privzeta vrednost je "Izvor, Ponor, Smer"
5. dodatno_Vmesniki - imena stolpcev z dodatnimi informacijami o vmesnikih v obliki string ter ločena z vejico, privzeta vrednost je ""
6. output_format - format končne datoteke, ki ga [podpira Graphviz](https://graphviz.org/docs/outputs/), privzeto je "jpg"
7. file_name - ime končne datoteke, privzeto je "Integracije"
8. zdruzi_povezave - True, če naj bodo povezave z istimi krajišči v grafu združene, False sicer, privzeto je False

Primer uporabe:

``
import integracije

intgracije.integracije(r'`pot do .xlsx datoteke`', 'Aplikacija, Komponenta', \
    'Lastnik', 'Izvor, Ponor, Smer', 'Podatki', 'png', file_name="Primer") 
``
