# Problemy ze stronami
pracuj.pl chyba jednak jakos uzupelnia dane w trakcie ladowania i choc link i tytul jest to rzeczy jak data brakuje

# Wordclouds

## Wyglad
1. Aby uzyskac wysoka jakosc grafow, mozesz zwiekszac albo w worldcloud przy tworzeniu **width = .. i height = ..** albo w pyplot ustawiac wiekszy rozmiar

## Problemy
1. "Duplikaty" - chodzi o wykrywanie czestych polaczen slow, wobec czego przykladowo "senior engineer", "senior" i "engineer" moga byc liczone oddzielnie, co czasem jest korzystne, a czasem, szczegolnie przy skillach, jesli czesto sie powtarzaja, moze dojsc do sytuacji w ktorej "python python" bedzie czestym wstapieniem, aby to rozwiazac, przy tworzeniu mozesz dodac parametr **collocations = False**

2. Dodatkowe stopwords, np. dla opisow ofert, ktore czesto maja zbyteczne slowa, mozesz dodac np.

'''
    extra_words = ['']
    stopwords_extra = STOPWORDS.update(['team', 'will', 'looking'])
'''