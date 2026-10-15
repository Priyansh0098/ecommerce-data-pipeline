
-- 1. Total number of products
SELECT COUNT(*) AS total_products
FROM products;

-- 2. Check duplicate product IDs
SELECT id, COUNT(*) AS duplicate_count
FROM products
GROUP BY id
HAVING COUNT(*) > 1;

-- 3. Check missing required values
SELECT *
FROM products
WHERE id IS NULL
   OR title IS NULL
   OR price IS NULL
   OR category IS NULL;

-- 4. Check invalid prices
SELECT *
FROM products
WHERE price < 0;

-- 5. Check invalid ratings
SELECT *
FROM products
WHERE rating < 0 OR rating > 5;

-- 6. Count products by category
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
ORDER BY product_count DESC;
