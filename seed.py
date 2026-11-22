import random
import sqlite3
from datetime import datetime, timedelta

random.seed(42)

conn = sqlite3.connect("aurora_beauty.sqlite")
cur = conn.cursor()

# Temporarily disable foreign keys while dropping/recreating tables, then re-enable before inserts
cur.execute("PRAGMA foreign_keys = OFF;")
with open("schema.sql", "r", encoding="utf-8") as f:
    for stmt in f.read().split(";"):
        stmt = stmt.strip()
        if stmt and not stmt.upper().startswith("PRAGMA"):
            cur.execute(stmt)
conn.commit()
cur.execute("PRAGMA foreign_keys = ON;")

# 1. Suppliers (15 rows)
suppliers = [
    ("AuraCosmetics d.o.o.", "+387 33 210-101", "orders@auracosmetics.ba"),
    ("DermMedika Sarajevo", "+387 33 210-102", "nabavka@dermmedika.ba"),
    ("GlamourDistribucija", "+387 33 210-103", "info@glamourdist.ba"),
    ("BalkanBeauty Wholesale", "+387 33 210-104", "sales@balkanbeauty.ba"),
    ("PureSkin Lab d.o.o.", "+387 33 210-105", "contact@pureskin.ba"),
    ("HairCare Pro BiH", "+387 33 210-106", "prodaja@haircarepro.ba"),
    ("VelvetMakeup Export", "+387 33 210-107", "orders@velvetmakeup.ba"),
    ("NaturaBotanica d.o.o.", "+387 33 210-108", "hello@naturabotanica.ba"),
    ("AdriaCosmo Partner", "+387 33 210-109", "b2b@adriacosmo.ba"),
    ("LumiGlow d.o.o.", "+387 33 210-110", "supply@lumiglow.ba"),
    ("PrestigeParfumerie", "+387 33 210-111", "orders@prestigeparf.ba"),
    ("BioDerma Trade BiH", "+387 33 210-112", "info@biodermatrade.ba"),
    ("SalonChoice d.o.o.", "+387 33 210-113", "sales@salonchoice.ba"),
    ("EssenceLine BiH", "+387 33 210-114", "support@essenceline.ba"),
    ("SilkTouch Cosmetics", "+387 33 210-115", "orders@silktouch.ba"),
]
cur.executemany(
    "INSERT INTO Suppliers (company_name, phone, email) VALUES (?, ?, ?)",
    suppliers,
)

# 2. Employees (10 employees — aligned with Milestone 1)
employees = [
    ("Amra Hodžić", "Store Manager", 1900.0),      # ID 1
    ("Lejla Kovačević", "Sales Assistant", 1250.0),  # ID 2
    ("Emina Delić", "Sales Assistant", 1250.0),      # ID 3
    ("Sara Begić", "Sales Assistant", 1250.0),       # ID 4
    ("Nermina Ramić", "Inventory Staff", 1300.0),    # ID 5
    ("Ajla Mujić", "Inventory Staff", 1300.0),       # ID 6
    ("Dina Softić", "Inventory Staff", 1300.0),      # ID 7
    ("Maja Karić", "Online Sales", 1300.0),          # ID 8
    ("Hana Omerović", "Online Sales", 1300.0),       # ID 9
    ("Tara Hadžić", "Online Sales", 1300.0),         # ID 10
]
cur.executemany(
    "INSERT INTO Employees (full_name, role, salary) VALUES (?, ?, ?)",
    employees,
)

