-- 1. Quantos pedidos foram feitos para cada tipo de pagamento?

SELECT 
	payment_type,
	COUNT(DISTINCT order_id) AS distinct_orders
FROM order_payments 
GROUP BY 1
ORDER BY 2 DESC;

-- 2. Qual o n�mero m�ximo e m�nimo de parcelas nos pagamentos?

SELECT 
	MAX(payment_installments) max_division,
	MIN(payment_installments) min_division
FROM order_payments;

-- 3. Quais s�o os top 10 pedidos com os maiores valores?

SELECT 
	order_id,
	payment_value 
FROM order_payments
ORDER BY 2 DESC
LIMIT 10;

