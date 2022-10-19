-- 01. Quantos pedidos foram feitos para cada tipo de pagamento?

SELECT 
	payment_type,
	COUNT(DISTINCT order_id) AS distinct_orders
FROM order_payments 
GROUP BY 1
ORDER BY 2 DESC;

-- 02. Qual o número máximo e mínimo de parcelas nos pagamentos?

SELECT 
	MAX(payment_installments) max_division,
	MIN(payment_installments) min_division
FROM order_payments;

-- 03. Quais são os top 10 pedidos com os maiores valores?

SELECT 
	order_id,
	payment_value 
FROM order_payments
ORDER BY 2 DESC
LIMIT 10;

-- 04. Quais são os últimos 10 pedidos com os menores valores?

SELECT
	op.order_id,
	order_purchase_timestamp,
	op.payment_value 
FROM order_payments op 
INNER JOIN orders o ON op.order_id = o.order_id 
WHERE op.payment_value > 0
ORDER BY 3 ASC, 2 DESC
LIMIT 10;

-- 05. Qual a média do valor de pagamento por tipo de pagamento?

SELECT 
	payment_type,
	ROUND(AVG(payment_value), 2) AS avg_payment_value
FROM order_payments 
GROUP BY 1
ORDER BY 2 DESC;

-- 06. Quais os top 5 clientes com os maiores valores de pagamento no boleto?

SELECT 
	o.customer_id,
	op.payment_value
FROM order_payments op 
INNER JOIN orders o ON op.order_id = o.order_id 
WHERE LOWER(op.payment_type) = "boleto"
ORDER BY 2 DESC 
LIMIT 5;

-- 07. Quais os top 5 clientes com os maiores valores de pagamento no cartão de crédito?

SELECT 
	o.customer_id,
	op.payment_value
FROM order_payments op 
INNER JOIN orders o ON op.order_id = o.order_id 
WHERE LOWER(op.payment_type) = "credit_card"
ORDER BY 2 DESC 
LIMIT 5;
