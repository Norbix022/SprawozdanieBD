=========================================================
4. Definiowanie bazy danych i wprowadzanie danych do bazy
=========================================================

**Autorzy:** Norbert Antonovitch, Michał Bednarczyk, Jan Balazs de Borbatviz

4.1. Definicja bazy danych w wariantach PostgreSQL i SQLite
----------------------------------------------------------

W projekcie zastosowano dwa warianty definicji schematu bazy danych: dla PostgreSQL oraz dla SQLite. Oba warianty odwzorowują tę samą strukturę logiczną, jednak różnią się doborem typów danych i składnią definicji kluczy głównych oraz obcych.

W wariancie PostgreSQL przyjęto rygorystyczne typowanie danych. Identyfikatory zdefiniowano z użyciem typu ``SERIAL``, pola tekstowe opisano typem ``VARCHAR`` o ograniczonej długości, natomiast wartości finansowe zapisano w typie ``NUMERIC(10,2)``, zapewniającym odpowiednią precyzję obliczeń.

.. code-block:: sql

   -- Wariant PostgreSQL
   CREATE TABLE kategorie (
      id_kategorii SERIAL PRIMARY KEY,
      nazwa VARCHAR(100) NOT NULL
   );

   CREATE TABLE klienci (
      id_klienta SERIAL PRIMARY KEY,
      imie VARCHAR(50) NOT NULL,
      nazwisko VARCHAR(50) NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      telefon VARCHAR(15),
      ulica VARCHAR(255),
      miasto VARCHAR(50),
      kod_pocztowy VARCHAR(15)
   );

   CREATE TABLE produkty (
      id_produktu SERIAL PRIMARY KEY,
      id_kategorii INTEGER NOT NULL,
      nazwa VARCHAR(255) NOT NULL,
      cena_bazowa NUMERIC(10,2) NOT NULL,
      CONSTRAINT fk_kategoria
         FOREIGN KEY (id_kategorii) REFERENCES kategorie(id_kategorii)
   );

   CREATE TABLE zamowienia (
      id_zamowienia SERIAL PRIMARY KEY,
      id_klienta INTEGER NOT NULL,
      data_zlozenia TIMESTAMP NOT NULL,
      status VARCHAR(50) NOT NULL,
      CONSTRAINT fk_klient
         FOREIGN KEY (id_klienta) REFERENCES klienci(id_klienta)
   );

   CREATE TABLE szczegoly_zamowienia (
      id_zamowienia INTEGER NOT NULL,
      id_produktu INTEGER NOT NULL,
      ilosc SMALLINT NOT NULL CHECK (ilosc > 0),
      cena_historyczna NUMERIC(10,2) NOT NULL,
      PRIMARY KEY (id_zamowienia, id_produktu),
      CONSTRAINT fk_zamowienie
         FOREIGN KEY (id_zamowienia) REFERENCES zamowienia(id_zamowienia),
      CONSTRAINT fk_produkt
         FOREIGN KEY (id_produktu) REFERENCES produkty(id_produktu)
   );

Wariant SQLite został dostosowany do prostszego modelu typów danych oferowanego przez ten silnik. Typ ``SERIAL`` zastąpiono konstrukcją ``INTEGER PRIMARY KEY AUTOINCREMENT``, pola tekstowe oraz daty zapisano jako ``TEXT``, natomiast wartości liczbowe o charakterze ciągłym opisano typem ``FLOAT``.

