"""
QR Code Generator - Flask backend.

Run with:  python app.py
Then open http://127.0.0.1:5000 in your browser.
"""
import base64
import io
from urllib.parse import urlparse

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.exceptions import DataOverflowError
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Limits so nobody can accidentally (or on purpose) make the server choke
MIN_SIZE = 128
MAX_SIZE = 1024
MAX_TEXT_LENGTH = 1000


class ValidationError(Exception):
    """Raised when the user's input isn't something we can encode."""


def clean_url(raw):
    """Add https:// if the user forgot it, then make sure it looks like a real URL."""
    url = raw.strip()
    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or "." not in parsed.netloc:
        raise ValidationError("That doesn't look like a valid web address.")
    return url


def escape_vcard(value):
    """vCard fields need a few characters escaped or scanners get confused."""
    return (
        value.replace("\\", "\\\\")
        .replace(",", "\\,")
        .replace(";", "\\;")
        .replace("\n", "\\n")
    )


def build_vcard(contact):
    """Turn the contact form fields into a vCard 3.0 string."""
    name = (contact.get("name") or "").strip()
    phone = (contact.get("phone") or "").strip()
    email = (contact.get("email") or "").strip()

    if not name:
        raise ValidationError("Please enter a name for the contact.")
    if not phone and not email:
        raise ValidationError("Add at least a phone number or an email.")
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        raise ValidationError("That email address doesn't look right.")

    lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{escape_vcard(name)}"]
    if phone:
        lines.append(f"TEL:{escape_vcard(phone)}")
    if email:
        lines.append(f"EMAIL:{escape_vcard(email)}")

    org = (contact.get("organization") or "").strip()
    if org:
        lines.append(f"ORG:{escape_vcard(org)}")

    lines.append("END:VCARD")
    return "\n".join(lines)


def get_payload(data):
    """Work out what text should actually go inside the QR code."""
    kind = data.get("type", "text")

    if kind == "contact":
        return build_vcard(data.get("contact") or {})

    content = (data.get("content") or "").strip()
    if not content:
        raise ValidationError("Type something to encode first.")
    if len(content) > MAX_TEXT_LENGTH:
        raise ValidationError(f"That's too long. Keep it under {MAX_TEXT_LENGTH} characters.")

    if kind == "url":
        return clean_url(content)
    if kind == "text":
        return content

    raise ValidationError("Unknown content type.")


def make_qr_png(payload, size):
    """Create the QR code and return it as PNG bytes at the requested pixel size."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    # NEAREST keeps the edges crisp, which matters for scanning
    image = image.resize((size, size), resample=0)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


@app.route("/")
def index():
    return render_template("index.html", min_size=MIN_SIZE, max_size=MAX_SIZE)


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Something went wrong with the request."), 400

    # Size might come through as a string, so be forgiving
    try:
        size = int(data.get("size", 320))
    except (TypeError, ValueError):
        return jsonify(error="Size must be a number."), 400
    size = max(MIN_SIZE, min(MAX_SIZE, size))

    try:
        payload = get_payload(data)
        png_bytes = make_qr_png(payload, size)
    except ValidationError as err:
        return jsonify(error=str(err)), 400
    except DataOverflowError:
        return jsonify(error="There's too much data to fit in one QR code."), 400

    encoded = base64.b64encode(png_bytes).decode("ascii")
    return jsonify(image=f"data:image/png;base64,{encoded}", size=size)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
