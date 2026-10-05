# QR Code Generator

A small Flask web app that turns text, links, or contact details into a QR code you can download as a PNG.

## Features
- Text, link, and contact (vCard) QR codes
- Adjustable size (128-1024 px)
- Generates without reloading the page
- Validation on the server with clear error messages

## Setup
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Project layout
```
qr-code-generator/
├── app.py              # Flask routes, validation, QR generation
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## API
`POST /api/generate` with JSON like:
```json
{ "type": "url", "content": "example.com", "size": 320 }
```
`type` is `text`, `url`, or `contact` (contact sends a `contact` object with `name`, `phone`, `email`, `organization`).
Returns `{ "image": "data:image/png;base64,...", "size": 320 }` or `{ "error": "..." }`.
