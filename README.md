# From data science to development 

This repository contains the studies about *Data Science to Development* course.

# SQL - Structured English Query Language

This repository contains studies about SQLite using DBeaver. 

- Consultas:

![image](https://user-images.githubusercontent.com/81119854/152888624-25fbb9c9-b3e4-435a-a2f8-0796461c6441.png)

- Consulta dos 10 primeiros valores da tabela de produtos:

![image](https://user-images.githubusercontent.com/81119854/152889948-90cfcc8e-eae6-4335-8ee9-1944737efe16.png)

## Filtrando colunas

- Consultas dinâmicas:

![image](https://user-images.githubusercontent.com/81119854/152890837-626e6b4a-2caa-4dac-9134-56b0c90a34f2.png)

- Condicionais:

![image](https://user-images.githubusercontent.com/81119854/152894962-d401410e-5de4-4bb8-aaec-f4b1fc905eed.png)

- Sucessivas condições:

![image](https://user-images.githubusercontent.com/81119854/152895944-ff79791e-e5a2-49be-87f5-07502ffea3ef.png)

## Filtrando linhas

- Filtrando linhas

![image](https://user-images.githubusercontent.com/81119854/152896485-982d7324-b0f2-4d62-8ff2-629b96ed81e4.png)

- Filtrando linhas e ordenando por peso de forma crescente:

![image](https://user-images.githubusercontent.com/81119854/152899621-8342d8cd-67bf-41fb-a769-f55795c31a49.png)

- Filtrando linhas e ordenando por peso de forma decrescente:

![image](https://user-images.githubusercontent.com/81119854/152899824-6524b77d-5edb-4a4f-9063-07a8269644a4.png)

## Filtrando linhas e colunas

- Filtrando a quantidade de produtos a partir do número de identificação e agrupando por categoria:

![image](https://user-images.githubusercontent.com/81119854/152900443-0efcf6e0-2863-4cec-9e25-e91693e63227.png)

- Invertendo a ordem das colunas:

![image](https://user-images.githubusercontent.com/81119854/152900618-2eeded68-cd20-4f64-94f1-328f5d128ff1.png)

- Retirando a categoria 'NULL' da consulta:

![image](https://user-images.githubusercontent.com/81119854/152900839-8eff8694-0617-4767-9879-2a09a3c13696.png)

- Ordenando por número decrescente de produtos:

![image](https://user-images.githubusercontent.com/81119854/152901024-99e3d780-2783-42e9-8619-8e6c061f795c.png)

- Incluindo a coluna package:

![image](https://user-images.githubusercontent.com/81119854/152901552-62227036-46ff-4b24-bc8b-7df539b34660.png)

- Ordenando por categoria:

![image](https://user-images.githubusercontent.com/81119854/152901680-8237cda8-5754-46fb-b954-2c5f83c43247.png)

- Selecionando, agrupando e ordenando por package:

![image](https://user-images.githubusercontent.com/81119854/152901883-b2642107-e34e-477f-acb2-9465be8aa07c.png)

## Tipos de uniões no SQL

Nesta seção, nós estudamos operações dentro da clause FROM para uniões entre as tabelas.

![image](https://user-images.githubusercontent.com/81119854/152988214-93f652cf-233e-4372-8df1-c5bcd2fe1bb2.png)

Para utilizarmos os comandos JOIN, precisamos saber quais elementos (colunas) conectam as tabelas. Para isso, usamos o mapa das tabelas - que deve ser adquido por meio do gestor ou algum outra funcionário que administra o banco de dados que usarmos. Para o dataset com o qual estamos trabalhando, o mapa das tabelas é:

![image](https://user-images.githubusercontent.com/81119854/152991386-29624aa8-450d-478b-8157-d82ee3f48eb2.png)

- Unindo as tabelas *orders* com *order_items*:

![image](https://user-images.githubusercontent.com/81119854/153031244-43ae65b9-826f-41dd-86fe-9116cfe8eb18.png)

- Exibindo apenas as 10 primeiras linhas:

![image](https://user-images.githubusercontent.com/81119854/153031707-c1f8dc9f-177c-48f1-81c1-1c1f99baf8af.png)

- Exibindo as tabelas *orders*, *order_items* e *products*:

![image](https://user-images.githubusercontent.com/81119854/153032874-f046a468-ac09-4161-9796-64f3005cfa63.png)

Se houver items que não são comuns de todas as tabelas, mas que gostaríamos que aparecessem, devemos usar LEFT/RIGHT JOIN em vez de INNER JOIN.

- Exibindo as tabelas *orders*, *order_items*, *products* e *order_payments*:

![image](https://user-images.githubusercontent.com/81119854/153034217-7f8d394a-b609-4e04-958d-8ae5fc562d4a.png)

- Podem existir pedidos sem uma ordem de pagamento. Por isso, a query acima ficaria assim: 

![image](https://user-images.githubusercontent.com/81119854/153034736-41024e4f-ba19-4608-99ad-450ce84fecb1.png)

-  Exibindo as tabelas *orders*, *order_items*, *products*, *order_payments* e *customers*:

![image](https://user-images.githubusercontent.com/81119854/153035574-4fa875eb-4826-4b07-8a2e-5c5e0f4bedae.png)
