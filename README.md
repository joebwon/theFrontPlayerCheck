This just notifies a discord channel on player/join leaves.

I really wanted to see VAC bans so I'd know to look out for player's who had recent bans, and I thought it was cool to log player join/leaves.

Anyway I'm not going with this for now, but thought it'd be cool to share anyway, so enjoy if it's useful.

Feel free to submit PRs or shoot me discord PMs for improvements, I'll try to keep it updated.

# Requirements:
python3


A steam API key (https://steamcommunity.com/dev/apikey)

A discord webhook (https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

# Installation Instructions (Ubuntu/Debian)

Note: Things may vary depending on your setup, but I've done my best.

## 1. Install Git (if not already installed)
Open a terminal and update your package list:

`sudo apt update`


Install Git:
`sudo apt install git`

## 2. Clone the Repository
`git clone https://github.com/joebwon/theFrontPlayerCheck.git`

Change to the cloned directory:
`cd theFrontPlayerCheck`

## 3. Install Python3 and Pip (if not already installed)
Most Ubuntu versions come with Python3 pre-installed, but it can be installed with:
`sudo apt install python3`

Install Pip for Python3:
`sudo apt install python3-pip`

## 4. Install Python Dependencies
`pip install -r requirements.txt`

## 5. Configure the .env File
Use your favorite editor to edit .env:
nano .env
or
vim.tiny .env

Replace the variables with your actual values:
```
DISCORD_WEBHOOK="https://discord.com/api/webhooks/yourwebhook"
STEAM_API_KEY=YOUR_STEAM_API_KEY
LOG_FILE_PATH="/path/to/ProjectWar.log"
```

Save and close the file (in nano, press CTRL + X, then Y, and Enter, in vim.tiny type : then wq then enter).

## 6. Running the Script
Ensure the script has execute permissions:
`chmod +x /path/to/theFrontPlayerCheck.py`

Run the script:
`python3 /path/to/theFrontPlayerCheck.py`
