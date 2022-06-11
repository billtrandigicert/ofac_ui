from db import connect_db


def view_data(from_date, to_date):
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT _id, DATE(captured_date) AS captured_date, order_id, cert_serial_number, denied_persons_match AS order_person_name, bis_entity_match AS order_org_name, 
                       addresses_match AS order_address, alt_name_match AS order_common_name, `type` as flagged_field, sys_source, 
                       grey_list_match AS greylist_reason, grey_list_match_value AS greylist_match_value, max_match AS match_score, disposition
                FROM data_warehouse.ofactory_web
                WHERE DATE(captured_date) >= %s AND DATE(captured_date) <= %s AND disposition = 'greylist'
            ''', (from_date, to_date)
            )
            ofac = cursor.fetchall()
    return ofac


def get_date():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT MAX(DATE(captured_date)) AS max_date FROM data_warehouse.ofactory_web''')
            _date = cursor.fetchone()
    return _date


def get_orders():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT COUNT(order_id) AS count FROM data_warehouse.ofactory_web''')
            order_no = cursor.fetchone()
    return order_no


def get_match():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT COUNT(order_id) AS count FROM data_warehouse.ofactory_web 
                               WHERE disposition IN ('greylist', 'blacklist', 'whitelist')''')
            list_match = cursor.fetchone()
    return list_match


def get_dispositions():
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(''' WITH cte AS (
                                SELECT disposition, COUNT(order_id) AS count_
                                FROM data_warehouse.ofactory_web
                                GROUP BY disposition
                                )
                                SELECT disposition, count_, ROUND(count_ * 100 / t.s, 2) AS percentage
                                FROM cte
                                CROSS JOIN (SELECT SUM(count_) AS s FROM cte) t;''')
            result = cursor.fetchall()
    disposition = {item['disposition']: item['percentage'] for item in result}
    return disposition


def update_db(pk, value):
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE data_warehouse.ofactory_web SET disposition = %s WHERE _id = %s ", (value, pk))
            connection.commit()


