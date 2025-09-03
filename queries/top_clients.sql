-- Top 5 clientes por faturamento
SELECT c.name AS customer,
       ROUND(SUM(oi.qty * oi.unit_price), 2) AS revenue
FROM Customers c
JOIN Orders o ON o.customer_id = c.id
JOIN OrderItems oi ON oi.order_id = o.id
GROUP BY c.id
ORDER BY revenue DESC
LIMIT 5;
