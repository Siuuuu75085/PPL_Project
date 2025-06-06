INSERT INTO customers (name) VALUES 
('Nguyen Van A'),
('Tran Thi B');

INSERT INTO orders (customer_id, total, discount_code) VALUES 
(1, 150.00, 'welcome'),
(2, 210.50, 'see you soon');

INSERT INTO order_items (order_id, product_name, quantity, price_per_unit) VALUES
(1, 'iPhone', 3, 10.00),
(1, 'laptop', 4, 5.00),
(2, 'tablet', 5, 7.00),
(2, 'watch', 2, 15.00);

SELECT 
    o.id AS order_id,
    c.name AS customer_name,
    o.total,
    o.discount_code,
    o.created_at,
    i.product_name,
    i.quantity,
    i.price_per_unit,
    (i.quantity * i.price_per_unit) AS subtotal
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items i ON o.id = i.order_id
ORDER BY o.created_at DESC;


SELECT SUM(total) AS total_revenue FROM orders;

SELECT 
    product_name,
    SUM(quantity) AS total_sold
FROM order_items
GROUP BY product_name
ORDER BY total_sold DESC
LIMIT 5;