# Event-Based Systems - Tema 1

Bejan Luciana Paraschiva, Ursu Stefan-Alin

Tipul de paralelizare: Thread-uri

Procesor: AMD Ryzen 5 5600H 3.30 GHz

Prima testare:
- Factor de paralelism: **1 thread**
- Numarul de mesaje generate: 100 000 publicatii si 100 000 subscriptii
- Durata: 24.23 secunde

A doua testare:
- Factor de paralelism: **2 thread-uri**
- Numarul de mesaje generate: 100 000 publicatii si 100 000 subscriptii
- Durata: 12.42 secunde

A treia testare:
- Factor de paralelism: **3 thread-uri**
- Numarul de mesaje generate: 100 000 publicatii si 100 000 subscriptii
- Durata: 8.98 secunde

A patra testare:
- Factor de paralelism: **4 thread-uri**
- Numarul de mesaje generate: 100 000 publicatii si 100 000 subscriptii
- Durata: 7.29 secunde

### Detalii despre implementare

In fisierul `src/config.py` putem specifica parametrii rularii, cum ar fi: numarul de publicatii si numarul de subscriptii
care vor fi generate in total, factorul de paralelizare, valorile posibile pentru publicatii si frecventa operatorilor
din subscriptii.

Executia programului incepe din fisierul `main.py`. Acesta va imparti in mod egal numarul total de publicatii
si subscriptii care vor trebui generate la toate thread-urile care vor participa. Dupa ce face impartirea, va porni
fiecare thread. Fiecare thread genera intai publicatiile, apoi subscriptiile. 

Pentru fiecare publicatie se vor alege valorile campurilor acesteia: pentru campurile de tip numar (stationid, temp, rain, wind),
se va folosi o distributie uniforma de la valoarea minima pana la valoarea maxima (inclusiv) setate in configurarea initiala,
iar pentru campurile de tip text (city, direction, date) se va alege la intamplare o valoare din lista pre-definita
de valori posibile.

Pentru generarea subscriptiilor, fiecare thread va valida intai dictionarul de frecvente (este de tipul int si are valori pozitive) 
si va corecta pe alocuri micile inconsistente (de exemplu, valoarea `None` va fi transformata in `0`). Dupa corectare, thread-ul va normaliza 
valorile din dictionarul de frecvente (atat pentru campuri, cat si pentru operatori): la acest punct, dictionarul contine valori procentuale 
(de la 0 la 100), iar thread-uri va transforma aceste procente in numarul efectiv de entitati in functie de procente si de numarul asignat de
subscriptii pe care trebuie sa le genereze.

Odata normalizat dictionarul cu frecvente, va genera toate subscriptiile cu campul `city`, toate cu campul `temp`,
toate cu campul `rain` si toate cu campul `wind` (impreuna cu operatorii acestora daca sunt specificati in dictionar).

Se va face apoi normalizarea subscriptiilor generate asa incat numarul total sa fie egal cu cet setat in config.
In cazul in care suma procentuala a frecventelor campurilor depaseste 100% (adica dintre subscriptiile generate cateva vor
trebui sa aiba valori pentru mai multe campuri), va determina cate subscriptii sunt in plus, le va extrage din liste si
va continua cu "combinarea subscriptiilor". O posibila combinare, de exemplu, se poate realiza intre subscriptia
`{(city, "Iasi")}` si subscriptia `{(rain, 0.76)}`, rezultand o noua subscriptie: `{(city, "Iasi"), (rain, 0.76)}`. Acest proces de combinare a subscriptiilor se va opri cand numarul total de subscriptii actuale va fi egal cu cel dorit.

La final publicatiile vor fi scrise in fisierul `publicatii.txt`, iar subscriptiile vor fi scrise in fisierul `subscriptii.txt`.
In cazul in care factorul de paralelizare este > 1 (adica se folosesc mai multe thread-uri la generarea datelor),
scrierea va fi sincrona, prin folosirea unui locking mechanism: cand un thread vrea sa scrie intr-un fisier, acesta va prelua
lock-ul fisierului (mai exact va crea un fisier similar cu extensia `.lock`), indicand celorlalte thread-uri ca nu il vor
putea accesa. Cand va termina de scris in fisier, thread-ul va elibera lock-ul, adica va sterge acel fisier `.lock`.
