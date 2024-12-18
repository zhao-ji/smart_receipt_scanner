# Smart Receipt Scanner

A web application that uses Azure Form Recognizer to extract information from receipt images.

## Features

- Upload and analyze receipt images
- Extract key information including:
  - Merchant details (name, address, phone)
  - Transaction details (date, time, receipt number)
  - Item details and prices
  - Tax and total amounts
- Modern, responsive UI
- Real-time processing

## Prerequisites

- Python 3.x
- Azure Form Recognizer API credentials

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd smart_receipts
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Azure credentials:
```
AZURE_FORM_ENDPOINT=your_endpoint_here
AZURE_FORM_KEY=your_key_here
```

## Running the Application

1. Activate the virtual environment if not already activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

- `GET /`: Main page with upload interface
- `POST /analyze`: Endpoint for receipt analysis
  - Accepts multipart form data with a 'file' field containing the receipt image
  - Returns JSON with extracted receipt information

## Development

The application is built with:
- Flask (Backend)
- Azure Form Recognizer (OCR and receipt analysis)
- TailwindCSS (Styling)
