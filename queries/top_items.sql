-- Itens mais vendidos (por quantidade)
SELECT p.name AS product, SUM(oi.qty) AS total_qty
FROM Products p
JOIN OrderItems oi ON oi.product_id = p.id
GROUP BY p.id
ORDER BY total_qty DESC
LIMIT 10;
