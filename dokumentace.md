# Dělení geografických dat pomocí quadtree

## Úvod
Cílem bylo napsat program, který bude vstupní bodová data ve formátu GeoJason dělit rekurzivně na 4 stejné
čtverce tak, aby v každé skupině bylo méně než 50 bodů. Vstupem je validní soubor ve formátu GeoJason,
výstupem opět GeoJason, který má v properties (atributech) zapsáno unikátní cluster_id pro každou skupinu dat.
Data je možno vizualizovat např. v QGISu. Program byl testován pro zpracování řádově statisíců dat.
Program se skládá ze skriptů „split.py,“ „quadtree.py“ a „quadtree_drawing.py.“ Spouští se ze „split.py.“ Po spuštění jsou
vykresleny vstupní body a následuje kreslení quadtree pomocí želví grafiky. Toto kreslení je však poměrně pomalé a
proto se nedoporučuje zpracovávat velká data. Případně je nutné vypnout želví kreslení přímo v kódu programu.
Program byl vypracován jakožto úkol pro předmět Základy programování, podrobné zadání je dostupné na adrese:
https://bit.ly/2Z934hy
### Vstup
Program je neinteraktivní. Uživatel musí nakopírovat svůj vstupní soubor pojmenovaný input.geojason
 do stejného adresáře, ve kterém jsou i skripty. Případně je nutné upravit název a cestu k souboru přímo
ve zdrojovém kódu programu. Program umí zpracovat pouze validní GeoJason soubor obsahující bodová data. 
Soubor může obsahovat řádově statisíce dat, nicméně v takovém případě program běží několik minut.
Například 16,5 tis. bodů zvládne zpracovat cca za 20 sekund (bez želví grafiky).
### Běh programu
#### Zpracování dat pomocí Quadtree
Pokud mají vstupní data 0 nebo 1 prvek, je uživateli pouze vypsána hláška, že použil příliš malá data.
Při takto malém souboru je v podstatě nesmyslné zjišťovat jakýkoli ohraničující čtverec apod. Při alespoň
2 prvcích program zjistí rozsah dat podle nejmenší a největší X a Y souřadnice. Z těchto bodů následně sestaví
ohraničující obdélník, v málo pravděpodobném případě čtverec. Pokud je v obdélníku více než 50 bodů,
je rozdělen na poloviny v půlce obou stran. Vzniknou tak 4 nové čtverce, ve kterých je opakovaně
(rekurzivně) uplatňován tentýž postup dokud čtverec neobsahuje méně než 50 bodů. V takovém případě 
je každému bodu v daném čtverci přiřazeno unikátní cluster_id do properties. V průběhu chodu programu
jsou vypisovány informační údaje pro uživatele a vývojáře programu. Jedná se zejména o číselné cluster_id,
které je v daném momentu zrovna přiřazované bodu, dále je také vypisován průběh hledání
geometrického středu v daném čtverci (seznamu) a informace týkající se želví grafiky.
V případě, že je některý ze čtverců (seznamů) prázdný vypisuje program „empty list.“
#### Želví grafika
Na začátku jsou vykresleny všechny vstupní body, ačkoliv má želva nastavenou nejvyšší rychlost, stále
je vykreslování poměrně pomalé. Následuje kreslení obdélníků / čtverců podle toho, kde zrovna probíhá dělení
pomocí algoritmu quadtree. Z důvodu malé rychlosti vykreslování se nedoporučuje zpracovávat řádově více než
stovky bodů při zapnuté želví grafice.
### Výstup
Výstupem je output.geojson uložený ve stejném adresáři v jakém jsou uloženy skripty. Obsahuje všechny
vstupní body s přiřazeným unikátním číselným cluster_id pro každou skupinu dat. 
## Funkcionalita programu
### Základní funkčnost
Program se skládá ze 2 skriptů „split.py“ a „quadtree.py“ (v základní verzi).
#### split.py
Nejprve je zde načten vstup, následně jsou překopírovány veškeré features do nového seznamu  „feat.“
Poté je zkontrolováno, zda vstupní seznam má alespoň 2 prvky. Seznam „counter_list“ obsahuje jediný prvek, což je 0, zároveň
 má index 0 (Tento seznam slouží k vytváření  cluster_id, při každém
splnění konečné podmínky rekurze je číslo v seznamu zvětšeno o jedničku a následně je přiřazeno všem prvkům 
ve čtverci.). Následně jsou zjištěny ohraničující body, které jsou potřebné na začátku při prvním volání funkce quadtree
a pro želví grafiku.
 Poté je již jen vytvořen validní GeoJason, který je uložen do výstupu output.geojson. 
#### quadtree.py
Quadtree je samostatný modul obsahující funkce potřebné pro samotné rekurzivní dělení. Podstatná je funkce
two_halves, která hledá geometrický střed setřízeného seznamu. Toto hledání je prováděno na principu binárního
 vyhledávání. Postupně jsou přenastavovány meze (left a right) a v každém kroku je vyloučena 
