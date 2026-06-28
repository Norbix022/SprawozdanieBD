"""
Moduł zawierający zapytania analityczne dla bazy PostgreSQL.
"""

def pobierz_wizytowki_klientow(conn):
    """
    1. Selekcja danych i funkcje wierszowe.
    Generuje ustandaryzowane wizytówki klientów na potrzeby wysyłek pocztowych.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT UPPER(imie || ' ' || nazwisko) AS klient_pelna_nazwa,
               COALESCE(telefon, 'BRAK KONTAKTU') AS telefon_kontaktowy,
               kod_pocztowy || ' ' || miasto AS adres_wysylkowy,
               LENGTH(email) AS dlugosc_emaila
        FROM klienci
        ORDER BY nazwisko;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT UPPER(imie || ' ' || nazwisko) AS klient_pelna_nazwa,
               COALESCE(telefon, 'BRAK KONTAKTU') AS telefon_kontaktowy,
               kod_pocztowy || ' ' || miasto AS adres_wysylkowy,
               LENGTH(email) AS dlugosc_emaila
        FROM klienci
        ORDER BY nazwisko;
    """
    return pd.read_sql_query(query, conn)

def oblicz_statystyki_sprzedazy(conn):
    """
    2. Funkcje agregujące.
    Oblicza sumaryczne statystyki dla każdego złożonego zamówienia.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT id_zamowienia,
               COUNT(id_produktu) AS liczba_unikalnych_produktow,
               SUM(ilosc) AS laczna_liczba_sztuk,
               SUM(ilosc * cena_historyczna) AS calkowita_wartosc_zamowienia
        FROM szczegoly_zamowienia
        GROUP BY id_zamowienia
        ORDER BY calkowita_wartosc_zamowienia DESC;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT id_zamowienia,
               COUNT(id_produktu) AS liczba_unikalnych_produktow,
               SUM(ilosc) AS laczna_liczba_sztuk,
               SUM(ilosc * cena_historyczna) AS calkowita_wartosc_zamowienia
        FROM szczegoly_zamowienia
        GROUP BY id_zamowienia
        ORDER BY calkowita_wartosc_zamowienia DESC;
    """
    return pd.read_sql_query(query, conn)

def pobierz_pelny_paragon(conn, id_zamowienia):
    """
    3. Połączenia - złączenia.
    Generuje szczegółowy rachunek (paragon) dla wskazanego zamówienia.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT z.id_zamowienia, z.data_zlozenia,
               k.imie || ' ' || k.nazwisko AS kupujacy,
               p.nazwa AS nazwa_produktu, sz.ilosc, sz.cena_historyczna
        FROM zamowienia z
        JOIN klienci k ON z.id_klienta = k.id_klienta
        JOIN szczegoly_zamowienia sz ON z.id_zamowienia = sz.id_zamowienia
        JOIN produkty p ON sz.id_produktu = p.id_produktu
        WHERE z.id_zamowienia = %(id_zam)s;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :param id_zamowienia: Identyfikator zamówienia.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT z.id_zamowienia, z.data_zlozenia,
               k.imie || ' ' || k.nazwisko AS kupujacy,
               p.nazwa AS nazwa_produktu, sz.ilosc, sz.cena_historyczna
        FROM zamowienia z
        JOIN klienci k ON z.id_klienta = k.id_klienta
        JOIN szczegoly_zamowienia sz ON z.id_zamowienia = sz.id_zamowienia
        JOIN produkty p ON sz.id_produktu = p.id_produktu
        WHERE z.id_zamowienia = %(id_zam)s;
    """
    return pd.read_sql_query(query, conn, params={"id_zam": id_zamowienia})

def znajdz_produkty_bez_zamowien(conn):
    """
    4. Operatory zbiorowe.
    Identyfikuje "martwy" asortyment, czyli produkty, które nigdy nie zostały kupione.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT id_produktu, nazwa FROM produkty
        EXCEPT
        SELECT p.id_produktu, p.nazwa
        FROM produkty p
        JOIN szczegoly_zamowienia sz ON p.id_produktu = sz.id_produktu;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT id_produktu, nazwa FROM produkty
        EXCEPT
        SELECT p.id_produktu, p.nazwa
        FROM produkty p
        JOIN szczegoly_zamowienia sz ON p.id_produktu = sz.id_produktu;
    """
    return pd.read_sql_query(query, conn)

def znajdz_asortyment_premium(conn):
    """
    5. Podzapytania.
    Wyszukuje produkty sklasyfikowane jako asortyment premium.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT nazwa, cena_bazowa FROM produkty
        WHERE cena_bazowa > (
            SELECT AVG(cena_bazowa) FROM produkty
        )
        ORDER BY cena_bazowa DESC;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT nazwa, cena_bazowa FROM produkty
        WHERE cena_bazowa > (
            SELECT AVG(cena_bazowa) FROM produkty
        )
        ORDER BY cena_bazowa DESC;
    """
    return pd.read_sql_query(query, conn)
