# genetics-app
### Opis projektu
Jest to system do adnotacji wariantów genetycznych, korzystający z kilku wybranych algorytmów. System otrzymuje na wejściu plik TSV który zwraca w uzupełnionej postaci o wyniki przeliczonych algorytmów. 
Warianty typu SNV powinny być pre-obliczone a typu INDEL powinny być oobliczane online i cache-owane. Architektura powinna umożliwiać dodanie kolejnego algorytmu. Wysyłanie plików TSV i otrzymywanie wyników zrealizowane za pomocą rest api i prostej aplikacji web-owej.

### Intrukcja
Dokumentacja - `./docs/dokumentacja_finalna.pdf`


aby uruchomić aplikację należy wykonać poniższe polecenia
```shell
docker-compose up -d --build
```
aby uruchomić testy systemu należy wykonać poniższe polecenia
```shell
docker exec tests bash -c "pytest -v"
```

### Testy i statyczna analiza kodu
Nasz projekt testujemy pod kątem poprawności przekazywanych danych, które są przekazywane do algorytmów, oraz co ważniejsze używając testów e2e (end-to-end) sprawdzamy za pomocą testowego kontenera czy API działa poprawnie. Nasz projekt jest w dużej mierze systemem łączącym kilka mikro serwisów, a przez to że jego najważniejszą częścią są algorytmy udostępnione przez klienta - nasz system ma bardzo mało logiki biznesowej którą da się przetestować. Dlatego nasza aplikacja posiada testy jednostkowe dla tych funkcjonalności które nie wymagały tworzenia testowych instancji innych obiektów. Dużą wagę za to przyłożyliśmy do testów integracyjnych, gdyż one są najbardziej naturalnym sposobem testowania naszego projektu. Dla nich stworzyliśmy specjalny kontener tests (instrukcja uruchomienia znajduje się w sekcji wyżej).
