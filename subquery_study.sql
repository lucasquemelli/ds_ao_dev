--------------------------
-- Operações com SELECT --
--------------------------

SELECT 
	p.product_id, 
	p.product_category_name,
	p.product_height_cm,
	p.product_length_cm,
	p.product_weight_g,
	p.product_weight_g * p.product_length_cm * p.product_width_cm AS product_volume_cm³,
	CASE WHEN p.product_category_name = 'perfumaria' then 'loja' else 'website' END AS local_purchase,
	CASE WHEN p.product_height_cm < 10 THEN 'small'
		 WHEN p.product_height_cm >= 10 AND p.product_height_cm < 15 THEN 'medium'
		 WHEN p.product_height_cm >= 15 AND p.product_height_cm <= 20 THEN 'large' ELSE 'extra_large' END AS package		 
FROM products p 
WHERE (p.product_category_name = 'perfumaria' OR p.product_category_name = 'artes')
	   AND p.product_weight_g > 1000 ORDER BY p.product_weight_g DESC;
  
SELECT
	CASE WHEN p.product_height_cm < 10 THEN 'small'
		 WHEN p.product_height_cm >= 10 AND p.product_height_cm < 15 THEN 'medium'
		 WHEN p.product_height_cm >= 15 AND p.product_height_cm <= 20 THEN 'large' ELSE 'extra_large' END AS package,
	product_category_name,
	COUNT(product_id) AS num_products
FROM products p 
WHERE product_category_name != 'NULL'
GROUP BY product_category_name, package  
ORDER BY package DESC; 

SELECT 
	o.order_id,
	o.customer_id,
	p.product_category_name,
	s.seller_state,
	c.customer_state 
FROM orders o 
	INNER JOIN order_items oi    ON (oi.order_id = o.order_id)
	INNER JOIN products p        ON (p.product_id = oi.product_id)
	LEFT JOIN order_payments op  ON (op.order_id = o.order_id)
	LEFT JOIN customer c         ON (c.customer_id = o.customer_id)
	LEFT JOIN order_reviews or2  ON (or2.order_id = o.order_id)
	INNER JOIN sellers s         ON (s.seller_id = oi.seller_id)
	INNER JOIN geolocation g     ON (g.geolocation_zip_code_prefix = s.seller_zip_code_prefix)
LIMIT 10;

SELECT * FROM order_items oi LIMIT 10;

SELECT
	o.customer_id, 
	c.customer_state,
	COUNT(oi.product_id) AS num_products 
FROM orders o INNER JOIN order_items oi ON (oi.order_id = o.order_id)
			  INNER JOIN customer c     ON (c.customer_id = o.customer_id)
GROUP BY o.customer_id, c.customer_state 
ORDER BY num_products DESC;

WITH product_count AS (

	SELECT
		order_id, 
		COUNT(product_id) AS num_products 
	FROM order_items oi  
	GROUP BY order_id 
	ORDER BY 2 DESC
	
), order_customer AS (

	SELECT 
		order_id,
		customer_id
	FROM orders o
	
), customer_state AS (

	SELECT
		customer_id,
		customer_state
	FROM customer c 
	
)

SELECT
	cs.customer_id, 
	cs.customer_state, 
	pc.num_products  
FROM customer_state cs INNER JOIN order_customer oc ON (cs.customer_id  = oc.customer_id)
					   INNER JOIN product_count pc  ON (pc.order_id = oc.order_id)
ORDER BY pc.num_products DESC;
	  