polovina seznamu. Funkce vrací index prvního prvku (bod nejblíže středu) z pravé (větší) poloviny seznamu.
Dále je zde samotná funkce quadtree. Pokud je v seznamu méně než 50 prvků, funkce zvětšuje číslo v 
seznamu cluster_counter o jedničku a toto číslo přiřazuje všem prvkům v seznamu. Dále je nakreslen
 obdélník (bounding box) pomocí želví grafiky. Toto je konečná podmínka
rekurze. V případě, že je v seznamu více než 50 prvků, jsou spočteny středy obdélníku ve směru X i Y. Nejprve je
seznam rozdělen ve směru osy X s pomocí funkce two_halves. Obě poloviny jsou načteny do nových seznamů 
přičemž ty jsou následně opět rozděleny tentokrát ve směru osy Y. Tímto postupěm vzniknou 4 nové seznamy
obsahující prvky ze 4 částí čtverce. Na tyto 4 seznamy je opět uplatněno rekurzivní dělení funkcí quadtree.
### Želví grafika
Program též obsahuje modul quadtree_drawing, díky kterému je možno vykreslovat průběh algoritmu.
#### quadtree_drawing.py
Nejprve je z modulu split.py volána funkce draw_points, které jsou předány souřadnice bounding boxu a seznam bodů.
Zároveň je funkce přiřazena do proměnné config_tuple, což bude vysvětleno záhy. Ve funkci je nejprve nastavena velikost
okna na 85 % velikosti monitoru, dále je zjištěna velikost obrazovky, která se hodí ve funkci setworldcoordinates.
Touto funkcí je definován souřadnicový systém v okně želví grafiky. Je zde tedy nastaven počátek na levý dolní roh
a maximální hodnota x a y na pravý horní roh. Zároveň jsou zde koeficienty -0,2 a 1,02, díky kterým nebudou kreslené obrazce v samém
kraji okna, což by způsobovalo zakrývání těchto tvarů a obrazců. Proto, aby data vyplňovala co možná nejvěší prostor
okna a zároveň byla vykreslena kompletně jsou dále zkoumány poměry stran obrazovky a také poměry stran dat. Pokud jsou
data „širší,“ než obrazovka, je uloženo do proměnné multiplier landscape, pokud jsou naopak „užší,“ proměnná multiplier
je rovna portrait. Jelikož je poměrně mnoho údajů potřeba v dalších funkcí želví grafiky, jsou tyto hodnoty uloženy
do entice configuration_tuple (tato entice ja také zároveň vracena funkcí draw_points). Následuje for cyklus, jenž projde
celý seznam, získá a následně přepočítá souřadnice bodů a tyto body vykreslí s pomocí funkce draw_1_point.
S přepočtem souřadnic je to mírně komplikovanější. Ve funkcích extract_x a extract_y jsou získány souřadnice
ze slovníku a tyto souřadnice jsou upraveny ve funkci modify_coor. Funkce modify_coor relativizuje souřadnice
vzhledem k nejmenší souřadnici (x nebo y), proto aby se počítalo s menšími hodnotami a také proto aby byl bod
s nejmenší x i y souřadnicí vykreslen v levém dolním rohu (zde je počátek souř. sys. tak ja bylo nastaveno ve funkci setworldcoordinates).
Dále jsou též souřadnice násobeny 10 000 000. Bylo totiž zjištěno, že želva pracuje pouze s 2 desetinnými místy.
Např. při zadání goto(14.46597945, 50.65468762), želva při dotazu na pozici vypisuje pouze (14.47,50.65) s pomocí funkce position. Je tedy lepší
nespoléhat na desetinná místa. Následně jsou souřadnice opět přepočítány ve funkci ratio_multiplier tak, aby bod s maximální
x i y souřadnicí byl vykreslen do horního pravého rohu a naopak bod snejnižšími hodnotami souřadnic do levého spodního (počátek
souřadnicového systému). Souřadnice jsou v podstatě převedeny do pixelového souřadnicového systému.
Toto se děje s ohledem na „orientaci“ dat (data orientation landscape nebo portrait). Poslední funkcí v modulu je draw_b_box.
Tato funkce je volána při rekurzivním dělení bodů do čtverců a zajišťuje kreslení ohraničujícího čtverce. Souřadnice jsou opět nejprve
přepočítávány stejným postupem jako ve funkci draw_points.

### Nekorektní vstupy
V programu nejsou ošetřeny žádné speciální případy pro nekorektní vstupy. Vstupem musí být validní GeoJson
soubor pojmenovaný input.geojson. V případě, že již ve stupním souboru je méně než 50 bodů, program všem 
přiřadí cluster_id = 1. Pokud je vstupní soubor dokonce prázdný či obsahuje 1 prvek, program pouze vypíše
hlášku o nedostatečném množství bodů.

