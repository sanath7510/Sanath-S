
from flask import Flask, request
import hashlib, time, csv, os

app = Flask(__name__)

# ---------------- Blockchain Classes ----------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        record = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(record.encode()).hexdigest()

class Blockchain:
    def __init__(self, csv_file):
        self.chain = []
        self.csv_file = csv_file
        if os.path.exists(csv_file):
            self.load_chain()
        else:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis)
        self.save_chain()

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, prev_block.hash)
        self.chain.append(new_block)
        self.save_block(new_block)

    def save_block(self, block):
        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([block.index, block.timestamp, block.data, block.previous_hash, block.hash])

    def load_chain(self):
        if not os.path.exists(self.csv_file):
            return
        with open(self.csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) < 5:
                    continue
                index, timestamp, data, prev_hash, hash_val = row
                block = Block(int(index), float(timestamp), data, prev_hash)
                if block.hash != hash_val:
                    raise Exception("Blockchain integrity compromised!")
                self.chain.append(block)

    def save_chain(self):
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "Timestamp", "Data", "PrevHash", "Hash"])
            for block in self.chain:
                writer.writerow([block.index, block.timestamp, block.data, block.previous_hash, block.hash])

# Separate chains
patients_chain = Blockchain("patients_chain.csv")
staff_chain = Blockchain("staff_chain.csv")

# ---------------- Frontend ----------------

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>Hospital System</title>
        <style>
            body { font-family: Arial; text-align:center; padding:50px; }
            .btn { background: linear-gradient(45deg,#4facfe,#00f2fe); border:none; color:white;
                   padding:15px 30px; font-size:18px; border-radius:10px; margin:10px; cursor:pointer; }
            .btn:hover { transform:scale(1.05); opacity:0.9; }
        </style>
    </head>
    <body>
        <h1>Welcome to Hospital System</h1>
        <h3>Select your role:</h3>
        <a href="/role/patient"><button class="btn">Patient Login</button></a>
        <a href="/role/staff"><button class="btn">Staff Login</button></a>
    </body>
    </html>
    '''

@app.route('/role/<role>')
def role_menu(role):
    return f'''
    <html>
    <head>
        <title>{role.capitalize()} Portal</title>
        <style>
            body {{ font-family: Arial; text-align:center; padding:50px; }}
            .btn {{ background: linear-gradient(45deg,#43e97b,#38f9d7); border:none; color:white;
                   padding:15px 30px; font-size:18px; border-radius:10px; margin:10px; cursor:pointer; }}
            .btn:hover {{ transform:scale(1.05); opacity:0.9; }}
        </style>
    </head>
    <body>
        <h1>{role.capitalize()} Portal</h1>
        <h3>Choose an option:</h3>
        <a href="/register/{role}"><button class="btn">Register</button></a>
        <a href="/records/{role}"><button class="btn">Access Records</button></a>
        <br><br>
        <a href="/"><button class="btn">Back</button></a>
    </body>
    </html>
    '''

@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if request.method == 'POST':
        name = request.form.get("name")
        info = request.form.get("info")
        data = f"{role.capitalize()} Name: {name}, Info: {info}"
        if role == "patient":
            patients_chain.add_block(data)
        else:
            staff_chain.add_block(data)
        return f"<h2>{role.capitalize()} registered successfully!</h2><a href='/role/{role}'>Back</a>"
    return f'''
    <html><body style="text-align:center; font-family:Arial; padding:30px;">
    <h2>{role.capitalize()} Registration</h2>
    <form method="POST">
        Name: <input type="text" name="name"><br><br>
        Info: <input type="text" name="info"><br><br>
        <input type="submit" value="Register" class="btn">
    </form>
    <br><a href="/role/{role}"><button class="btn">Back</button></a>
    </body></html>
    '''

@app.route('/records/<role>')
def records(role):
    chain = patients_chain if role == "patient" else staff_chain
    rows = ""
    for block in chain.chain:
        rows += f"<tr><td>{block.index}</td><td>{time.ctime(block.timestamp)}</td><td>{block.data}</td><td>{block.previous_hash}</td><td>{block.hash}</td></tr>"
    return f'''
    <html><body style="font-family:Arial; padding:20px;">
    <h2>{role.capitalize()} Records</h2>
    <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>Index</th><th>Timestamp</th><th>Data</th><th>PrevHash</th><th>Hash</th></tr>
        {rows}
    </table>
    <br><a href="/role/{role}"><button class="btn">Back</button></a>
    </body></html>
    '''

if __name__ == "__main__":
    app.run(debug=True)
