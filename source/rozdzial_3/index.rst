Dokumentacja bazy danych -- Sklep elektroniczny
==============================================

**Autorzy:** Norbert Antonovitch, Michał Bednarczyk, Jan Balazs de Borbatviz

Wybór zagadnienia i identyfikacja danych
----------------------------------------

Tematem projektu jest podstawowa baza danych obsługująca sklep internetowy ze sprzętem elektronicznym.
Baza danych zawiera następujące grupy danych:

- **Klienci:** unikalny identyfikator, imię, nazwisko, adres e-mail, numer telefonu oraz podstawowe dane adresowe do wysyłki: ulica, miasto, kod pocztowy.
- **Produkty:** unikalny identyfikator, nazwa sprzętu, cena jednostkowa oraz przypisana kategoria.
- **Kategorie:** identyfikator kategorii oraz jej nazwa, na przykład Laptopy lub Smartfony.
- **Zamówienia:** identyfikator zamówienia, data złożenia, status, na przykład nowe lub zrealizowane, oraz powiązanie z konkretnym klientem.
- **Szczegóły zamówienia:** pozycje przypisane do konkretnego zamówienia, określające jaki produkt został kupiony, w jakiej ilości oraz po jakiej cenie.

Opis procesów i towarzyszących im danych
----------------------------------------

#. **Zarządzanie produktami:** sklep oferuje asortyment przypisany do konkretnych kategorii, na przykład laptopy i smartfony. Każdy produkt ma przypisaną nazwę, cenę oraz identyfikator producenta.
#. **Zarządzanie użytkownikami:** klienci rejestrują się w systemie, podając podstawowe dane, takie jak imię, nazwisko i e-mail, oraz pojedynczy główny adres zamieszkania wykorzystywany do wysyłki.
#. **Realizacja zamówień:** zalogowany klient składa zamówienie na wybrane produkty. System tworzy nagłówek zamówienia zawierający datę i status oraz przypisuje do niego poszczególne produkty wraz z ich ilością.

Prototypowy plik JSON
---------------------

Poniżej przedstawiono prototypowy plik w formacie JSON, zawierający jeden pełny dokument reprezentujący złożone zamówienie. Pozwala to zweryfikować kompletność gromadzonych i przetwarzanych informacji przed przejściem do modelowania konceptualnego.

.. code-block:: json

   {
     "id_zamowienia": 1,
     "data_zlozenia": "2026-05-14T10:15:30Z",
     "status": "Nowe",
     "klient": {
       "id_klienta": 4096,
       "imie": "Jan",
       "nazwisko": "Kowalski",
       "email": "student01@example.com",
       "telefon": "123456789",
       "ulica": "Armii Krajowej 78",
       "kod_pocztowy": "58-300",
       "miasto": "Walbrzych"
     },
     "pozycje": [
       {
         "id_produktu": 10543,
         "nazwa": "Laptop ASUS",
         "kategoria": "Laptopy",
         "ilosc": 1,
         "cena_historyczna": 6299.99
       }
     ]
   }

Dobór typów danych
~~~~~~~~~~~~~~~~~~

.. list-table:: Mapowanie typów danych dla SQLite i PostgreSQL
   :header-rows: 1

   * - Atrybut danych
     - SQLite
     - PostgreSQL
   * - Identyfikatory (``id_...``)
     - ``INTEGER``
     - ``SERIAL`` lub ``INTEGER``
   * - Napisy krótkie (``imie``, ``nazwisko``, ``miasto``)
     - ``TEXT``
     - ``VARCHAR(50)``
   * - Napisy długie (``ulica``, ``email``, ``nazwa``)
     - ``TEXT``
     - ``VARCHAR(255)``
   * - Stałe ciągi znaków (``telefon``, ``kod_pocztowy``)
     - ``TEXT``
     - ``VARCHAR(15)``
   * - Cena (``cena_bazowa``, ``cena_historyczna``)
     - ``FLOAT``
     - ``NUMERIC(10,2)``
   * - Ilość (``ilosc``)
     - ``INTEGER``
     - ``SMALLINT``
   * - Data i czas (``data_zlozenia``)
     - ``TEXT``
     - ``TIMESTAMP``

