import requests
import os
import time
from datetime import datetime, timezone

GREEN = '\x1b[92m'
YELLOW = '\x1b[93m'
CYAN = '\x1b[96m'
RED = '\x1b[91m'
RESET = '\x1b[0m'

BANNER = r"""
___  ____            _____                 
|  \/  (_)          /  ___|                
| .  . |_ _ __   ___\ `--.  ___ __ _ _ __  
| |\/| | | '_ \ / _ \`--. \/ __/ _` | '_ \ 
| |  | | | | | |  __/\__/ / (_| (_| | | | |
\_|  |_/_|_| |_|\___\____/ \___\__,_|_| |_|
    Minecraft Server OSINT - mine-scan
"""

# api url
api_url = "https://mcapi.shit.vc"

# Functions clears console
def clear_console():
	os.system('cls' if os.name == 'nt' else 'clear')

# GET + JSON helper for errors
def fetch_json(url, params=None):
	try:
		r = requests.get(url, params=params, timeout=10)
		r.raise_for_status()
		return r.json()
	except requests.exceptions.HTTPError as e:
		print(f"API HTTP Error: {e}")
	except requests.exceptions.RequestException:
		print("Network error. Check connection.")
	except ValueError:
		print("Invalid JSON response from API.")
	return {}


def format_ts(ts):
	if not ts:
		return ''
	try:
		if isinstance(ts, (int, float)):
			dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone()
		else:
			s = str(ts)
			if s.endswith('Z'):
				s = s[:-1] + '+00:00'
			dt = datetime.fromisoformat(s)
			if dt.tzinfo is None:
				dt = dt.replace(tzinfo=timezone.utc)
			dt = dt.astimezone()
		return dt.strftime('%Y-%m-%d %H:%M:%S %Z')
	except Exception:
		return str(ts)

# Searches for a specific player
def search_player(player_name):
	return fetch_json(f"{api_url}/whereis/{player_name}")

# Searches for data about an server from the api
def get_server_info(server_ip):
	return fetch_json(f"{api_url}/server/{server_ip}")

# Searches for data on what servers a player has been on
def get_server_players(server_ip):
	return fetch_json(f"{api_url}/who/{server_ip}")

# Gives random server
def get_random_server(count=1, version=None, min_players=0, software=None, country=None):
	params = {
		"count": count,
		"minPlayers": min_players,
	}
	if version:
		params["version"] = version
	if software:
		params["software"] = software
	if country:
		params["country"] = country
	return fetch_json(f"{api_url}/servers/random", params=params)

# Search for servers version, country, minimum players etc
def search_servers(version=None, software=None, authmode=None, min_players=0, country=None, sort=None, page=1, page_size=20):
	params = {
		"minPlayers": min_players,
		"page": page,
		"pageSize": page_size,
	}
	if version:
		params["version"] = version
	if software:
		params["software"] = software
	if authmode:
		params["authmode"] = authmode
	if country:
		params["country"] = country
	valid_sorts = ["lastseen", "players", "version"]
	if sort and sort.lower() in valid_sorts:
		params["sort"] = sort.lower()
	else:
		params["sort"] = "lastseen"
	response = fetch_json(f"{api_url}/servers", params=params)
	if not response:
		print("API Error: unable to reach API or bad response")
		return {}
	return response

