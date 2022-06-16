from flask import Flask, render_template, request
import flask_excel as excel
from datetime import datetime, timedelta
import json
import pymysql

from service import *

app = Flask(__name__)


@app.route('/')
def view_list():
    latest_date = get_date()['max_date']
    last_week = latest_date - timedelta(days=7)
    return render_template("index.html", date=get_date(), order_no=get_orders(), list_match=get_match(),
                           disposition=get_dispositions(), ofac=view_data(from_date=last_week, to_date=latest_date))


@app.route('/filtered_list')
def filter_list():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    if request.args.get('action') == 'Run Report':
        return render_template("index.html", date=get_date(), order_no=get_orders(), list_match=get_match(),
                            disposition=get_dispositions(), ofac=view_data(from_date=from_date, to_date=to_date))
    elif request.args.get('action') == 'Click here to download!':
        final = download_data(from_date=from_date, to_date=to_date)
        final = [{'order_id': record['order_id'], 'cert_serial_number': record['cert_serial_number'],
                'disposition': record['disposition']} for record in final]

        excel.init_excel(app)
        extension_type = "csv"
        filename = "ofactory_legal_disposition" + "." + extension_type
        return excel.make_response_from_records(final, file_type=extension_type, file_name=filename)


@app.route('/updating_list', methods=['POST'])
def updating_list():
    print('updating disposition and comment')
    return json.dumps({'status': 'OK'})


@app.route('/update_list', methods=['POST'])
def update_list():
    print('successful!')
    _created = datetime.now()
    order_id = request.form.get('order_id')
    cert_serial_number = request.form.get('cert_serial_number')
    disposition = request.form.get('disposition')
    comment = request.form.get('comment')
    print({'_created': _created, 'order_id': order_id, 'cert_serial_number': cert_serial_number, 'disposition': disposition, 'comment': comment})
    
    try:
        insert_db(_created, order_id, cert_serial_number , disposition)
    except pymysql.err.IntegrityError:
        print("Order exists!")
        update_db(disposition, order_id)
    except pymysql.err.DataError:
        print('Why???')
    return json.dumps({'status': 'OK'})


if __name__ == '__main__':
    app.run(debug=True)