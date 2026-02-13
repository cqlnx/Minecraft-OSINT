# Minecraft-OSINT

Minecraft-OSINT is a command-line OSINT tool for discovering and analyzing
public Minecraft servers.

It allows you to:

-   Retrieve server information (version, software, auth mode,
    geolocation)
-   View players that have been observed on a specific server
-   Track where a player has been seen (UUID, first/last seen, server history)
-   Perform advanced searches across indexed servers
-   Discover random servers with custom filters

## Installation

``` bash
git clone https://github.com/cqlnx/Minecraft-OSINT.git
cd mine-scan
pip install -r requirements.txt
python mine-scan.py
```

## About

MineScan is powered by its official backend API, which indexes publicly
accessible Minecraft server data.
The api can be found at mcapi.shit.vc

## Disclaimer

Data is collected from publicly accessible Minecraft servers and is
intended for research and educational purposes only.
