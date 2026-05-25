import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# Configurações do Império
LOCAL_PORT = 8080
ELITE_FILE = "elite.txt"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_proxy()

    def do_POST(self):
        self.handle_proxy()

    def handle_proxy(self):
        try:
            # Carrega o Néctar fresco
            with open(ELITE_FILE, "r") as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            
            if not proxies:
                self.send_error(500, "Estoque de Néctar vazio. Rode o pro.py")
                return

            # Rotação Elite: Escolhe um IP aleatório da lista
            target_proxy = random.choice(proxies)
            proxy_dict = {"http": f"http://{target_proxy}", "https": f"http://{target_proxy}"}

            # Repassa a requisição
            response = requests.get(self.path, proxies=proxy_dict, stream=True, timeout=5)
            
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.content)
            print(f"[>] Roteado via: {target_proxy}")
            
        except Exception as e:
            self.send_error(502, f"Erro no túnel: {e}")

def run_central():
    print(f"[!] CENTRAL ATIVA: Porta {LOCAL_PORT} | Roteando Néctar...")
    server = HTTPServer(('127.0.0.1', LOCAL_PORT), ProxyHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_central()