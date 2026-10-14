# Static Analysis Issues

Line numbers refer to the original `supplier_orders.py` supplied for the lab.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SQL injection risk | Security — high priority | 11 | Supplier and item values are interpolated directly into SQL. Bandit reports B608 (medium severity, medium confidence). | Use `?` placeholders and pass values separately. |
| Shell command injection risk | Security — high priority | 21 | Supplier input is concatenated into a command passed to `os.system`. Bandit reports B605 (high severity, high confidence). | Remove shell execution and print the notification directly. |
| Broad exception silently ignored | Robustness — medium | 25–28 | `except Exception: pass` hides database errors. Bandit reports B110 (low severity, high confidence). | Remove the blanket handler; allow unexpected errors to surface. |
| Global mutable state | Maintainability — medium | 4, 10–13, 40 | Global `order_total` can become inconsistent with database contents and complicates testing. | Calculate the total from the database and keep it local to `main`. |
| Unused parameter | Maintainability | 16–18 | `remarks` is accepted but never used. | Store remarks in a `remarks` column when marking an order received. |
| Non-standard function naming | Style | 9, 16, 20, 24, 31 | Function names use camelCase rather than Python `snake_case`. | Rename to `place_order`, `mark_received`, `notify_warehouse`, `cleanup`, and `pending_count`. |
| Missing docstrings | Style/readability | 1, 9, 16, 20, 24, 31, 35 | Module and functions lack explanatory docstrings. | Add concise module and function docstrings. |
| Side effect on import | Maintainability/testability | 44 | `main()` runs whenever the module is imported. | Use an `if __name__ == "__main__":` guard. |
| No quantity validation | Robustness | 9–13 | Zero or negative quantities can be recorded. | Reject non-positive quantities and add a database `CHECK` constraint. |
| Long lines and spacing | Style | 5, 11, 12, 32 | Lines exceed configured limits and `order_total+=quantity` lacks operator spacing. | Wrap statements and use conventional spacing. |
