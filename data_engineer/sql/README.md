# Тест SQL

На основе таблиц базы данных, напишите SQL код, который возвращает необходимые результаты
Пример: 

Общее количество товаров
```sql
select count (*) from items

```

## Структура данных

Используемый синтаксис: Oracle SQL или другой

| Сustomer       | Description           |
| -------------- | --------------------- |
| customer\_id   | customer unique id    |
| customer\_name | customer name         |
| country\_code  | country code ISO 3166 |

| Items             | Description       |
| ----------------- | ----------------- |
| item\_id          | item unique id    |
| item\_name        | item name         |
| item\_description | item description  |
| item\_price       | item price in USD |

| Orders       | Description                 |
| ------------ | --------------------------- |
| date\_time   | date and time of the orders |
| item\_id     | item unique id              |
| customer\_id | user unique id              |
| quantity     | number of items in order    |

| Countries     | Description           |
| ------------- | --------------------- |
| country\_code | country code          |
| country\_name | country name          |
| country\_zone | AMER, APJ, LATAM etc. |


| Сonnection\_log         | Description                           |
| ----------------------- | ------------------------------------- |
| customer\_id            | customer unique id                    |
| first\_connection\_time | date and time of the first connection |
| last\_connection\_time  | date and time of the last connection  |

## Задания

### 1) Общее количество покупателей


| **CustomerCountDistinct** |
| ----------------------------- |
| #                             |

```sql
select count (customer_id) from customer
```

### 2) Количество покупателей из Италии и Франции

| **Country_name** | **CustomerCountDistinct** |
| ------------------------- | ----------------------------- |
| France                    | #                             |
| Italy                     | #                             |

```sql
    select 
        countries.country_name,
        count(customer_id) CustomerCountDistinct
    from 
        customer,
        countries
    where 
        customer.country_code = countries.country_code
        and customer.country_code in ('FR', 'IT')
    GROUP BY
        countries.country_name;
```

### 3) ТОП 10 покупателей по расходам

| **Customer_name** | **Revenue** |
| ---------------------- | ----------- |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |

```sql
    select 
        customer.customer_name, (orders.quantity)*(item.item_price) revenue     
    from 
        customer,
        item,
        orders
    where 
        (customer.customer_id)= (orders.customer_id)
        and orders.item_id  = item.item_id
    GROUP BY customer.customer_id
    ORDER BY (orders.quantity)*(item.item_price) desc
    LIMIT 10;
```

### 4) Общая выручка USD по странам, если нет дохода, вернуть NULL

| **Country_name** | **RevenuePerCountry** |
| ------------------------- | --------------------- |
| Italy                     | #                     |
| France                    | NULL                  |
| Mexico                    | #                     |
| Germany                   | #                     |
| Tanzania                  | #                     |

```sql
        with rev_base as (select 
            customer.country_code, (orders.quantity)*(item.item_price) revenue     
        from 
            customer,
            item,
            orders
        where 
            (customer.customer_id)= (orders.customer_id)
            and orders.item_id  = item.item_id
        GROUP BY customer.country_code
        ORDER BY (orders.quantity)*(item.item_price) desc)
        SELECT countries.country_name, rev_base.revenue revenue_per_country
        from countries left join rev_base on (countries.country_code = rev_base.country_code)
        group by countries.country_name;
```

### 5) Самый дорогой товар, купленный одним покупателем

| **Customer\_id** | **Customer\_name** | **MostExpensiveItemName** |
| ---------------- | ------------------ | ------------------------- |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |

```sql
with cust_temp as 
    (select customer.customer_id,
        item.item_name, 
        max(item.item_price) over (PARTITION by customer.customer_id)
    FROM
        customer,
        item,
        orders
    where 
        item.item_id=orders.item_id
        and customer.customer_id=orders.customer_id
    GROUP BY 
        customer.customer_id)
    select 
        customer.customer_id, customer_name, cust_temp.item_name MostExpensiveItemName 
    from 
        customer,cust_temp
    where cust_temp.customer_id = customer.customer_id;
```

### 6) Ежемесячный доход

| **Month (MM format)** | **Total Revenue** |
| --------------------- | ----------------- |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
    select 
        substr(cast(orders.date_time as text),6,2) 'Month (MM format)',
        sum(orders.quantity*item.item_price) 'Total Revenue'
    FROM
        orders,
        item
    where
        orders.item_id = item.item_id
    group by
        substr(cast(orders.date_time as text),6,2)
    order by
        substr(cast(orders.date_time as text),6,2) ASC;
```

### 7) Общий доход в MENA

| **Total Revenue MENA** |
| ---------------------- |
| #                      |

```sql
    select
        sum(orders.quantity*item.item_price) 'Total Revenue MENA'
    FROM
        orders,
        item
    where
        orders.item_id = item.item_id;
```

### 8) Найти дубликаты

Во время передачи данных произошел сбой, в таблице orders появилось несколько 
дубликатов (несколько результатов возвращаются для date_time + customer_id + item_id). 
Вы должны их найти и вернуть количество дубликатов.

```sql
    --|| или concat(..)
    select
        orders.date_time||orders.customer_id||orders.item_id,
        count (orders.date_time||orders.customer_id||orders.item_id)
    FROM
        orders
    group by
        orders.date_time||orders.customer_id||orders.item_id
    having
        orders.date_time||orders.customer_id||orders.item_id >1;
```