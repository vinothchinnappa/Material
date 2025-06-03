from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

@app.route('/process-csv', methods=['POST'])
def process_csv():
    file = request.files['file']
    df = pd.read_csv(BytesIO(file.read()))
    
    # Validate & Transform
    errors = []
    results = []
    
    for _, row in df.iterrows():
        try:
            quantity = int(row['Quantity'])
            if quantity < 0:
                raise ValueError("Negative quantity not allowed")

            date = datetime.strptime(row['Stock_Date'], "%Y-%m-%d")
            results.append({
                'material_code': row['Material_Code'],
                'material_name': row['Material_Name'],
                'category': row['Category'],
                'quantity': quantity,
                'unit': row['Unit'],
                'stock_date': date.strftime('%Y-%m-%d')
            })
        except Exception as e:
            errors.append({'row': row.to_dict(), 'error': str(e)})

    return jsonify({'valid_data': results, 'errors': errors})
