"""
Flask Encryption/Decryption App with Menu Navigation, Background, Centered Layout, Filename Preservation, and Fixed Exit
"""

from flask import Flask, request, render_template_string, send_file, redirect, url_for, flash
from io import BytesIO
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

# --- Crypto params ---
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LEN = 32
PBKDF2_ITERS = 100_000

# --- Utilities ---

def derive_key(password: str, salt: bytes = None):
    if salt is None:
        salt = get_random_bytes(SALT_SIZE)
    key = PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS)
    return key, salt

def encrypt_bytes(key: bytes, plaintext: bytes) -> bytes:
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + tag + ciphertext

def decrypt_bytes(key: bytes, data: bytes) -> bytes:
    nonce = data[:NONCE_SIZE]
    tag = data[NONCE_SIZE:NONCE_SIZE+16]
    ciphertext = data[NONCE_SIZE+16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

# --- New: Include filename in encrypted payload ---
def encrypt_with_password_and_filename(password: str, plaintext: bytes, filename: str) -> bytes:
    key, salt = derive_key(password)
    payload = encrypt_bytes(key, plaintext)
    fname_bytes = filename.encode("utf-8")
    fname_len = len(fname_bytes).to_bytes(2, "big")
    return salt + fname_len + fname_bytes + payload

def decrypt_with_password_and_filename(password: str, data: bytes):
    salt = data[:SALT_SIZE]
    fname_len = int.from_bytes(data[SALT_SIZE:SALT_SIZE+2], "big")
    fname_start = SALT_SIZE + 2
    fname_end = fname_start + fname_len
    filename = data[fname_start:fname_end].decode("utf-8")
    payload = data[fname_end:]
    key, _ = derive_key(password, salt)
    plaintext = decrypt_bytes(key, payload)
    return filename, plaintext

# --- Shared CSS template ---
STYLE = """
<style>
  body {
    background-image: url("{{ url_for('static', filename='background.jpg') }}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
    font-family: Arial, sans-serif;
    text-shadow: 1px 1px 2px black;
    padding: 20px;
  }
  .panel {
    background: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 10px;
    width: 60%;
    max-width: 600px;
    margin: 100px auto;
    text-align: center;
  }

  /* Buttons & links */
  a, button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.2s, box-shadow 0.2s;
    margin: 5px;
  }
  a:hover, button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 10px rgba(0,114,255,0.6);
  }

  /* Input fields */
  input[type=password],
  input[type=text],
  input[type=file],
  textarea {
    width: 80%;
    padding: 10px;
    margin: 8px 0;
    border: 2px solid #0072ff;
    border-radius: 8px;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 14px;
    outline: none;
    transition: border 0.3s, box-shadow 0.3s;
  }
  input[type=password]:focus,
  input[type=text]:focus,
  input[type=file]:focus,
  textarea:focus {
    border-color: #00c6ff;
    box-shadow: 0 0 8px #00c6ff;
  }
</style>
"""

# --- Templates ---

MAIN_MENU = STYLE + """
<div class="panel">
  <h2>Main Menu</h2>
  <ul style="list-style:none; padding:0;">
    <li><a href="{{ url_for('encryption_menu') }}">Encryption</a></li>
    <li><a href="{{ url_for('decryption_menu') }}">Decryption</a></li>
    <li>
      <form method="post" action="{{ url_for('exit_app') }}">
        
      </form>
    </li>
  </ul>
</div>
"""

ENCRYPTION_MENU = STYLE + """
<div class="panel">
  <h2>Encryption Menu</h2>
  <ul style="list-style:none; padding:0;">
    <li><a href="{{ url_for('encrypt_text_page') }}">Text Encryption</a></li>
    <li><a href="{{ url_for('encrypt_file_page') }}">File Encryption</a></li>
    <li><a href="{{ url_for('index') }}">Exit</a></li>
  </ul>
</div>
"""

ENCRYPT_TEXT_FORM = STYLE + """
<div class="panel">
<h2>Encrypt Text</h2>
<form method=post action="/encrypt_text">
  <p>
    Password: <input id="password" name=password type=password required>
    <div id="strength-bar" style="height:10px; width:100%; background:#333; border-radius:5px; margin-top:5px;">
      <div id="strength-fill" style="height:100%; width:0%; background:red; border-radius:5px;"></div>
    </div>
  </p>
  <p>
  <div style="display: flex; align-items: center; gap: 10px;">
    <textarea id="textInput" name=text rows=5 cols=60 required></textarea>
    <button type="button" id="micButton" style="
        border: none;
        background: #007BFF;
        color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 20px;
        cursor: pointer;">🎤</button>
  </div>
</p>
  <button type=submit>Encrypt & Download</button>
</form>
<br><a href="{{ url_for('encryption_menu') }}">Back</a>

<script>
function checkStrength(pw) {
  let strength = 0;
  if (pw.length >= 8) strength++;
  if (/[A-Z]/.test(pw)) strength++;
  if (/[0-9]/.test(pw)) strength++;
  if (/[^A-Za-z0-9]/.test(pw)) strength++;

  return strength;
}

document.getElementById("password").addEventListener("input", function() {
  const pw = this.value;
  const strength = checkStrength(pw);
  const fill = document.getElementById("strength-fill");

  let colors = ["red", "orange", "yellow", "limegreen", "green"];
  let widths = ["20%", "40%", "60%", "80%", "100%"];

  fill.style.width = widths[strength] || "0%";
  fill.style.background = colors[strength] || "red";

// 🎤 Voice input integration
if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert("❌ Speech Recognition is not supported in this browser. Use Chrome or Edge.");
} else {
    const micButton = document.getElementById("micButton");
    const textInput = document.getElementById("textInput");

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onstart = () => console.log("🎤 Recognition started");
    recognition.onspeechend = () => recognition.stop();
    recognition.onend = () => console.log("✅ Recognition stopped");

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log("You said:", transcript);
        textInput.value += " " + transcript;
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        alert("⚠️ Speech recognition error: " + event.error);
    };

    micButton.addEventListener("click", () => recognition.start());
}
});
</script>
</div>
"""

ENCRYPT_FILE_FORM = STYLE + """
<div class="panel">
<h2>Encrypt File</h2>
<form method=post action="/encrypt_file" enctype=multipart/form-data>
  <p>
    Password: <input id="file-password" name=password type=password required>
    <div id="file-strength-bar" style="height:10px; width:100%; background:#333; border-radius:5px; margin-top:5px;">
      <div id="file-strength-fill" style="height:100%; width:0%; background:red; border-radius:5px;"></div>
    </div>
  </p>
  <p>File: <input type=file name=file required></p>
  <button type=submit>Encrypt File & Download</button>
</form>
<br><a href="{{ url_for('encryption_menu') }}">Back</a>

<script>
function checkStrength(pw) {
  let strength = 0;
  if (pw.length >= 8) strength++;
  if (/[A-Z]/.test(pw)) strength++;
  if (/[0-9]/.test(pw)) strength++;
  if (/[^A-Za-z0-9]/.test(pw)) strength++;

  return strength;
}

document.getElementById("file-password").addEventListener("input", function() {
  const pw = this.value;
  const strength = checkStrength(pw);
  const fill = document.getElementById("file-strength-fill");

  let colors = ["red", "orange", "yellow", "limegreen", "green"];
  let widths = ["20%", "40%", "60%", "80%", "100%"];

  fill.style.width = widths[strength] || "0%";
  fill.style.background = colors[strength] || "red";

// 🎤 Voice input integration
if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert("❌ Speech Recognition is not supported in this browser. Use Chrome or Edge.");
} else {
    const micButton = document.getElementById("micButton");
    const textInput = document.getElementById("textInput");

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onstart = () => console.log("🎤 Recognition started");
    recognition.onspeechend = () => recognition.stop();
    recognition.onend = () => console.log("✅ Recognition stopped");

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log("You said:", transcript);
        textInput.value += " " + transcript;
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        alert("⚠️ Speech recognition error: " + event.error);
    };

    micButton.addEventListener("click", () => recognition.start());
}
});
</script>
</div>
"""

DECRYPT_FORM = STYLE + """
<div class="panel">
<h2>Decrypt File</h2>
<form method=post action="/decrypt" enctype=multipart/form-data>
  <p>Password: <input name=password type=password required></p>
  <p>Encrypted file: <input type=file name=file required></p>
  <button type=submit>Decrypt</button>
</form>
<br><a href="{{ url_for('index') }}">Back</a>
</div>
"""

# --- Routes ---

@app.route("/")
def index():
    return render_template_string(MAIN_MENU)

@app.route("/encryption")
def encryption_menu():
    return render_template_string(ENCRYPTION_MENU)

@app.route("/encryption/text")
def encrypt_text_page():
    return render_template_string(ENCRYPT_TEXT_FORM)

@app.route("/encryption/file")
def encrypt_file_page():
    return render_template_string(ENCRYPT_FILE_FORM)

@app.route("/decryption")
def decryption_menu():
    return render_template_string(DECRYPT_FORM)

@app.route("/encrypt_text", methods=['POST'])
def encrypt_text():
    password = request.form.get('password')
    text = request.form.get('text', '')
    if not password or not text:
        flash('Password and text are required.')
        return redirect(url_for('encrypt_text_page'))
    data = encrypt_with_password_and_filename(password, text.encode('utf-8'), "encrypted_text.txt")
    buf = BytesIO(data)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name='encrypted_text.bin')

@app.route("/encrypt_file", methods=['POST'])
def encrypt_file():
    password = request.form.get('password')
    up = request.files.get('file')
    if not password or not up:
        flash('Password and file are required.')
        return redirect(url_for('encrypt_file_page'))
    plaintext = up.read()
    data = encrypt_with_password_and_filename(password, plaintext, up.filename)
    out_name = f"{up.filename}.enc"
    buf = BytesIO(data)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=out_name)

@app.route("/decrypt", methods=['POST'])
def decrypt():
    password = request.form.get('password')
    up = request.files.get('file')
    if not password or not up:
        flash('Password and file are required.')
        return redirect(url_for('decryption_menu'))
    data = up.read()
    try:
        filename, plaintext = decrypt_with_password_and_filename(password, data)
    except Exception as e:
        flash('Decryption failed: ' + str(e))
        return redirect(url_for('decryption_menu'))

    buf = BytesIO(plaintext)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=filename)

@app.route("/exit", methods=["POST"])
def exit_app():
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if shutdown is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    shutdown()
    return "Application shutting down..."

if __name__ == '__main__':
    app.run(debug=True)
