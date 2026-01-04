# Discord Apple Integrations Bot

A Discord bot that integrates with macOS Apple apps using slash commands:
- **Calendar**: Create reminders in your macOS Calendar app
- **Apple Music**: Search and open songs in Apple Music

## Features

- `/setreminder` - Create calendar events via Discord
- `/reminderhelp` - Get help on using the reminder command
- `/searchsong` - Search and open a song in Apple Music
- `/searchsonghelp` - Get help on using the searchsong command
- Calendar integration with macOS Calendar app
- Apple Music integration via URL scheme
- Beautiful embeds for confirmation messages
- Input validation for dates and times

## Prerequisites

1. **macOS** - Required for Calendar and Apple Music integration
2. **Python 3.8+**
3. **Swift compiler** (comes with Xcode)
4. **Discord Bot Token** - Create one at [Discord Developer Portal](https://discord.com/developers/applications)
5. **Apple Music** (optional) - For playing songs

## Setup Instructions

### 1. Compile the Swift Executables

First, compile the Swift code that handles Calendar and Apple Music operations:

```bash
swiftc SetReminder.swift -o SetReminder
swiftc SearchSong.swift -o SearchSong
```

This creates the `SetReminder` and `SearchSong` executables that the bot will use.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install discord.py python-dotenv fastapi uvicorn
```

### 3. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the bot token
6. Under "Privileged Gateway Intents", enable:
   - Message Content Intent (if needed)
   - Server Members Intent (optional)

### 4. Configure Bot Permissions

In the OAuth2 > URL Generator section:
- Select scopes: `bot` and `applications.commands`
- Select permissions: `Send Messages`, `Use Slash Commands`, `Embed Links`
- Copy the generated URL and use it to invite the bot to your server

### 5. Set Up Environment Variables

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit `.env` and add your bot token:

```
DISCORD_BOT_TOKEN=your-actual-token-here
```

Or export it directly:

```bash
export DISCORD_BOT_TOKEN='your-token-here'
```

### 6. Grant Calendar Access

When you first run the bot and create a reminder, macOS will ask for Calendar access. Make sure to grant permission in System Preferences > Security & Privacy > Privacy > Calendars.

## Running the Bot

### Start the FastAPI Server (Backend)

```bash
python3 fastapi_apple.py
```

or with uvicorn:

```bash
uvicorn fastapi_apple:app --reload
```

### Start the Discord Bot

In a separate terminal:

```bash
python3 discord_bot.py
```

You should see:
```
YourBotName#1234 has connected to Discord!
Synced 4 command(s)
```

## Usage

In Discord, use the slash commands:

### Create a Reminder

```
/setreminder
title: Team Meeting
date: 2026-01-15
start_time: 14:00
end_time: 15:00
description: Discuss Q1 goals and project timeline
```

### Search a Song in Apple Music

```
/searchsong
song: End of Beginning
artist: Djo
```

**Note**: The `/searchsong` command opens Apple Music with search results for the song. You'll need to manually click play on the desired track as Apple Music URL schemes don't support auto-play for streaming songs.

### Get Help

```
/reminderhelp
/searchsonghelp
```

## Date/Time Formats

- **Date**: `YYYY-MM-DD` (e.g., 2026-01-15)
- **Time**: `HH:MM` in 24-hour format (e.g., 14:00 for 2:00 PM)

## Troubleshooting

### Bot doesn't respond to commands
- Make sure slash commands are synced (wait a few minutes after bot starts)
- Check that the bot has proper permissions in your server
- Verify the bot token is correct

### "Calendar integration not available" error
- Ensure the Swift executable is compiled: `swiftc SetReminder.swift -o SetReminder`
- Check that `SetReminder` executable exists in the same directory
- Verify file permissions: `chmod +x SetReminder`

### "Access to calendar not granted" error
- Go to System Preferences > Security & Privacy > Privacy > Calendars
- Grant access to Terminal or your IDE

### "Search song operation timed out" error
- Ensure FastAPI server is running: `python3 fastapi_apple.py`
- Check that `SearchSong` executable exists and is compiled
- Verify Apple Music is installed

### Command not showing up
- Slash commands can take up to an hour to sync globally
- Try kicking and re-inviting the bot
- Use guild-specific sync for faster testing

## Project Structure

```
.
├── discord_bot.py        # Main Discord bot code
├── fastapi_apple.py      # FastAPI server for Apple integrations
├── SetReminder.swift     # Swift code for Calendar integration
├── SetReminder           # Compiled Swift executable for Calendar
├── SearchSong.swift      # Swift code for Apple Music search integration
├── SearchSong            # Compiled Swift executable for Apple Music
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

## Architecture

The bot uses a three-tier architecture:

1. **Discord Bot** (`discord_bot.py`) - Handles Discord slash commands and user interaction
2. **FastAPI Server** (`fastapi_apple.py`) - REST API that receives requests from Discord bot
3. **Swift Executables** (`SetReminder`, `PlaySong`) - Native macOS integration for Calendar and Apple Music

**Flow Example (SetReminder)**:
```
Discord /setreminder → discord_bot.py → FastAPI /setreminder → SetReminder executable → macOS Calendar
```

**Flow Example (SearchSong)**:
```
Discord /searchsong → discord_bot.py → FastAPI /searchsong → SearchSong executable → Apple Music (URL scheme)
```

## Notes

- This bot runs on the machine where you execute it (needs macOS for Calendar and Apple Music access)
- Reminders are created in the Calendar app of the machine running the bot
- Apple Music integration uses URL schemes to open search results (manual play required)
- Each server member can create reminders that appear in the bot host's Calendar
- Consider security implications if running in public servers

## License

MIT License - feel free to modify and use as needed.

