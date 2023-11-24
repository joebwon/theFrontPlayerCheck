#!/usr/bin/python3
import time
import re
import requests
from steam.webapi import WebAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get your steam API key from .env file
api_key = os.getenv('STEAM_API_KEY')
api = WebAPI(key=api_key)

# Get Discord webhook from .env file
webhook_url = os.getenv('DISCORD_WEBHOOK')


# Func to send to discord
def send_to_discord(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Error sending message to Discord: \
              {response.status_code} - {response.text}")


# Log watcher def
def watch_log_file(log_file_path):
    # This part starts the log at EOF, so we don't get dupes
    with open(log_file_path, 'r') as file:
        file_position = file.seek(0, 2)

    while True:
        with open(log_file_path, 'r') as file:
            file.seek(file_position)
            lines = file.readlines()
            file_position = file.tell()

        for line in lines:
            process_line(line)

        time.sleep(5)


# This defines what to look for in log entries
def process_line(line):
    # Check for join requests
    if 'Join request:' in line:
        join_match = re.search(r'\?ppid=(\d+)\?hn=[^?]+\?Name=([^?]+)', line)
        if join_match:
            steam_id, player_name = join_match.groups()
            process_join(steam_id, player_name)

    # Check for player leaving
    elif 'LogPlayer: player leave game' in line:
        leave_match = re.search(r'account=STEAM:(\d+)', line)
        if leave_match:
            steam_id = leave_match.group(1)
            process_leave(steam_id)


# Tattle tail when they join
def process_join(steam_id, player_name):
    try:
        response = api.call('ISteamUser.GetPlayerBans', steamids=steam_id)
        if response and 'players' in response:
            player_info = response['players'][0]
            log_message = (
                f"Player connected to The Front server Name: \
                    {player_name} "
                f"SteamID: {player_info['SteamId']} \
                    VacBanned: {player_info['VACBanned']} "
                f"NumberOfVACBans: \
                    {player_info['NumberOfVACBans']} "
                f"DaysSinceLastBan: \
                    {player_info['DaysSinceLastBan']} "
                f"NumberOfGameBans: \
                    {player_info['NumberOfGameBans']}"
            )
            log_to_file(log_message)
            send_to_discord(webhook_url, log_message)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player bans: {e}")


# Leave event isn't much because the log just gives us steam ID.
def process_leave(steam_id):
    leave_message = f"Player with ID {steam_id} has left the server"
    log_to_file(leave_message)
    send_to_discord(webhook_url, leave_message)


# Func to log the information to a file
def log_to_file(message, log_file='player_log.txt'):
    with open(log_file, 'a') as file:
        file.write(message + '\n')


# Replace this with your log file path
log_file_path = os.getenv('LOG_FILE_PATH')


# Start watching the log file
watch_log_file(log_file_path)
