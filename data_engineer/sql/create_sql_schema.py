import sqlite3
import os


DB_NAME = 'test.db'
target_path='.'
target_folder = os.path.abspath(target_path)
db_path = target_folder + os.path.sep + DB_NAME

customer_list = [[1,'aa','ru'],[2,'bb','gb'],[3,'cc','ru']]
item_list = [[1,'itm1','item_1',10],[2,'itm2','item_2',20],[3,'itm3','item_3','15']]
order_list = [['2022-01-01',1, 2,10],['2022-02-02',2, 3,5],['2022-03-03',2, 1,10],['2022-03-11',3, 1,10]]
country_list = [['gb','england','gb38'],['ru','rusia', 'rus'],['us','usa', 'usa1']]
connection_log_list = [['1','2022-01-01','2022-01-01'], ['2','2022-02-02','2022-03-03'],['3','2022-03-11','2022-03-11']]


#create cities dictionary from list (source: github, OpenWeatherMap.org)
con = sqlite3.connect(db_path)
cur = con.cursor()


# SQLite DB ddl schema
def create_db_sqlite(db_path):
    with open(db_path, 'w') as _:
        pass
    sql_ddl_customer = '''
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER NOT NULL,
        customer_name TEXT,
        country_code TEXT
    );
    '''
    sql_ddl_item = '''
        CREATE TABLE IF NOT EXISTS item (
        item_id INTEGER NOT NULL,
        item_name TEXT,
        item_description TEXT,
        item_price REAL
    );
    '''
    sql_ddl_orders = '''
        CREATE TABLE IF NOT EXISTS orders (
        date_time TEXT,
        item_id INTEGER,
        customer_id INTEGER,
        quantity REAL
    );
    '''
    sql_ddl_countries = '''
        CREATE TABLE IF NOT EXISTS countries (
        country_code TEXT,
        country_name TEXT,
        country_zone TEXT
    );
    '''
    sql_ddl_connection_log = '''
        CREATE TABLE IF NOT EXISTS connection_log (
        customer_id INTEGER,
        first_connection_time TEXT,
        last_connection_time TEXT
    );
    '''

    cur = con.cursor()
    cur.execute(sql_ddl_customer)
    cur.execute(sql_ddl_item)
    cur.execute(sql_ddl_orders)
    cur.execute(sql_ddl_countries)
    cur.execute(sql_ddl_connection_log)
    con.commit()
    con.close()

create_db_sqlite(db_path)
def populate_db_sqlite(db_path, customer_list, item_list, order_list, country_list, connection_log_list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executemany(
        'INSERT INTO customer (customer_id, customer_name, country_code) VALUES (?, ?, ?)',
        customer_list
        )
    conn.commit()
    cur.executemany(
        'INSERT INTO item (item_id, item_name, item_description, item_price) VALUES (?, ?, ?, ?)',
        item_list
        )
    conn.commit()
    cur.executemany(
        'INSERT INTO orders (date_time, item_id, customer_id, quantity) VALUES (?, ?, ?, ?)',
        order_list
        )
    conn.commit()
    cur.executemany(
        'INSERT INTO countries (country_code, country_name, country_zone) VALUES (?, ?, ?)',
        country_list
        )
    conn.commit()
    cur.executemany(
        'INSERT INTO connection_log (customer_id, first_connection_time, last_connection_time) VALUES (?, ?, ?)',
        connection_log_list
        )
    conn.commit()
    conn.close()
    print('Populated SQLite database')

populate_db_sqlite(db_path, customer_list, item_list, order_list, country_list, connection_log_list)