# main loop
def main():
	while True:
		clear_console()
		print(CYAN + BANNER + RESET)
		menu = (
			f"{GREEN}1){RESET} Get server info\n"
			f"{GREEN}2){RESET} View indexed players for a server\n"
			f"{GREEN}3){RESET} Search for a player\n"
			f"{GREEN}4){RESET} Search database (advanced)\n"
			f"{GREEN}5){RESET} Get random server\n"
			f"{GREEN}6){RESET} Credits / About\n"
			f"{GREEN}q){RESET} Quit\n"
		)
		option = input(menu + f"{CYAN}Select option: {RESET}").strip()

		if option == '3':
			clear_console()
			print(f"{CYAN}=== Search for Player ==={RESET}")
			print("Find servers where a player has been seen.")
			print("Includes UUID, total servers found, first seen and last seen.\n")
			player_name = input("Enter player name: ").strip()
			data = search_player(player_name)
			uuid = data.get("uuid")
			name = data.get("name")
			total_servers = data.get("totalServers")
			first_seen = data.get("firstSeen")
			last_seen = data.get("lastSeen")
			first_seen = format_ts(first_seen)
			last_seen = format_ts(last_seen)
			print(f"\nPlayer: {name}")
			print(f"UUID: {uuid}")
			print(f"Total Servers Found: {total_servers}")
			print(f"First Seen: {first_seen}")
			print(f"Last Seen: {last_seen}")
			print("\nServers:")
			for server in data.get('servers', []):
				fs = format_ts(server.get('firstSeen'))
				ls = format_ts(server.get('lastSeen'))
				print(f"  - {server.get('ip')}:{server.get('port')}")
				print(f"    First Seen: {fs}")
				print(f"    Last Seen: {ls}")
			input("\nPress Enter to return to the main menu...")

		elif option == '1':
			clear_console()
			print(f"{CYAN}=== Get Server Information ==={RESET}")
			server_ip = input("Enter IP of the server: ").strip()
			data = get_server_info(server_ip)
			geo = data.get('geolocation', {})
			print(f"\nServer: {server_ip}")
			print(f" -Version: {data.get('version')}")
			print(f" -Software: {data.get('software')}")
			print(f" -Auth Mode: {data.get('authmode')}")
			print(f" -Last Seen: {format_ts(data.get('lastSeen'))}")
			print(f" -Country: {geo.get('country')}")
			input("\nPress Enter to return to the main menu...")

		elif option == '2':
			clear_console()
			print(f"{CYAN}=== View Indexed Players for a Server ==={RESET}")
			server_ip = input("Enter IP of the server: ").strip()
			data = get_server_players(server_ip)
			print(f"\nIndexed players for {server_ip}:\n")
			for player in data.get('players', []):
				print(f"  - {player.get('name')} (UUID: {player.get('uuid')})")
			input("\nPress Enter to return to the main menu...")

		elif option == '5':
			clear_console()
			print(f"{CYAN}=== Random Server Finder ==={RESET}")
			version = input("Version (leave blank for any): ").strip() or None
			country = input("Country (leave blank for any): ").strip() or None
			min_players = input("Minimum players (default 0): ").strip()
			min_players = int(min_players) if min_players else 0
			data = get_random_server(count=1, version=version, min_players=min_players, country=country)
			servers = data.get('servers', [])
			if not servers:
				print("No servers found with those filters.")
			else:
				s = servers[0]
				ip = s.get('serverip')
				ver = s.get('version') or s.get('rawVersion')
				players = s.get('onlinePlayers') if s.get('onlinePlayers') is not None else s.get('playersCount', 0)
				geo = s.get('geolocation', {}) or {}
				country_code = geo.get('country') or geo.get('countryName') or ''
				last = format_ts(s.get('lastSeen'))
				print(f"\nRandom Server: {ip} | {ver} | {players} players | {country_code} | lastSeen: {last}")
			input("\nPress Enter to return to the main menu...")

		elif option == '4':
			clear_console()
			print(f"{CYAN}=== Advanced Server Search ==={RESET}")
			version = input("Version (leave blank for any): ").strip() or None
			software = input("Software (leave blank for any): ").strip() or None
			authmode = input("Auth mode (online/offline/whitelist, leave blank for any): ").strip() or None
			country = input("Country (code or name, leave blank for any): ").strip() or None
			min_players = input("Minimum players (default 0): ").strip()
			min_players = int(min_players) if min_players else 0
			page = input("Page number (default 1): ").strip()
			page = int(page) if page else 1
			sort = input("Sort by (lastseen/players/version, default lastseen): ").strip() or None
			page_size = input("Page size (1-100, default 20): ").strip()
			page_size = int(page_size) if page_size else 20
			data = search_servers(version=version, software=software, authmode=authmode, min_players=min_players, country=country, sort=sort, page=page, page_size=page_size)
			servers = data.get('servers', [])[:page_size]
			if not servers:
				print("No servers found with those filters.")
			else:
				for server in servers:
					ip = server.get('serverip')
					ver = server.get('version') or server.get('rawVersion')
					soft = server.get('software')
					players = server.get('onlinePlayers') if server.get('onlinePlayers') is not None else server.get('playersCount', 0)
					geo = server.get('geolocation', {}) or {}
					country_code = geo.get('country') or geo.get('countryName') or ''
					last = format_ts(server.get('lastSeen'))
					print(f"  - {ip} | {ver} | {soft} | {players} players | {country_code} | lastSeen: {last}")
			input("\nPress Enter to return to the main menu...")

		elif option == '6':
			clear_console()
			print(f"{CYAN}=== Credits / About ==={RESET}")
			print(f"{YELLOW}Minecraft Server OSINT Tool{RESET}")
			print(f"{YELLOW}Created by: Reimo{RESET}")
			print(f"{YELLOW}Github: https://github.com/cqlnx/Minecraft-OSINT{RESET}")
			print(f"{YELLOW}API: https://mcapi.shit.vc{RESET}")
			input("\nPress Enter to return to the main menu...")
			
		elif option.lower() in ('q', 'quit', 'exit'):
			print(f"{RED}Exiting.{RESET}")
			break
		
		else:
			print("Invalid option. Please enter 1, 2, 3, 4 or q to quit.")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("\nExiting.")
