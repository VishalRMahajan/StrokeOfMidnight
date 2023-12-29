import threading
import time
from flask import Flask, after_this_request, render_template, request, send_from_directory
import json
import csv
import os
from io import StringIO

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'json'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file and allowed_file(file.filename):
        json_data = file.read().decode('utf-8')
        csv_data = json_to_csv(json_data)

        # Save CSV file temporarily
        csv_filename = 'output.csv'
        csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)

        csv_data = json_to_csv(json_data)

        with open(csv_filepath, 'w', newline='') as csv_file:
            csv_file.write(csv_data)

        def delete_file():
            time.sleep(30)  # wait for 5 seconds
            os.remove(csv_filepath)

        threading.Thread(target=delete_file).start()
        
        return send_from_directory(app.config['UPLOAD_FOLDER'], csv_filename, as_attachment=True)

    else:
        return render_template('index.html', error='Invalid file format')
    
    

def json_to_csv(json_data):
    data = json.loads(json_data)

    if not data or not isinstance(data, list):
        return ''

    output = StringIO()
    csv_writer = csv.writer(output)

    # Write header
    headers = list(data[0].keys())
    csv_writer.writerow(headers)

    # Write data
    for row in data:
        row_values = [str(row.get(header, '')) for header in headers]
        csv_writer.writerow(row_values)

    return output.getvalue()


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
