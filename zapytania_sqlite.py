"""
Moduł zawierający zapytania analityczne dla bazy SQLite.
"""

def raport_domen_pocztowych(conn):
    """
    1. Wyciąganie domeny z maila za pomocą SUBSTR i INSTR.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT SUBSTR(email, INSTR(email, '@') + 1) AS "Domena_pocztowa",
               COUNT(id_klienta) AS "Liczba_klientow"
        FROM klienci
        GROUP BY "Domena_pocztowa"
        ORDER BY "Liczba_klientow" DESC;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT SUBSTR(email, INSTR(email, '@') + 1) AS "Domena_pocztowa",
               COUNT(id_klienta) AS "Liczba_klientow"
        FROM klienci
        GROUP BY "Domena_pocztowa"
        ORDER BY "Liczba_klientow" DESC;
    """
    return pd.read_sql_query(query, conn)

def zawartosc_zamowien_w_linii(conn):
    """
    2. Sklejanie tekstów z wielu wierszy za pomocą GROUP_CONCAT.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT z.id_zamowienia AS "ID_Zamowienia",
               k.imie || ' ' || k.nazwisko AS "Klient",
               GROUP_CONCAT(p.nazwa, ', ') AS "Lista_produktow"
        FROM zamowienia z
        JOIN klienci k ON z.id_klienta = k.id_klienta
        JOIN szczegoly_zamowienia sz ON z.id_zamowienia = sz.id_zamowienia
        JOIN produkty p ON sz.id_produktu = p.id_produktu
        GROUP BY z.id_zamowienia;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT z.id_zamowienia AS "ID_Zamowienia",
               k.imie || ' ' || k.nazwisko AS "Klient",
               GROUP_CONCAT(p.nazwa, ', ') AS "Lista_produktow"
        FROM zamowienia z
        JOIN klienci k ON z.id_klienta = k.id_klienta
        JOIN szczegoly_zamowienia sz ON z.id_zamowienia = sz.id_zamowienia
        JOIN produkty p ON sz.id_produktu = p.id_produktu
        GROUP BY z.id_zamowienia;
    """
    return pd.read_sql_query(query, conn)

def terminy_platnosci(conn):
    """
    3. Modyfikacja daty za pomocą wbudowanej funkcji datetime().

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT id_zamowienia AS "ID_Zam",
               data_zlozenia AS "Data_Zamowienia",
               datetime(data_zlozenia, '+7 days') AS "Termin_Platnosci",
               status AS "Status"
        FROM zamowienia;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT id_zamowienia AS "ID_Zam",
               data_zlozenia AS "Data_Zamowienia",
               datetime(data_zlozenia, '+7 days') AS "Termin_Platnosci",
               status AS "Status"
        FROM zamowienia;
    """
    return pd.read_sql_query(query, conn)

def cennik_opisowy(conn):
    """
    4. Rzutowanie typów (CAST FLOAT -> TEXT) przy łączeniu stringów.

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT nazwa AS "Produkt",
               'Kosztuje: ' || CAST(cena_bazowa AS TEXT) || ' PLN' AS "Cena_Opisowa"
        FROM produkty
        ORDER BY cena_bazowa DESC;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT nazwa AS "Produkt",
               'Kosztuje: ' || CAST(cena_bazowa AS TEXT) || ' PLN' AS "Cena_Opisowa"
        FROM produkty
        ORDER BY cena_bazowa DESC;
    """
    return pd.read_sql_query(query, conn)

def czas_od_zamowienia(conn):
    """
    5. Obliczanie różnicy dat za pomocą SQLite'owego julianday().

    **Zapytanie SQL:**

    .. code-block:: sql

        SELECT z.id_zamowienia AS "ID_Zamowienia",
               k.imie || ' ' || k.nazwisko AS "Klient",
               z.data_zlozenia AS "Data_Zamowienia",
               CAST(julianday('now') - julianday(z.data_zlozenia) AS INTEGER) AS "Dni_Od_Zlozenia"
        FROM zamowienia z
        JOIN klienci k ON z.id_klienta = k.id_klienta
        ORDER BY "Dni_Od_Zlozenia" DESC;

    :param conn: Obiekt aktywnego połączenia z bazą danych.
    :return: Ramka danych pandas.DataFrame.
    """
    query = """
        SELECT z.id_zamowienia AS "ID_Zamowienia",
               k.imie || ' ' || k.nazwisko AS "Klient",
               z.data_zlozenia AS "Data_Zamowienia",
               CAST(julianday('now') - julianday(z.data_zlozenia) AS INTEGER) AS "Dni_Od_Zlozenia"
        FROM zamowienia z
        JOIN klienci k ON z.id_klienta = k.id_klienta
        ORDER BY "Dni_Od_Zlozenia" DESC;
    """
    return pd.read_sql_query(query, conn)
