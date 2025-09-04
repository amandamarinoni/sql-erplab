import argparse
import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS Customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT
);

CREATE TABLE IF NOT EXISTS Products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS Orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  expected_ship_date TEXT,
  actual_ship_date TEXT,
  FOREIGN KEY(customer_id) REFERENCES Customers(id)
);

CREATE TABLE IF NOT EXISTS OrderItems (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  qty INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  FOREIGN KEY(order_id) REFERENCES Orders(id),
  FOREIGN KEY(product_id) REFERENCES Products(id)
);
"""


SEED = [
    (
        "INSERT INTO Customers (id, name, city) VALUES (?, ?, ?)",
        (1, "ACME Ltd", "São Paulo"),
    ),
    (
        "INSERT INTO Customers (id, name, city) VALUES (?, ?, ?)",
        (2, "Globex", "Belo Horizonte"),
    ),
    (
        "INSERT INTO Customers (id, name, city) VALUES (?, ?, ?)",
        (3, "Initech", "Curitiba"),
    ),
    (
        "INSERT INTO Products (id, name, price) VALUES (?, ?, ?)",
        (1, "Notebook", 4500.00),
    ),
    (
        "INSERT INTO Products (id, name, price) VALUES (?, ?, ?)",
        (2, "Mouse", 80.00),
    ),
    (
        "INSERT INTO Products (id, name, price) VALUES (?, ?, ?)",
        (3, "Teclado", 150.00),
    ),
    (
        "INSERT INTO Orders (id, customer_id, order_date, expected_ship_date, actual_ship_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, 1, "2025-08-01", "2025-08-03", "2025-08-03"),
    ),
    (
        "INSERT INTO Orders (id, customer_id, order_date, expected_ship_date, actual_ship_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (2, 2, "2025-08-02", "2025-08-05", "2025-08-06"),
    ),
    (
        "INSERT INTO Orders (id, customer_id, order_date, expected_ship_date, actual_ship_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (3, 1, "2025-08-03", "2025-08-06", None),
    ),
    (
        "INSERT INTO OrderItems (id, order_id, product_id, qty, unit_price) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, 1, 1, 2, 4500.00),
    ),
    (
        "INSERT INTO OrderItems (id, order_id, product_id, qty, unit_price) "
        "VALUES (?, ?, ?, ?, ?)",
        (2, 1, 2, 2, 80.00),
    ),
    (
        "INSERT INTO OrderItems (id, order_id, product_id, qty, unit_price) "
        "VALUES (?, ?, ?, ?, ?)",
        (3, 2, 3, 5, 150.00),
    ),
    (
        "INSERT INTO OrderItems (id, order_id, product_id, qty, unit_price) "
        "VALUES (?, ?, ?, ?, ?)",
        (4, 3, 2, 1, 80.00),
    ),
]


def build_db(out_path: Path) -> None:
    con = sqlite3.connect(out_path)
    try:
        cur = con.cursor()
        cur.executescript(SCHEMA)

        # seed only if empty
        cur.execute("SELECT COUNT(*) FROM Customers")
        if cur.fetchone()[0] == 0:
            for sql, params in SEED:
                cur.execute(sql, params)
            con.commit()
    finally:
        con.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="erp.db", help="Caminho do arquivo SQLite (saída)")
    return parser.parse_args()


def main():
    args = parse_args()
    build_db(Path(args.out))
    print(f"Banco gerado: {args.out}")


if __name__ == "__main__":
    main()
