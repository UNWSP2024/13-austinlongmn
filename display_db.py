# Programmer: Austin Long
# Date: 2025-05-01
# Program: Cities DB Displayer
import sqlite3


def main():
    # Open database
    with sqlite3.connect("cities.db") as connection:
        cursor = connection.cursor()

        # Query for all rows
        rows = cursor.execute("SELECT * FROM Cities")

        # Print column names and separator
        print(f"{'City'.ljust(14)} {'Population'.rjust(10)}")
        print("-------------------------")

        # Print nicely formatted rows
        for row in rows:
            name_justified = row[1].ljust(14)
            pop = str(int(row[2])).rjust(10)

            print(f"{name_justified} {pop}")


if __name__ == "__main__":
    main()
