PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Stock_Entries;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Suppliers;

CREATE TABLE Suppliers (
    supplierId INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE Employees (
    employeeId INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('Store Manager', 'Sales Assistant', 'Inventory Staff', 'Online Sales')),
    salary REAL NOT NULL CHECK (salary > 0)
);

CREATE TABLE Products (
    productId INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT NOT NULL UNIQUE,
    brand TEXT NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Skincare', 'Haircare', 'Makeup')),
    supplierId INTEGER NOT NULL,
    purchase_price REAL NOT NULL CHECK (purchase_price >= 0),
    selling_price REAL NOT NULL CHECK (selling_price >= 0),
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    expiration_date TEXT NOT NULL,
    FOREIGN KEY (supplierId) REFERENCES Suppliers(supplierId)
);

CREATE TABLE Stock_Entries (
    entryId INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT NOT NULL UNIQUE,
    entry_date TEXT NOT NULL,
    total_amount REAL NOT NULL CHECK (total_amount >= 0),
    supplierId INTEGER NOT NULL,
    employeeId INTEGER NOT NULL,
    FOREIGN KEY (supplierId) REFERENCES Suppliers(supplierId),
    FOREIGN KEY (employeeId) REFERENCES Employees(employeeId)
);

CREATE TABLE Orders (
    orderId INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT NOT NULL UNIQUE,
    order_type TEXT NOT NULL CHECK (order_type IN ('In-Store', 'Online')),
    employeeId INTEGER NOT NULL,
    order_datetime TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('Cash', 'Card', 'Cash on Delivery')),
    total_amount REAL NOT NULL CHECK (total_amount >= 0),
    status TEXT NOT NULL CHECK (status IN (
        'Completed',
        'Reserved',
        'Pending',
        'Cancelled',
        'Lost - Out of Stock',
        'Lost - Delayed'
    )),
    customer_name TEXT,
    customer_phone TEXT,
    shipping_address TEXT,
    FOREIGN KEY (employeeId) REFERENCES Employees(employeeId)
);

CREATE TABLE Order_Items (
    itemId INTEGER PRIMARY KEY AUTOINCREMENT,
    orderId INTEGER NOT NULL,
    productId INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    FOREIGN KEY (orderId) REFERENCES Orders(orderId),
    FOREIGN KEY (productId) REFERENCES Products(productId)
);