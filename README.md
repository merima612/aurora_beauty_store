# Aurora Beauty Store — SQLite Database Implementation & Reporting (Milestone 2, Task 4)

This repository contains the relational database schema, deterministic data seeding script, business SQL queries, KPI summary report, and execution screenshots for **Aurora Beauty Store** (`aurora_beauty.sqlite`).

---

## Project Structure

```text
aurora/
├── aurora_beauty.sqlite     # Populated SQLite database file
├── schema.sql               # Relational schema, primary/foreign keys, and CHECK constraints
├── seed.py                  # Deterministic Python seeding script (Sep–Nov 2026)
├── queries.sql              # Business queries linked to operational goals (G1–G3) and reporting
├── report.html              # HTML operational & KPI report
└── screenshots/             # Execution and verification screenshots
    ├── er_diagram.png
    ├── suppliers.png
    ├── employees.png
    ├── products.png
    ├── stock_entries.png
    ├── orders.png
    ├── order_items.png
    ├── seed_and_counts.png
    ├── queries_output.png
    └── reportView.png
Database Schema & Staff Allocation
The SQLite database implements 6 relational entities with foreign key constraints enforced (PRAGMA foreign_keys = ON):

Suppliers (supplierId PK)

Employees (employeeId PK)

Products (productId PK, supplierId FK)

Stock_Entries (entryId PK, supplierId FK, employeeId FK)

Orders (orderId PK, employeeId FK)

Order_Items (itemId PK, orderId FK, productId FK)

Staff Allocation (10 Employees — Owner Separate)
Aligned with Milestone 1, the Employees table contains 10 employees allocated as follows, while the Owner is separate from these 10 employees:

1 Store Manager (employeeId = 1)

3 Sales Assistants (employeeId = 2–4)

3 Inventory Staff (employeeId = 5–7)

3 Online Sales (employeeId = 8–10)

Data Generation Explanation
Synthetic operational data was generated deterministically using a Python script (seed.py) with a fixed seed (random.seed(42)) against the schema defined in schema.sql. The dataset spans three months (September – November 2026) and populates:

15 Suppliers

10 Employees (1 Store Manager, 3 Sales Assistants, 3 Inventory Staff, 3 Online Sales; Owner separate)

20 Products across Skincare, Haircare, and Makeup

15 Stock Entries across September–November 2026

210 Orders (Completed, Reserved, Pending, Cancelled, Lost - Out of Stock, and Lost - Delayed) across September–November 2026

260 Order Items, with Orders.total_amount automatically calculated from Order_Items (quantity * unit_price)

Business Queries (queries.sql)
Query 1 (G1 — Stock accuracy): Monthly count and lost revenue of orders with status 'Lost - Out of Stock' (COUNT + SUM).

Query 2 (G2 — Online response time): Monthly count of 'Online' orders lost due to delayed response ('Lost - Delayed') grouped by employee (JOIN + COUNT).

Query 3 (G3 — Complete reservations): Lists 'Reserved' orders and flags whether required customer details (customer_name, customer_phone, shipping_address) are Complete or Incomplete.

Query 4 (Multi-table join + aggregation): Total units sold and revenue (SUM) by supplier and product category across 4 joined tables (Order_Items, Orders, Products, Suppliers) for 'Completed' orders.
