-- Pedidos possivelmente atrasados
SELECT o.id, c.name AS customer, o.order_date, o.expected_ship_date, o.actual_ship_date,
CASE
  WHEN o.actual_ship_date IS NULL AND julianday('now') - julianday(o.order_date) > 3 THEN 'maybe_delayed'
  WHEN o.actual_ship_date > o.expected_ship_date THEN 'delayed'
  ELSE 'on_time'
END AS status
FROM Orders o
JOIN Customers c ON c.id = o.customer_id;
