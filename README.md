# discord_plexpi_bot
Discord Bot to automate torrent file download to plex server on raspberry pi
## Installation
Create an ``.env`` from the ``.env.example`` file and define the constance values. ``DISCORD_TOKEN`` is your Discord bot token.

Create a virtual environment (optional):
```bash
python -m venv venv
```

Activating the virtual environment:
```bash
source venv/bin/activate
```

Install requirements:
```bash
pip install -r requirements.txt
```

Update requirements after install a new lib:
```bash
pip freeze > requirements.txt
```

## Running the Bot
```bash
python bot.py
```