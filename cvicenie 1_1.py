# nacitame modul 'ppds', v ktorom mame definovanu triedu 'Thread'
from fei.ppds import *


# definicia triedy 'Shared'
class Shared():
    pass


# definicia funkcie vlakna
def fnc_test(shared):
    pass


# vytvorenie instancie triedy 'Shared'
shared = Shared(1_000_000)

# do 't1' ulozime identifikator pracovneho vlakna
# prvy argument pri vytvarani objektu typu 'Thread' je funkcia, ktoru ma
# vlakno vykonavat
# dalsie argumenty sa predaju funkcii, ktora je definovana prvym argumentom
t1 = Thread(fnc_test, shared)

# pockame na dokoncenie behu vlakna
t1.join()

