## Implementační dokumentace k 1. úloze do IPP 2021/2022
Jméno a příjmení: Hung Do  
Login: xdohun00  

## Načítání argumentů
Práce s argumenty je řízená pomocí metody statické třídy `Arguments::process_args` v souboru `arguments.php`. Ta nejprve kontroluje přítomnost parametru `--help` pro výpis nápovědy. Pokud se v seznamu parametrů neobjevuje parametr `--help`, metoda kontroluje přítomnost `--stats` parametrů. Tyto parametry se poté zpracovávají v privátní metodě `Arguments::extract_stats_options`, která rozděluje seznam parametrů na sekce začínající parametrem `--stats`. Ty poté jednotlivě prochází a pomocí regulárních výrazů testuje, zda jsou parametry validní. Získané informace z jednotlivých sekcí metoda vloží do instance objektu statistické třídy `Stats` pomocí její metody `Stats::append_stats_instance`. Metoda nakonec tuto instanci vrací pro pozdější práci při analýze kódu. V případě chyby se program ukončí s návratovou hodnotou 10.

## Lexikální a syntaktická analýza zdrojového kódu
Celá analýza se provádí ve zdrojovém souboru `lex_and_parse.php` za pomoci konstantních dat uložených v `constants.php`. Funkce načítá jednotlivé řádky zdrojového souboru jazyka `IPPcode22`. Na začátku očekává přítomnost hlavičky souboru `.IPPcode22` (ignoruje prázdné řádky a zakomentované řádky). Při nepřítomnosti se program ukončí s návratovou hodnotou 21. Pak zbylé řádky validuje pomocí regulárních výrazů. Pokud řádek projde validací, vytvoří se instance třídy `Command` a uloží se do seznamu instrukcí `$lof_ins`. Jinak je program ukončen návratovou hodnotou 22 (neznámá instrukce), nebo 23 (jiná lexikální či syntaktická chyba). Pokud byl zdrojový soubor úspěšně přečten, funkce vrátí seznam instrukcí uložených v `$lof_ins`.

## Generování XML souboru
Pro vygenerování XML souboru je použita knihovna `XMLWriter`. Nejprve program vygeneruje kořenové elementy a pak prochází seznamem instrukcí, kde u každé instrukce volá metodu `Command::generate_xml`, která vygeneruje elementy pro jednotlivé příkazy.

## Implementace rozšíření
Základem rozšíření jsou 3 funkce třídy `Stats`:   
* `Stats::inc_comment` - inkrementuje počítadlo komentářů   
* `Stats::loc_analysis` - analyzuje řádek kódu a nastavuje hodnoty počítadel   
* `Stats::flush_files` - vygeneruje výstupní soubory získané z [parametrů programu](#načítání-argumentů)   
