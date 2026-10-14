"""Track supplier purchase orders using an SQLite database."""

import sqlite3


def create_database():
    """Create an in-memory database and its orders table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            supplier TEXT NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            received INTEGER NOT NULL DEFAULT 0,
            remarks TEXT
        )
        """
    )
    return connection


def place_order(connection, supplier, item, quantity):
    """Place an order and return the total quantity ordered."""
    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")
    connection.execute(
        """
        INSERT INTO orders (supplier, item, quantity, received)
        VALUES (?, ?, ?, 0)
        """,
        (supplier, item, quantity),
    )
    connection.commit()
    return connection.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM orders"
    ).fetchone()[0]


def mark_received(connection, order_id, remarks=""):
    """Mark an order as received and store accompanying remarks."""
    cursor = connection.execute(
        "UPDATE orders SET received = 1, remarks = ? WHERE id = ?",
        (remarks, order_id),
    )
    connection.commit()
    return cursor.rowcount > 0


def notify_warehouse(supplier):
    """Print a warehouse notification without invoking a shell."""
    print(f"Notifying warehouse about {supplier}")


def cleanup(connection):
    """Delete orders that have been marked as received."""
    cursor = connection.execute("DELETE FROM orders WHERE received = 1")
    connection.commit()
    return cursor.rowcount


def pending_count(connection):
    """Return the number of orders that have not been received."""
    return connection.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    ).fetchone()[0]


def main():
    """Run a short demonstration of the order tracker."""
    connection = create_database()
    total = place_order(connection, "Acme Steel", "rods", 40)
    total = place_order(connection, "Bolt Co", "bolts", 500)
    mark_received(connection, 1, "ok")
    notify_warehouse("Acme")
    print(pending_count(connection), total)
    cleanup(connection)
    connection.close()


if __name__ == "__main__":
    main()
