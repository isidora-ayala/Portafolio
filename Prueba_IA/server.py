import http.server
import json
import sqlite3
import os
import webbrowser
from urllib.parse import urlparse

PORT = 8080

BASE_DIR = os.path.dirname(__file__)
html_file = os.path.join(BASE_DIR, "prototipo_mcp.html")
DB_PATH = os.path.join(BASE_DIR, "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now', '-3 hours'))
    )""")
    conn.commit()
    conn.close()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/prototipo_mcp.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(html_file, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data) if post_data else {}

        parsed = urlparse(self.path)

        if parsed.path == "/api/register":
            self.handle_register(data)
        elif parsed.path == "/api/login":
            self.handle_login(data)
        elif parsed.path == "/api/forgot-password":
            self.handle_forgot(data)
        else:
            self.send_json({"error": "Ruta no encontrada"}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_register(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not name or not email or not password:
            self.send_json({"error": "Completa todos los campos."}, 400)
            return
        if "@" not in email or "." not in email:
            self.send_json({"error": "Ingresa un correo electronico valido."}, 400)
            return
        if len(password) < 6:
            self.send_json({"error": "La contrasena debe tener al menos 6 caracteres."}, 400)
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                      (name, email, password))
            conn.commit()
            self.send_json({"success": True, "name": name})
        except sqlite3.IntegrityError:
            self.send_json({"error": "Este correo ya esta registrado."}, 400)
        finally:
            conn.close()

    def handle_login(self, data):
        email = data.get("email", "").strip()
        password = data.get("password", "")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email = ? AND password = ?",
                  (email, password))
        row = c.fetchone()
        conn.close()

        if row:
            self.send_json({"success": True, "name": row[0]})
        else:
            self.send_json({"error": "Correo electronico o contrasena incorrectos."}, 401)

    def handle_forgot(self, data):
        email = data.get("email", "").strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email = ?", (email,))
        row = c.fetchone()
        conn.close()

        if row:
            self.send_json({"success": True, "name": row[0]})
        else:
            self.send_json({"error": "Este correo no esta registrado."}, 404)

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]} {args[2]}")

if __name__ == "__main__":
    init_db()

    print("=" * 50)
    print("  BancoEstado ChatBot - Servidor Local")
    print("=" * 50)
    print(f"  http://localhost:{PORT}")
    print(f"  http://127.0.0.1:{PORT}")
    print()

    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except:
        print(f"  Abre http://localhost:{PORT} en tu navegador")

    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()
