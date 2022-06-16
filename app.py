import imp
from flask import Flask, render_template, request
import flask_excel as excel
from datetime import datetime, timedelta
import json
import pymysql

from service import *
from helper import logging_ofac

app = Flask(__name__)
logger = logging_ofac()


@app.route('/')
def view_list():
    logger.info('View data!')

    latest_date = get_date()['max_date']
    last_week = latest_date - timedelta(days=7)
    return render_template("index.html", date=get_date(), order_no=get_orders(), list_match=get_match(),
                           disposition=get_dispositions(), ofac=view_data(from_date=last_week, to_date=latest_date))


@app.route('/filtered_list')
def filter_list():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    if request.args.get('action') == 'Run Report':
        logger.info('Filter data & Run report!')

        return render_template("index.html", date=get_date(), order_no=get_orders(), list_match=get_match(),
                            disposition=get_dispositions(), ofac=view_data(from_date=from_date, to_date=to_date))
    elif request.args.get('action') == 'Click here to download!':
        logger.info('Download CSV successfully!')

        final = download_data(from_date=from_date, to_date=to_date)
        final = [{'order_id': record['order_id'], 'cert_serial_number': record['cert_serial_number'],
                'disposition': record['disposition'], 'comment': record['comment']} for record in final]

        excel.init_excel(app)
        extension_type = "csv"
        filename = "ofactory_legal_disposition" + "." + extension_type
        return excel.make_response_from_records(final, file_type=extension_type, file_name=filename)


@app.route('/updating_list', methods=['POST'])
def updating_list():
    logger.info('Updating disposition & comment')
    return json.dumps({'status': 'OK'})


@app.route('/update_list', methods=['POST'])
def update_list():
    _created = datetime.now()
    order_id = request.form.get('order_id')
    cert_serial_number = request.form.get('cert_serial_number')
    disposition = request.form.get('disposition')
    comment = request.form.get('comment')

    logger.info(f"User submitted: '_created': {_created}, 'order_id': {order_id}, 'cert_serial_number': {cert_serial_number}, 'disposition': {disposition}, 'comment': {comment}")
    
    try:
        insert_db(_created, order_id, cert_serial_number , disposition, comment)
        logger.info(f'Insert order {order_id} to database successfully!')
    except pymysql.err.IntegrityError:        
        update_db(disposition, order_id)
        logger.error(f"pymysql.err.IntegrityError due to duplicate {order_id}!")
    except pymysql.err.DataError:
        logger.error("pymysql.err.DataError because x-editable call to ajax call!")
    return json.dumps({'status': 'OK'})


if __name__ == '__main__':
    app.run(debug=True)