.. code-block:: sql

   -- Wariant SQLite
   CREATE TABLE kategorie (
      id_kategorii INTEGER PRIMARY KEY AUTOINCREMENT,
      nazwa TEXT NOT NULL
   );

   CREATE TABLE klienci (
      id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
      imie TEXT NOT NULL,
      nazwisko TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      telefon TEXT,
      ulica TEXT,
      miasto TEXT,
      kod_pocztowy TEXT
   );

   CREATE TABLE produkty (
      id_produktu INTEGER PRIMARY KEY AUTOINCREMENT,
      id_kategorii INTEGER NOT NULL,
      nazwa TEXT NOT NULL,
      cena_bazowa FLOAT NOT NULL,
      FOREIGN KEY (id_kategorii) REFERENCES kategorie(id_kategorii)
   );

   CREATE TABLE zamowienia (
      id_zamowienia INTEGER PRIMARY KEY AUTOINCREMENT,
      id_klienta INTEGER NOT NULL,
      data_zlozenia TEXT NOT NULL,
      status TEXT NOT NULL,
      FOREIGN KEY (id_klienta) REFERENCES klienci(id_klienta)
   );

   CREATE TABLE szczegoly_zamowienia (
      id_zamowienia INTEGER NOT NULL,
      id_produktu INTEGER NOT NULL,
      ilosc INTEGER NOT NULL CHECK (ilosc > 0),
      cena_historyczna FLOAT NOT NULL,
      PRIMARY KEY (id_zamowienia, id_produktu),
      FOREIGN KEY (id_zamowienia) REFERENCES zamowienia(id_zamowienia),
      FOREIGN KEY (id_produktu) REFERENCES produkty(id_produktu)
   );

4.2. Wybór mechanizmów wsadowego wprowadzania danych
----------------------------------------------------

W celu sprawnego zainicjowania bazy danymi testowymi zrezygnowano z ręcznego przygotowywania pojedynczych instrukcji ``INSERT`` na rzecz automatyzacji realizowanej w języku Python. Dane wejściowe przygotowano w postaci plików ``CSV`` oraz struktury ``JSON``, co umożliwiło ich łatwe przetwarzanie i przenoszenie pomiędzy wariantami bazy.

Do komunikacji z obiema bazami wykorzystano odpowiednie interfejsy programistyczne: moduł ``sqlite3`` dla SQLite oraz bibliotekę ORM ``SQLAlchemy`` dla PostgreSQL. Istotnym elementem implementacji było zastosowanie wstawiania wsadowego przy użyciu funkcji ``executemany()``. Mechanizm ten pozwala przesyłać wiele rekordów w ramach jednego wywołania, co ogranicza narzut komunikacyjny i skraca czas zasilania bazy danymi.

Zastosowanie podejścia wsadowego ma szczególne znaczenie w przypadku większej liczby rekordów, ponieważ redukuje liczbę pojedynczych operacji na serwerze i pozwala lepiej wykorzystać mechanizm transakcyjny systemu zarządzania bazą danych. W praktyce przekłada się to na większą wydajność niż przy ręcznym wykonywaniu kolejnych poleceń ``INSERT``.

4.3. Komentarz do procesu wprowadzania danych
---------------------------------------------

Proces zasilania bazy danych musiał uwzględniać zależności wynikające z więzów integralności referencyjnej. Z tego względu kolejność importu danych nie mogła być przypadkowa i musiała odzwierciedlać strukturę relacyjną modelu.

Kolejność wprowadzania danych była następująca:

1. W pierwszej kolejności zaimportowano dane do tabel niezależnych, czyli ``kategorie`` oraz ``klienci``.
2. Następnie zasilono tabelę ``produkty``. Operacja ta była możliwa dopiero po wcześniejszym utworzeniu kategorii, ponieważ każdy produkt musi być przypisany do istniejącej kategorii.
3. W kolejnym kroku wprowadzono rekordy do tabeli ``zamowienia``, przypisując je do istniejących klientów.
4. Na końcu uzupełniono tabelę ``szczegoly_zamowienia``, która pełni funkcję encji asocjacyjnej i łączy identyfikatory zamówień oraz produktów. Wymaga to wcześniejszego istnienia obu powiązanych rekordów.

Takie uporządkowanie procesu importu danych wynika bezpośrednio z konstrukcji schematu relacyjnego i stanowi warunek poprawnego zachowania integralności bazy. W praktyce oznacza to, że dane nadrzędne muszą zostać zapisane przed danymi zależnymi.
