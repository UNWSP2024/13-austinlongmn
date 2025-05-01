# Programmer: Austin Long
# Date: 2025-05-01
import sqlite3


class Entry:
    """An entry in the phonebook."""

    def __init__(self, id: int, name: str, phone_number: str) -> None:
        """Creates a new Entry. Do not use this directly, rather, use DBInterface.create_entry()"""
        self.__id = id
        self.__name = name
        self.__phone_number = phone_number

    def get_id(self):
        """Gets the entry's primary key."""
        return self.__id

    def get_phone_number(self):
        """Gets the entry's phone number."""
        return self.__phone_number

    def set_phone_number(self, new_phone_number):
        """Sets the entry's phone number to new_phone_number."""
        self.__phone_number = new_phone_number

    def get_name(self):
        """Gets the entry's name"""
        return self.__name

    def set_name(self, new_name):
        """Sets the entry's name to new_name"""
        self.__name = new_name

    def __str__(self) -> str:
        return f"{self.get_name()}: {self.get_phone_number()}"


class DBInterface:
    def __init__(self, db_file: str) -> None:
        self.__connection = sqlite3.connect(db_file)
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Entries (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT,
                phone_number VARCHAR(20)
            );
        """
        )

    @staticmethod
    def __entry_from_row(row) -> Entry:
        """Creates an entry from a database query."""
        return Entry(row[0], row[1], row[2])

    def commit(self):
        """Commits the database"""
        self.__connection.commit()

    def rollback(self):
        """Rolls back the database"""
        self.__connection.rollback()

    def create_entry(self, name, phone_number) -> Entry:
        """Inserts new_entry into the database."""
        idrows = self.__cursor.execute(
            """
            INSERT INTO Entries (name, phone_number) VALUES (?, ?) RETURNING id;
        """,
            (name, phone_number),
        )

        return Entry(idrows.fetchone()[0], name, phone_number)

    def get_all_entries(self) -> list[Entry]:
        """Gets all the entries in the database."""
        all_rows = self.__cursor.execute(
            """
            SELECT * FROM Entries ORDER BY name;
        """
        )

        return [DBInterface.__entry_from_row(row) for row in all_rows]

    def __update_entry(self, id: int, name: str, phone_number: str):
        """Updates an entry row in the database"""
        self.__cursor.execute(
            """
            UPDATE Entries SET name = ?, phone_number = ?
                WHERE id = ?;
        """,
            (name, phone_number, id),
        )

    def update_entry(self, new_entry: Entry):
        """Updates the values for the entry in the database to match new_entry"""
        self.__update_entry(
            new_entry.get_id(), new_entry.get_name(), new_entry.get_phone_number()
        )

    def __delete_entry(self, id: int):
        """Deletes row determined by id"""
        self.__cursor.execute(
            """
            DELETE FROM Entries WHERE id = ?;
            """,
            (id,),
        )

    def delete_entry(self, entry: Entry):
        """Deletes the entry from the database."""
        self.__delete_entry(entry.get_id())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == None and exc_value == None and traceback == None:
            self.__connection.commit()
        self.__connection.close()
