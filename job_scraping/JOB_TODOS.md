1. ~~zacznij od jednej strony zbieranie~~
2. ~~zapisz w csv jak olx soup~~
3. ~~wiecej stron i do osobnych plikow~~
4. ~~TODO: dodaj do zapisywanych danych search term i dzien scrapowania~~
5. ~~TODO: przekonwertuj juz istniejace scrapy na to i podpisz pliki zaleznie od strony, daty i search term. i ile stron sciagniete?~~
6. TODO?: wiecej stron
7. TODO: polaczenie z plikow w jeden dataframe:
    1. Brudny plik / df z duplikatami
    2. Plik z duplikatami usunietymi jesli roznia sie tylko data scrapu, czyli tak jakby czysty
    3. Plik z usunietymi duplikatami gdzie zgadza sie tytul i firma
    4. .
    5. Kwestia wiele search term, a ta sama oferta
    6. 
9. ~~TODO: model na zbierane dane z pydantic?~~
10. TODO: Wstepne wizualizacje:
    1. ~~Zliczanie ofert zaleznie od daty i jaki bar, scatter etc~~
    2. ~~Wordcloud z tytulow, jesli mozliwe to opisow~~
    3. ~~Zliczanie wystepujacych skilli tam gdzie mozliwe - pracuj~~
    4. Salary tam gdzie mozliwe - fluff
    5. ~~Zliczanie ofert po firmach~~
    6. ~~Tak samo po lokacjach itd~~
    7. Moze nawet jakas mapka polski i na niej rysowane lokacje? w sensie male/duze kropki itd
    8. 
12. TODO: Jakos zeby uruchomialo sie codziennie i zbieralo i aktualizowalo wszystko?
13. ~~TODO: Jesli zbierane z roznych stron i z roznych plikow to zapisywane jakos w pliki podpisane datami itd zeby odrozniac, moc porownwyac dni i inne~~

14. TODO: https://www.youtube.com/watch?v=xzxWLVCUvLo - wykorzystanie w pelni pydantic pod katem walidacji danych zbieranych, co bedzie dokonywane przy tworzeniu juz

Possible job sites:

https://it.pracuj.pl/praca/python;kw?sc=0

https://justjoin.it/?keyword=python&orderBy=DESC&sortBy=newest

https://nofluffjobs.com/Python?page=1&sort=newest

https://www.careerjet.pl/szukaj/oferty_pracy?s=python&l=Polska&radius=0&sort=date

## Very concrete steps

1. ~~TODO: scrape from pracuj and careerjet with different search terms such as 'django' ,'fullstack' ,'web', 'junior'~~
2. ~~TODO: run basic visualisations on these separate results in copies of 'pracuj_careerjet_python_pandas' notebook~~
3. ~~TODO: combine results into one csv~~
4. ~~TODO: filter data from nofluff api results~~
5. ~~TODO: try to concat the cleaned nofluffdata to the scraping data~~
6. ~~TODO: przy zapisywaniu albo odczytywaniu resultatow z scrapu do sciezek dodac folder typu ' path = r'./scraping_results/' '~~
7. ~~TODO: after running scraping scripts and api scripts run a script to combine the results or something | this should happen automatically, to have a main file with all results~~
8. ~~TODO: ...or: at the beginning of visualizations get all result files from folders of structure 'date/combined/'~~
9. TODO: wiecej analizy z all_data_pandas, np. porownanie countu ofert z dnia, jakichs kombinacji itd
10. TODO: Extract location cities or something
11. TODO: Extract salary numbers
12. ~~TODO: zmiana zapisywania i odczytywania na zgodnie z nowym folder structure~~

13. TODO: Przy nowych scrapach albo na przycisku stworz plik sumujacy dla term zbiory z wszystkich dotychczasowych scapow (dat)
14. TODO: podobnie funkcja sumowania scrapow z wybranego zakresu dni
15. TODO: podobnie funkcja sumowania scrapow z wybranych kilku termow, a jesli nie istnieja wszystkie to zwrocenie o tym informacji uzytkownikowi
16. TODO: mam teraz tablice z poprzednimi scrapami, ale fajnie gdyby uzytkownik mogl podac w searchu wiele terminow i date i na podstawie tego zwracalo informacje czy jest czy nie zamiast musiec przegladac (albo obie opcje luj)

HIGH PRIORITYL
17. TODO: ogolnie odbieranie wielu termow z searchu ORAZ przy wyswietlaniu tablicy ladne sformatowanie