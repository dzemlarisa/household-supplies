-- 1. Выборка списка всех запасов с сортировкой (SELECT, ORDER BY)
SELECT id, name, quantity, unit FROM stocks ORDER BY name;

-- 2. Выборка всех пользователей (SELECT)
SELECT id, name, email FROM users;

-- 3. Фильтрация: поиск запасов в категории "продукты" (WHERE)
SELECT name, quantity, unit FROM stocks WHERE category_id = 1;

-- 4. Фильтрация: поиск запасов с количеством больше 1 (WHERE)
SELECT name, quantity FROM stocks WHERE quantity > 1.0;

-- 5. Соединение таблиц: запасы + название категории (JOIN)
SELECT stocks.name AS stock_name, categories.name AS category_name, stocks.quantity
FROM stocks
JOIN categories ON stocks.category_id = categories.id;

-- 6. Соединение таблиц: запасы + имя владельца (JOIN)
SELECT stocks.name AS stock_name, users.name AS owner_name
FROM stocks
JOIN users ON stocks.user_id = users.id;

-- 7. Агрегатная функция: общее количество запасов (COUNT)
SELECT COUNT(*) AS total_stocks FROM stocks;

-- 8. Агрегатная функция: суммарное количество всех запасов (SUM)
SELECT SUM(quantity) AS total_quantity FROM stocks;

-- 9. Группировка: сколько запасов в каждой категории (GROUP BY)
SELECT categories.name AS category_name, COUNT(stocks.id) AS stock_count
FROM categories
LEFT JOIN stocks ON categories.id = stocks.category_id
GROUP BY categories.name;

-- 10. Группировка + фильтрация групп: категории, где больше 1 запаса (HAVING)
SELECT categories.name AS category_name, COUNT(stocks.id) AS stock_count
FROM categories
JOIN stocks ON categories.id = stocks.category_id
GROUP BY categories.id, categories.name
HAVING COUNT(stocks.id) > 1;