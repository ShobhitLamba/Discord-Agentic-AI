# Discord Reminder Bot

A Discord bot that creates reminders in your macOS Calendar app using slash commands.

## Features

- `/setreminder` - Create calendar reminders via Discord
- `/reminderhelp` - Get help on using the bot
- Calendar integration with macOS Calendar app
- Beautiful embeds for confirmation messages
- Input validation for dates and times

## Prerequisites

1. **macOS** - Required for Calendar integration
2. **Python 3.8+**
3. **Swift compiler** (comes with Xcode)
4. **Discord Bot Token** - Create one at [Discord Developer Portal](https://discord.com/developers/applications)

## Setup Instructions

### 1. Compile the Swift Executable

First, compile the Swift code that handles Calendar operations:

```bash
swiftc SetReminder.swift -o SetReminder
```

This creates the `SetReminder` executable that the bot will use.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install discord.py python-dotenv
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

```bash
python discord_bot.py
```

You should see:
```
YourBotName#1234 has connected to Discord!
Synced 2 command(s)
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

### Get Help

```
/reminderhelp
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

### Command not showing up
- Slash commands can take up to an hour to sync globally
- Try kicking and re-inviting the bot
- Use guild-specific sync for faster testing

## Project Structure

```
.
├── discord_bot.py        # Main Discord bot code
├── SetReminder.swift     # Swift code for Calendar integration
├── SetReminder           # Compiled Swift executable
├── main.py              # Original FastAPI service (legacy)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .env.example         # Example environment file
└── README.md           # This file
```

## Migration from FastAPI

The bot replaces the FastAPI service with Discord slash commands:
- FastAPI POST `/set_reminder` → Discord `/setreminder` command
- Same Swift executable for Calendar integration
- Better user interface with Discord embeds
- Input validation and error handling

## Notes

- This bot runs on the machine where you execute it (needs macOS for Calendar access)
- Reminders are created in the Calendar app of the machine running the bot
- Each server member can create reminders that appear in the bot host's Calendar
- Consider security implications if running in public servers

## License

MIT License - feel free to modify and use as needed.
