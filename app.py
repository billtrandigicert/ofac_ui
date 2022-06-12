from crypt import methods
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


@app.route('/filtered_list', methods=["POST"])
def filter_list():
    from_date = request.form.get("from")
    to_date = request.form.get("to")
    if request.form['action'] == 'Run Report':
        return render_template("index.html", date=get_date(), order_no=get_orders(), list_match=get_match(),
                            disposition=get_dispositions(), ofac=view_data(from_date=from_date, to_date=to_date))
    elif request.form['action'] == 'Click here to download!':
        ofac = view_data(from_date=from_date, to_date=to_date)
        ofac = [{'order_id': record['order_id'], 'cert_serial_number': record['cert_serial_number'],
                'disposition': record['disposition']} for record in ofac]

        excel.init_excel(app)
        extension_type = "csv"
        filename = "ofactory_legal_disposition" + "." + extension_type
        return excel.make_response_from_records(ofac, file_type=extension_type, file_name=filename)


@app.route('/update_list', methods=['POST'])
def update_list():
    pk = request.form.get('pk')
    value = request.form.get('value')
    update_db(pk, value)
    return json.dumps({'status': 'OK'})


if __name__ == '__main__':
    app.run(debug=True)