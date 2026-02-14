# Minecraft-OSINT

Minecraft-OSINT is a command-line OSINT tool for discovering and analyzing
public Minecraft servers.

It allows you to:

-   Retrieve server information (version, software, auth mode, geolocation)
-   View players that have been observed on a specific server
-   Track where a player has been seen (UUID, first/last seen, server history)
-   Perform advanced searches across indexed servers
-   Discover random servers with custom filters

## Demo

### Main Menu
<img width="695" height="299" alt="menu" src="https://github.com/user-attachments/assets/4122dc72-42dd-427b-bd3c-5b3bc11da2cc" />

### Player Search Example
![player-search](https://github.com/user-attachments/assets/81b0a7e8-9581-4836-98e2-d5fc05863d5c)


## Installation

``` bash
git clone https://github.com/cqlnx/Minecraft-OSINT.git
cd Minecraft-OSINT
pip install -r requirements.txt
python main.py
```

## About

MineScan is powered by its official backend API, which indexes publicly
accessible Minecraft server data.
The api can be found at mcapi.shit.vc

## Disclaimer

Data is collected from publicly accessible Minecraft servers and is
intended for research and educational purposes only.