# 3. Products (20 rows)
products_data = [
    ("387010010001", "CeraVe", "Hydrating Cleanser 236ml", "Skincare", 1, 14.50, 22.90, 28, "2027-11-30"),
    ("387010010002", "La Roche-Posay", "Cicaplast Baume B5+ 40ml", "Skincare", 2, 16.00, 25.50, 4, "2027-09-15"),
    ("387010010003", "The Ordinary", "Niacinamide 10% + Zinc 30ml", "Skincare", 5, 9.20, 15.90, 32, "2027-08-20"),
    ("387010010004", "Garnier", "Micellar Cleansing Water 400ml", "Skincare", 8, 6.50, 11.50, 40, "2028-01-10"),
    ("387010010005", "La Roche-Posay", "Anthelios UVMune SPF50+ 50ml", "Skincare", 12, 21.00, 33.90, 6, "2027-06-30"),
    ("387010010006", "The Ordinary", "Hyaluronic Acid 2% + B5 30ml", "Skincare", 5, 10.50, 17.50, 24, "2027-10-05"),
    ("387010010007", "L'Oreal", "Elseve Bond Repair Shampoo", "Haircare", 6, 11.00, 17.90, 19, "2028-02-15"),
    ("387010010008", "Moroccanoil", "Argan Hair Treatment 25ml", "Haircare", 13, 22.00, 34.50, 5, "2027-12-01"),
    ("387010010009", "Kérastase", "Nutritive Nectar Thermique", "Haircare", 6, 35.00, 54.00, 11, "2027-07-25"),
    ("387010010010", "Garnier", "Fructis Hair Food Papaya", "Haircare", 8, 7.80, 12.90, 27, "2028-03-12"),
    ("387010010011", "SalonChoice", "Keratin Silk Leave-In Spray", "Haircare", 13, 12.40, 19.90, 16, "2027-09-18"),
    ("387010010012", "SilkTouch", "Rosemary Scalp Oil 60ml", "Haircare", 15, 8.90, 14.90, 22, "2027-11-11"),
    ("387010010013", "Maybelline", "Lash Sensational Mascara", "Makeup", 3, 10.20, 16.90, 35, "2027-08-30"),
    ("387010010014", "Maybelline", "Fit Me Matte Foundation 30ml", "Makeup", 3, 11.50, 18.50, 8, "2027-10-22"),
    ("387010010015", "L'Oreal", "Infallible 24H Fresh Wear", "Makeup", 7, 15.00, 24.50, 17, "2027-12-19"),
    ("387010010016", "EssenceLine", "Velvet Lip Tint Mauve", "Makeup", 14, 4.20, 7.50, 45, "2028-04-01"),
    ("387010010017", "VelvetMakeup", "Cream Blush Petal Glow", "Makeup", 7, 7.60, 12.90, 3, "2027-09-05"),
    ("387010010018", "LumiGlow", "Dewy Setting Mist 100ml", "Makeup", 10, 9.80, 16.50, 20, "2027-11-28"),
    ("387010010019", "GlamourDist", "Precision Brow Pencil", "Makeup", 3, 5.40, 9.50, 29, "2028-01-20"),
    ("387010010020", "PrestigeParf", "Soft Matte Lip Liner", "Makeup", 11, 4.80, 8.90, 18, "2027-12-30"),
]
cur.executemany(
    """INSERT INTO Products
       (barcode, brand, name, category, supplierId, purchase_price, selling_price, stock_quantity, expiration_date)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    products_data,
)

# 4. Stock_Entries (15 rows across 3 months: Sep, Oct, Nov 2026)
start_date = datetime(2026, 9, 1, 9, 30)
for i in range(1, 16):
    entry_dt = (start_date + timedelta(days=i * 5)).strftime("%Y-%m-%d")
    inv_num = f"INV-2026-{200 + i}"
    total_inv = round(random.uniform(520.0, 1950.0), 2)
    sup_id = ((i - 1) % 15) + 1
    emp_id = random.choice([5, 6, 7])  # Inventory Staff (IDs 5-7)
    cur.execute(
        """INSERT INTO Stock_Entries (invoice_number, entry_date, total_amount, supplierId, employeeId)
           VALUES (?, ?, ?, ?, ?)""",
        (inv_num, entry_dt, total_inv, sup_id, emp_id),
    )

# 5. Orders (210 rows across September, October, and November 2026)
statuses_pool = (
    ["Completed"] * 145
    + ["Reserved"] * 22
    + ["Pending"] * 12
    + ["Cancelled"] * 15
    + ["Lost - Out of Stock"] * 7
    + ["Lost - Delayed"] * 9
)
random.shuffle(statuses_pool)

payments = ["Cash", "Card", "Cash on Delivery"]
customers = [
    ("Merima K.", "+387 61 234-501", "Grbavička 12, Sarajevo"),
    ("Aida S.", "+387 62 345-602", "Zmaja od Bosne 44, Sarajevo"),
    ("Belma H.", "+387 61 456-703", "Ferhadija 19, Sarajevo"),
    ("Lejla M.", "+387 63 567-804", "Maršala Tita 8, Sarajevo"),
    ("Dženita O.", "+387 61 678-905", "Ilidža centar 5, Sarajevo"),
    ("Ena B.", "+387 62 789-006", "Titova 31, Sarajevo"),
]

for i in range(1, 211):
    dt = start_date + timedelta(hours=i * 9)
    status = statuses_pool[i - 1]
    order_type = "Online" if (status == "Lost - Delayed" or i % 2 == 0) else "In-Store"
    emp_id = random.choice([8, 9, 10]) if order_type == "Online" else random.choice([2, 3, 4])
    payment = "Cash on Delivery" if order_type == "Online" else random.choice(["Cash", "Card"])

    if order_type == "Online" or status == "Reserved":
        cname, cphone, caddr = customers[i % len(customers)]
        addr = "Store Pickup" if (order_type == "In-Store" and status == "Reserved") else caddr
    else:
        cname, cphone, addr = None, None, None

    cur.execute(
        """INSERT INTO Orders
           (order_number, order_type, employeeId, order_datetime, payment_method,
            total_amount, status, customer_name, customer_phone, shipping_address)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            f"ORD-2026-{1000 + i}",
            order_type,
            emp_id,
            dt.strftime("%Y-%m-%d %H:%M:%S"),
            payment,
            0.0,
            status,
            cname,
            cphone,
            addr,
        ),
    )

# 6. Order_Items (260 rows)
for j in range(1, 261):
    order_id = (j % 210) + 1
    prod_id = random.randint(1, 20)
    qty = random.randint(1, 3)
    unit_price = cur.execute(
        "SELECT selling_price FROM Products WHERE productId = ?",
        (prod_id,),
    ).fetchone()[0]
    cur.execute(
        "INSERT INTO Order_Items (orderId, productId, quantity, unit_price) VALUES (?, ?, ?, ?)",
        (order_id, prod_id, qty, unit_price),
    )

cur.execute(
    """
    UPDATE Orders
    SET total_amount = COALESCE((
        SELECT ROUND(SUM(quantity * unit_price), 2)
        FROM Order_Items
        WHERE Order_Items.orderId = Orders.orderId
    ), 0.0)
    """
)

conn.commit()
conn.close()
print("Done! Created aurora_beauty.sqlite with 10 employees, 210 orders, and 260 order items.")