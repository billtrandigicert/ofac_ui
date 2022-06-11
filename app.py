from flask import Flask, render_template, request, Response
import flask_excel as excel
from datetime import timedelta
import json

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
    return render_template("index.html", date=get_date(), order_no=get_orders(), list_match=get_match(),
                           disposition=get_dispositions(), ofac=view_data(from_date=from_date, to_date=to_date))


@app.route('/update_list', methods=['POST'])
def update_list():
    pk = request.form['pk']
    value = request.form['value']
    update_db(pk, value)
    return json.dumps({'status': 'OK'})


@app.route('/download_csv')
def download_csv():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    ofac = view_data(from_date='2019-06-06', to_date='2022-06-07')
    ofac = [{'order_id': record['order_id'], 'cert_serial_number': record['cert_serial_number'],
             'disposition': record['disposition']} for record in ofac]

    excel.init_excel(app)
    extension_type = "csv"
    filename = "ofactory_legal_disposition" + "." + extension_type
    return excel.make_response_from_records(ofac, file_type=extension_type, file_name=filename)


if __name__ == '__main__':
    app.run(debug=True)