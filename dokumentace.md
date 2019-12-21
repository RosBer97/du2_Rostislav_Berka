# Dělení geografických dat pomocí quadtree

## Úvod
Cílem bylo napsat program, který bude vstupní bodová data ve formátu GeoJason dělit rekurzivně na 4 stejné
čtverce tak, aby v každé skupině bylo méně než 50 bodů. Vstupem je validní soubor ve formátu GeoJason,
výstupem opět GeoJason, který má v properties (atributech) zapsáno unikátní cluster_id pro každou skupinu dat.
Data je možno vizualizovat např. v QGISu. Program byl testován pro zpracování řádově statisíců dat.
Program se skládá ze skriptů „split.py“ a „quadtree.py.“ Program se spouští ze „split.py“ Program byl
vypracován jakožto úkol pro předmět Základy programování, podrobné zadání je dostupné na adrese:
https://bit.ly/2Z934hy
### Vstup
Program je neinteraktivní. Uživatel musí nakopírovat svůj vstupní soubor pojmenovaný input.geojason
 do stejného adresáře, ve kterém jsou i skripty. Případně je nutné upravit název a cestu k souboru přímo
ve zdrojovém kódu programu. Program umí zpracovat pouze validní GeoJason soubor obsahující bodová data. 
Soubor může obsahovat řádově statisíce dat, nicméně v takovém případě program běží několik minut.
Například 16,5 tis. bodů zvládne zpracovat cca za 20 sekund.
### Běh programu
Program zjistí rozsah dat podle nejmenší a největší X a Y souřadnice. Z těchto bodů následně sestaví 
ohraničující obdélník, v málo pravděpodobném případě čtverec. Pokud je v obdélníku více než 50 bodů, 
obdélník je rozdělen na poloviny v půlce obou stran. Vzniknou tak 4 nové čtverce, ve kterých je opakovaně 
(rekurzivně) uplatňován tentýž postup dokud čtverec neobsahuje méně než 50 bodů. V takovém případě 
je každému bodu v daném čtverci přiřazeno unikátní cluster_id do properties. V průběhu chodu programu
jsou vypisovány informační údaje pro uživatele a vývojáře programu. Jedná se zejména o číselné cluster_id,
které je v daném momentu zrovna přiřazované danému bodu, dále je také vypisován průběh hledání
geometrického středu v daném čtverci (seznamu). V případě, že je některý ze čtverců (seznamů) prázdný
vypisuje program „empty list.“
### Výstup
Výstupem je output.geojson uložený ve stejném adresáři v jakém jsou uloženy oba skripty. Obsahuje všechny
vstupní body s přiřazeným unikátním číselným cluster_id pro každou skupinu dat. 
## Funkcionalita programu
### Základní funkčnost
Program se skládá ze 2 skriptů „split.py“ a „quadtree.py.“
#### split.py
Nejprve je zde načten vstup, následně jsou překopírovány veškeré features do nového seznamu  „feat.“
Seznam „counter_list“ obsahuje jediný prvek, což je 0, zároveň
 má index 0 (Tento seznam slouží k vytváření  cluster_id, při každém
splnění konečné podmínky rekurze je číslo v seznamu zvětšeno o jedničku a následně je přiřazeno všem prvkům 
ve čtverci.). Následně jsou zjištěny ohraničující body, které jsou potřebné na začátku při prvním volání funkce quadtree.
 Poté je již jen vytvořen validní GeoJason, který je uložen do výstupu output.geojson. 
#### quadtree.py
Quadtree je samostatný modul obsahující funkce potřebné pro samotné rekurzivní dělení. Podstatná je funkce
two_halves, která hledá geometrický střed setřízeného seznamu. Toto hledání je prováděno na principu binárního
 vyhledávání. Postupně jsou přenastavovány meze (left a right) a v každém kroku je vyloučena 
polovina seznamu. Funkce vrací index prvního prvku (bod nejblíže středu) z pravé (větší) poloviny seznamu.
Dále je zde samotná funkce quadtree. Pokud je v seznamu méně než 50 prvků, funkce zvětšuje číslo v 
seznamu cluster_counter o jedničku a toto číslo přiřazuje všem prvkům v seznamu. Toto je konečná podmínka
rekurze. V případě, že je v seznamu více než 50 prvků, jsou spočteny středy obdélníku ve směru X i Y. Nejprve je
seznam rozdělen ve směru osy X s pomocí funkce two_halves. Obě poloviny jsou načteny do nových seznamů 
přičemž ty jsou následně opět rozděleny tentokrát ve směru osy Y. Tímto postupěm vzniknou 4 nové seznamy
obsahující prvky ze 4 částí čtverce. Na tyto 4 seznamy je opět uplatněno rekurzivní dělení funkcí quadtree.py. 
### Nekorektní vstupy
V programu nejsou ošetřeny žádné speciální případy pro nekorektní vstupy. Vstupem musí být validní GeoJson
soubor pojmenovaný input.geojson. V případě, že již ve stupním souboru je méně než 50 bodů, program všem 
přiřadí cluster_id = 1. Pokud je vstupní soubor dokonce prázdný, vypisuje pouze  „empty list.“

