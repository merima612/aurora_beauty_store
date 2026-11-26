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

-- QUERY 3 (G3 - Complete reservations): Check whether reserved orders are complete
SELECT
    o.orderId,
    o.order_number,
    o.order_datetime,
    o.customer_name,
    o.customer_phone,
    o.pickup_deadline,
    o.total_amount,
    CASE
        WHEN NULLIF(TRIM(o.customer_name), '') IS NULL
          OR NULLIF(TRIM(o.customer_phone), '') IS NULL
          OR DATETIME(o.pickup_deadline) IS NULL
          OR NOT EXISTS (
              SELECT 1
              FROM Order_Items AS oi
              JOIN Products AS p ON p.productId = oi.productId
              WHERE oi.orderId = o.orderId
                AND oi.quantity > 0
          )
        THEN 'Incomplete'
        ELSE 'Complete'
    END AS reservation_status
FROM Orders AS o
WHERE o.status = 'Reserved'
ORDER BY o.order_datetime DESC;

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