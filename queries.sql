-- QUERY 1 (G1 - Stock accuracy): Lost orders due to stockouts by month (COUNT + SUM)
SELECT
    strftime('%Y-%m', order_datetime) AS order_month,
    COUNT(*) AS lost_out_of_stock_count,
    ROUND(SUM(total_amount), 2) AS lost_revenue_km
FROM Orders
WHERE status = 'Lost - Out of Stock'
GROUP BY strftime('%Y-%m', order_datetime)
ORDER BY order_month;

-- QUERY 2 (G2 - Online response time): Lost online orders due to delayed response by employee (JOIN + COUNT)
SELECT
    strftime('%Y-%m', o.order_datetime) AS order_month,
    e.full_name AS employee_name,
    e.role,
    COUNT(*) AS delayed_lost_orders
FROM Orders o
JOIN Employees e ON o.employeeId = e.employeeId
WHERE o.order_type = 'Online'
  AND o.status = 'Lost - Delayed'
GROUP BY strftime('%Y-%m', o.order_datetime), e.employeeId, e.full_name, e.role
ORDER BY order_month, delayed_lost_orders DESC;

-- QUERY 3 (G3 - Complete reservations): Reserved orders and completeness check of required customer details
SELECT
    orderId,
    order_number,
    order_datetime,
    customer_name,
    customer_phone,
    shipping_address,
    total_amount,
    CASE
        WHEN customer_name IS NULL OR TRIM(customer_name) = ''
          OR customer_phone IS NULL OR TRIM(customer_phone) = ''
          OR shipping_address IS NULL OR TRIM(shipping_address) = ''
        THEN 'Incomplete'
        ELSE 'Complete'
    END AS reservation_status
FROM Orders
WHERE status = 'Reserved'
ORDER BY order_datetime DESC;

-- QUERY 4 (3+ tables + SUM): Total units sold and revenue by supplier and category for completed orders
SELECT
    s.company_name AS supplier_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue_km
FROM Order_Items oi
JOIN Orders o ON oi.orderId = o.orderId
JOIN Products p ON oi.productId = p.productId
JOIN Suppliers s ON p.supplierId = s.supplierId
WHERE o.status = 'Completed'
GROUP BY s.supplierId, s.company_name, p.category
ORDER BY revenue_km DESC;