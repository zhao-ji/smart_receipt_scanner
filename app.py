import os
from flask import Flask, request, jsonify, render_template
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
import json
import traceback
from pprint import pprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Azure Form Recognizer credentials
endpoint = os.getenv("AZURE_FORM_ENDPOINT")
key = os.getenv("AZURE_FORM_KEY")

# Initialize the Form Recognizer client
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_receipt():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Analyze the receipt
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-receipt", document=file
        )
        receipts = poller.result()

        if len(receipts.documents) == 0:
            return jsonify({'error': 'No receipt found in image'}), 400

        receipt = receipts.documents[0]
        receipt_dict = receipt.to_dict()
        fields = receipt_dict.get('fields', {})
        
        # Extract receipt information
        result = {
            'merchant_name': fields.get('MerchantName', {}).get('value') if 'MerchantName' in fields else None,
            'merchant_address': fields.get('MerchantAddress', {}).get('content') if 'MerchantAddress' in fields else None,
            'merchant_phone': fields.get('MerchantPhoneNumber', {}).get('value') if 'MerchantPhoneNumber' in fields else None,
            'transaction_date': fields.get('TransactionDate', {}).get('content') if 'TransactionDate' in fields else None,
            'transaction_time': fields.get('TransactionTime', {}).get('content') if 'TransactionTime' in fields else None,
            'receipt_number': fields.get('ReceiptNumber', {}).get('value') if 'ReceiptNumber' in fields else None,
            'subtotal': float(fields.get('Subtotal', {}).get('value')) if 'Subtotal' in fields else None,
            'tax': float(fields.get('TotalTax', {}).get('value')) if 'TotalTax' in fields else None,
            'total': float(fields.get('Total', {}).get('value')) if 'Total' in fields else None,
            'payment_method': fields.get('PaymentMethod', {}).get('value') if 'PaymentMethod' in fields else None,
            'items': []
        }

        if 'Items' in fields:
            items = fields.get('Items', {}).get('value', [])
            for item in items:
                item = item.get('value', {})
                pprint(item)
                item_dict = {
                    'description': item.get('Description', {}).get('value') if 'Description' in item else None,
                    'amount': float(item.get('TotalPrice', {}).get('value')) if 'TotalPrice' in item else None
                }
                result['items'].append(item_dict)

        return jsonify(result)

    except Exception as e:
        error_traceback = traceback.format_exc()
        print(error_traceback)  # 打印到控制台
        return jsonify({
            'error': str(e),
            'traceback': error_traceback
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
