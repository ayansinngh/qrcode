# QR Code Generator

A lightweight web application built with **Python and Flask** that generates downloadable QR codes from text, URLs, and contact details. It features a simple interface, customizable QR code sizes, and instant generation without page reloads.

## 🚀 Live Demo

**[Try the QR Code Generator](https://vercel.com/ayansinnghs-projects/qrcode)**

## ✨ Features

- **Text QR Codes** — Convert plain text into scannable QR codes.
- **URL QR Codes** — Generate QR codes for website links and web addresses.
- **Contact QR Codes** — Create vCard QR codes containing contact information.
- **Adjustable Size** — Choose QR code dimensions from 128 to 1024 pixels.
- **Instant Generation** — Generate QR codes without reloading the page.
- **PNG Download** — Download generated QR codes as PNG images.
- **Server-Side Validation** — Display clear error messages for invalid or missing inputs.
- **REST API** — Generate QR codes programmatically using a JSON request.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **QR Code Generation:** Python QR code library
- **Frontend:** HTML5, CSS3, JavaScript
- **Image Format:** PNG
- **Data Format:** JSON
- **Deployment:** Vercel

## 📁 Project Structure

```text
qr-code-generator/
├── app.py                  # Flask routes and QR generation
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Application interface
└── static/
    ├── css/
    │   └── style.css       # Application styling
    └── js/
        └── app.js          # Client-side interactions
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip
- Git (optional)

### 1. Clone the repository

```bash
git clone https://github.com/ayansinnghs/qrcode.git
cd qrcode
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Linux / macOS**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open the local URL displayed in your terminal, typically:

```text
http://127.0.0.1:5000
```

## 🔌 API Documentation

### Generate a QR Code

**Endpoint:** `/api/generate`

**Method:** `POST`

**Content-Type:** `application/json`

### Request Examples

#### 1. Generate a QR code from text

```json
{
  "type": "text",
  "content": "Hello, World!",
  "size": 320
}
```

#### 2. Generate a QR code from a URL

```json
{
  "type": "url",
  "content": "example.com",
  "size": 320
}
```

#### 3. Generate a QR code from contact details

```json
{
  "type": "contact",
  "contact": {
    "name": "Ayan Singh",
    "phone": "+911234567890",
    "email": "ayan@example.com",
    "organization": "Example Organization"
  },
  "size": 320
}
```

### Successful Response

The API returns the generated QR code as a Base64-encoded PNG image.

```json
{
  "image": "data:image/png;base64,...",
  "size": 320
}
```

### Error Response

Invalid requests return an error message.

```json
{
  "error": "Invalid input"
}
```

*The exact error message and HTTP status code depend on the server-side validation implemented in `app.py`.*

## 💡 How It Works

1. Enter text, a URL, or contact details.
2. Select the desired QR code size.
3. Submit the form to generate the QR code.
4. The frontend sends a request to the Flask API using JavaScript.
5. The server validates the input and generates a QR code.
6. Preview and download the resulting PNG image.

## 🎯 Project Goals

This project demonstrates practical skills in:

- Python application development
- Flask routing and backend validation
- REST API design and JSON handling
- Frontend and backend integration
- JavaScript asynchronous requests
- Image generation and Base64 encoding
- Project organization and deployment

## 🔮 Future Improvements

- Add custom QR code colors and backgrounds.
- Support logo placement in QR codes.
- Add error correction level selection.
- Generate SVG QR codes.
- Add batch QR code generation.
- Improve accessibility and mobile responsiveness.

## 👨‍💻 Author

**Ayan Singh**

- GitHub: [@ayansinnghs](https://github.com/ayansinnghs)
- Live Project: [QR Code Generator](https://vercel.com/ayansinnghs-projects/qrcode)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub!
