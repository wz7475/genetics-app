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


