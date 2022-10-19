SELECT
	customer_state,
	COUNT(DISTINCT customer_id) AS distinct_customers,
	COUNT(customer_unique_id) AS distinct_auto_customers
FROM customer 
GROUP BY 1
ORDER BY 2 DESC;

SELECT
	product_id,
	product_category_name,
	product_height_cm,
	product_length_cm,
	product_width_cm,
	product_weight_g,
	(product_height_cm * product_length_cm * product_width_cm) AS volume_cm3,
	CASE 
		WHEN LOWER(product_category_name) = 'perfumaria' THEN 'store'
		ELSE 'website'
	END AS source,
	CASE 
		WHEN product_height_cm < 10 THEN 'small'
		WHEN product_height_cm BETWEEN 10 AND 15 THEN 'medium'
		ELSE 'large'
	END product_size
FROM products
WHERE LOWER(product_category_name) IN ('perfumaria', 'artes')
AND product_weight_g >= 1000
ORDER BY 6 DESC; 

SELECT 
	product_category_name,
	CASE 
		WHEN product_height_cm < 10 THEN 'small'
		WHEN product_height_cm BETWEEN 10 AND 15 THEN 'medium'
		ELSE 'large'
	END product_size,
	COUNT(DISTINCT product_id) AS distinct_products
FROM products
WHERE product_category_name IS NOT NULL
GROUP BY 1,2
ORDER BY 3 DESC;

SELECT
	oi.product_id,
	o.customer_id,
	o.order_purchase_timestamp,
	o.order_delivered_customer_date, 
	oi.price AS product_price,
	oi.freight_value,
	(oi.price + oi.freight_value) AS total_price
FROM orders o
LEFT JOIN order_items oi WHERE o.order_id = oi.order_id; 