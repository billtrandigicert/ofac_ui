from helper import connect_db


def view_data(from_date, to_date):
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT a._id, DATE(b.order_date) AS order_date, a.order_id, a.cert_serial_number, b.order_person_name, bis_entity_match AS order_org_name, 
                       addresses_match AS order_address, b.org_zip AS order_zip_code, b.order_email, alt_name_match AS order_common_name, 
                       `type` as flagged_field, a.sys_source, grey_list_match AS greylist_reason, grey_list_match_value 
                       AS greylist_match_value, max_match AS match_score, 
                       CASE WHEN (sdns > 0.28999999 or alt_name > 0.28999999 or addresses > 0.88999999 or denied_persons > 0.28999999) THEN 'greylist'
                       ELSE 'passed' END AS disposition
                FROM data_warehouse.ofactory_results a
                LEFT JOIN data_warehouse.orion_api_2d_orders b ON a.order_id = b.order_id AND a.cert_serial_number = b.serial_number 
                LEFT JOIN data_warehouse.ofactory_disposition c ON a.order_id = c.order_id AND a.cert_serial_number = c.cert_serial_number 
                WHERE c.disposition IS NULL AND DATE(order_date) >= %s AND DATE(order_date) <= %s
            ''', (from_date, to_date)
            )
            ofac = cursor.fetchall()
    return ofac


def get_date():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT MAX(DATE(order_date)) AS max_date FROM data_warehouse.ofactory_results a
                LEFT JOIN data_warehouse.orion_api_2d_orders b ON a.order_id = b. order_id AND a.cert_serial_number = b.serial_number''')
            _date = cursor.fetchone()
    return _date


def get_orders():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT COUNT(order_id) AS count FROM data_warehouse.ofactory_results''')
            order_no = cursor.fetchone()
    return order_no


def get_match():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT COUNT(order_id) AS count FROM data_warehouse.ofactory_disposition''')
            list_match = cursor.fetchone()
    return list_match


def get_dispositions():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' WITH cte AS (
                                SELECT disposition, COUNT(_id) AS count_
                                FROM data_warehouse.ofactory_disposition
                                GROUP BY disposition
                                )
                                SELECT disposition, count_, ROUND(count_ * 100 / t.s, 2) AS percentage
                                FROM cte
                                CROSS JOIN (SELECT SUM(count_) AS s FROM cte) t;''')
            result = cursor.fetchall()
    disposition = {item['disposition']: item['percentage'] for item in result}
    return disposition


def insert_db(_created, order_id, cert_serial_number , disposition, comment):
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO data_warehouse.ofactory_disposition (_created, order_id, cert_serial_number , disposition, comment)
                                VALUES (%s, %s, %s, %s, %s);''', (_created, order_id, cert_serial_number , disposition, comment))
            connection.commit()


def update_db(disposition, order_id):
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''UPDATE data_warehouse.ofactory_disposition SET disposition = %s WHERE order_id = %s;''', (disposition, order_id))
            connection.commit()


def download_data(from_date, to_date):
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT a.order_id, cert_serial_number, disposition, b.order_date, comment 
                FROM data_warehouse.ofactory_disposition a
                LEFT JOIN data_warehouse.orion_api_2d_orders b ON a.order_id = b. order_id AND a.cert_serial_number = b.serial_number 
                WHERE DATE(order_date) >= %s AND DATE(order_date) <= %s
            ''', (from_date, to_date)
            )
            final = cursor.fetchall()
    return final