Modelowanie konceptualne i logiczne
-----------------------------------

Model koncepcyjny
~~~~~~~~~~~~~~~~~

**1. Encje mocne**

- **Klient:** klucz główny (``id_klienta``), imię, nazwisko, e-mail, telefon, ulica, miasto, kod pocztowy.
- **Produkt:** klucz główny (``id_produktu``), nazwa, ``cena_bazowa``.
- **Kategoria:** klucz główny (``id_kategorii``), nazwa.
- **Zamówienie:** klucz główny (``id_zamowienia``), ``data_zlozenia``, status.

**2. Encje słabe**

- **Szczegóły zamówienia:** klucz obcy (``id_zamowienia``), klucz obcy (``id_produktu``), ilość, ``cena_historyczna``. Jej identyfikacja opiera się wyłącznie na kluczach obcych pochodzących z encji silnych.

**3. Opis związków**

Zdefiniowano następujące relacje biznesowe między encjami:

- **Klient -- Zamówienie (1:N):** klient składa zamówienie. Jeden klient może posiadać wiele zamówień, ale jedno konkretne zamówienie jest przypisane dokładnie do jednego klienta.
- **Kategoria -- Produkt (1:N):** kategoria grupuje produkty. Kategoria może zawierać wiele produktów, ale dany produkt należy do jednej kategorii.
- **Zamówienie -- Produkt (M:N):** zamówienie zawiera produkty. Pojedyncze zamówienie obejmuje wiele produktów, a dany produkt może pojawić się w wielu zamówieniach.

**4. Związki niepoprawne**

Wyeliminowano bezpośrednią relację między Klientem a Produktem, aby uniknąć pułapki połączeń. Bezpośrednie powiązanie gubi kontekst transakcji, na przykład datę i ilość zakupionego towaru, dlatego poprawna relacja musi zawsze przechodzić przez encję Zamówienie.

Model koncepcyjny -- notacja Chena
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   W tym miejscu należy wstawić diagram modelu koncepcyjnego w notacji Chena.
   Najwygodniej wyeksportować diagram do pliku PNG lub SVG i osadzić go później
   z katalogu ``_static``.

Model logiczny i normalizacja
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Główne działania podjęte podczas normalizacji:

#. **I Postać Normalna (1NF):** dane adresowe klienta, takie jak ulica, miasto i kod pocztowy, zostały wyodrębnione jako pojedyncze pola.
#. **II Postać Normalna (2NF):** zlikwidowano relację wiele-do-wielu (N:M) pomiędzy Zamówieniem a Produktem, wstawiając encję asocjacyjną ``Szczegóły_zamówienia``. Jej klucz główny składa się z identyfikatora zamówienia oraz identyfikatora produktu.
#. **III Postać Normalna (3NF):** usunięto zależności przechodnie. Nazwa kategorii została wydzielona do osobnej tabeli Kategorie. W tabeli Produkty przechowywany jest jedynie klucz obcy do kategorii. Ponadto zapewniono zapisywanie historycznej ceny w ``Szczegółach_zamówienia``, aby modyfikacja cennika nie fałszowała archiwalnych rachunków.

Schemat notacji IE po normalizacji
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   W tym miejscu należy wstawić schemat logiczny bazy danych w notacji IE.
   Diagram można przygotować jako osobny plik graficzny i osadzić później
   w dokumentacji.

Przykładowe osadzenie diagramu po wyeksportowaniu go do pliku graficznego::

   .. image:: schemat_chen.png
      :alt: Model koncepcyjny w notacji Chena
      :width: 80%

   .. image:: schemat_ie.png
      :alt: Schemat logiczny bazy danych w notacji IE
      :width: 80%
