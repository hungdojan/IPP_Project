
## Implementační dokumentace k 2. úloze do IPP 2021/2022
Jméno a příjmení: Hung Do  
Login: xdohun00  

## Interpret jazyka IPPcode22
Práce překladače je rozdělena na 3 podúkoly:
1. Zpracovávání argumentů
2. Načtení a zpracování XML zdrojového souboru
3. Vykonávání jednotlivých příkazů

## Zpracování argumentů
Argumenty se zpracovávají ve zdrojovém souboru `proj1_module/arguments.py` za pomoci standardní knihovny `argparse`.  Z nich vyčte zdrojový soubor (`--source`) a vstupní soubor (`--input`). Pokud jsou hodnoty obou možností (hodnoty parametrů) prázdné a `--help` nebyla zavolána, je program ukončen. 

## Načítání a zpracování XML zdrojového souboru
XML zdrojové soubory jsou řešeny v `proj2_module/xml_parser.py`. Nejprve se celý soubor načte pomocí `xml.etree.ElementTree.parse` funkce, aby se zjistilo, zda je soubor správně formátovaný ("well-formed"). Po zkontrolování hlavičky souboru se načítají jednotlivé elementy instrukcí a informace ukládají se do objektu třídy `Statement`. Každá instance této třídy se poté vloží do seznamu, který se pak z funkce vrací. Pokud v XML souboru nastane chyba, program se ukončí s náležitou chybovou hodnotou.

## Vykonávání jednotlivých příkazů
Celé vykonávání programu je popsána na několika řádcích v následujícím úseku kódu:
```python
lof_ins = xml_parser()		# ziska serazeny seznam prikazu
nof_ins = len(lof_ins)		# pocet prikazu
ins_index = 0				# reprezentace ukazatele na prikaz (program counter)

# vykonavani programu, dokud program counter nedojde na konec seznamu
# nebo se zavola prikaz ukonceni programu (EXIT)
while ins_index < nof_ins:
	# ziskani prikazu
	stat = lof_ins[ins_index]
	# vykonani prikazu a aktualizace hodnoty program counter
	ins_index = instruction_set[stat.ins](ins_index, stat.args)
```
Nejprve se načte seřazený seznam příkazů pro vykonání. Přes ten se pak cyklicky prochází. Pomocí `ins_index` (reprezentující program counter) se získá ze seznamu objekt instrukce. Ze slovníku instrukcí `instruction_set` program najde příslušnou funkci a volá se s argumenty získané ze zdrojového XML. Funkce nakonec vrátí novou pozici `ins_index` . Cyklus se ukončí poté, co hodnota indexu instrukce překročí velikost seznamu instrukcí (program vykonal poslední instrukci). Druhá možnost ukončení programu (vyjma chybových stavů) je instrukce `EXIT` ve zdrojovém souboru.

## Struktura programu
Jednotlivá doplňující skripta jsou uložena v modulu `proj2_module`.
- `arguments.py`
	- Soubor zpracovává vsstupní argumenty programu
- `coredata.py` 
	- Obsahuje třídu `CodeData`, která si udržuje data celého programu (např. jednotlivé rámce, odkazy na návěští, programový zásobník a odkládací zásobník pro funkce.
- `error.py` 
	- Obsahuje výčet chybových kód a implementaci chybového hlášení.
- `frame.py` 
	- Obsahuje třídu `Frame` jako reprezentace rámce a `Variable` jako reprezentace definované proměnné v rámci.
- `statement.py` 
	- Obsahuje třídu `Statement` reprezentující jednu instrukci, která se má vykonat. Instance této třídy nese jméno instrukce a jednotlivé argumenty instrukce.
- `instruction_set.py` 
	- Obsahuje instrukční sadu. Každá instrukce má svoje jméno s její implementací. V každé instrukci se provádí sémantická kontrola (např. typová kontrola, typová kompatibilita operace, existence proměnné apod.)
- `stack_instruction_set.py` 
	- Implementace zásobníkové instrukční sady.
- `statement.py`
	- Obsahuje třídu `Statement` reprezentující příkaz v jazyce  `IPPcode22` a `Argument` reprezentující argumenty příkazu.
- `xml_parser.py`
	- Stará se o načítání XML zdrojového souboru.

## Implementace testovacího skriptu
Práce testovacího skriptu je rozdělena do 4 částí:
1. Načtení argumentů a inicializace testů
2. Spuštění testů
3. Vygenerování HTML
4. Závěrečný úklid (mazání vygenerovaných testovacích souboru, pokud uživatel nevybral argument `--noclean`)

## Načítání argumentů a inicializace testů
Argumenty se zpracovávají obdobně jako v [interpretu](#zpracování-argumentů).  Provádí se při tom různé kontroly (např. kolize `--int-only` a `--parse-only`) a doplnění implicitních hodnot (např. pokud uživatel nespecifikuje cestu ke složce s `jexamxml.jar` souboru, bude nastaveno výchozí cesta `/pub/courses/ipp/jexamxml/`).
## Spuštění testů
Podle nastavených parametrů se testovací skript může spustit ve třech režimech:
- **parse only**
	- testuje se správnost parse skriptu
- **interpret only** 
	- testuje se správnost interpreta
- **parse and interpret**
	- testuje se zřetězení obou programů

Nejprve se ve zvolené složce najdou příslušné testovací soubory (`.in`, `.src`, `.out`, `.rc`), poté se spustí test nad těmito soubory a porovnávají se návratové hodnoty a obsah výstupu. Pokud všechny tyto výstupy odpovídají předpokládaným výstupům, daný test je prohlášen za úspěšný, v opačném případě daný test selhal. Výsledky testů se pak uloží do seznamu testů pro pozdější generování HTML souboru.

## Vygenerování HTML
Poté, co se získají výsledky všech testů, program zpracuje záznamy testů a vygeneruje HTML soubor. Při inicializaci si objekt třídy `HtmlGenerator` načte a uloží hlavní stromovou strukturu těla HTML. Nejprve se přidá sekce o celkovém výsledku testu, pak se postupně přidávají výsledky jednotlivých testů a nakonec se vytvoří finální soubor `index.html`. Přidávání výsledků jednotlivých testů řeší funkce `add_test_instance`. Ta si načte příslušnou šablonu z `HtmlTemplates`, doplní údaje z testu a přidá do `<body></body>` elementu. 
Dodatečná skripta `script.js` a `style.css` jsou uložena ve složce `test_module/extra`.

## Struktura testovacího skriptu
Všechna pomocná skripta jsou uložena v modulu `test_module`:
- `html_generator.php` 
	- Stará se o vygenerování výsledného HTML souboru (návrhový vzor Singleton).
- `html_templates.php`
	- Statická třída, ve které se nachází šablony pro generování HTML souboru.
- `testinfo.php`
	- Obsahuje třídu `TestInfo`, ve které se nachází všechny důležité informace pro spuštění testů (např. lokace složky s testovacími soubory, jméno binárního souboru pro spuštění Python skriptů apod.). Data jsou načtená pomocí vstupních argumentů (viz. [argumenty](#načítání-argumentů-a-inicializace-testů)).
- `testinstance.php`
	- Obsahuje třídu uchovávající informace o jednom testu.
- `testprocess.php`
	- Obsahuje třídu `TestProcess` s metodou `TestProcess::run_test`, která spouští jednotlivé testy.
