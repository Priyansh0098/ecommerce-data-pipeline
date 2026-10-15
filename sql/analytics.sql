
-- 1. Check total products
SELECT COUNT(*) AS total_products
FROM products;


-- 2. Find the 5 most expensive products
SELECT title, price, category
FROM products
ORDER BY price DESC
LIMIT 5;


-- 3. Category-wise product analysis
SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(price), 2) AS average_price,
    MAX(price) AS highest_price
FROM products
GROUP BY category
ORDER BY average_price DESC;


-- 4. Find highly rated products
SELECT
    title,
    rating,
    rating_count
FROM products
WHERE rating >= 4.5
ORDER BY rating DESC, rating_count DESC;


-- 5. Find products with prices above the overall average
SELECT title, price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
)
ORDER BY price DESC;


-- 6. Category-wise total catalog value
SELECT
    category,
    ROUND(SUM(price), 2) AS total_catalog_value
FROM products
GROUP BY category
ORDER BY total_catalog_value DESC;
