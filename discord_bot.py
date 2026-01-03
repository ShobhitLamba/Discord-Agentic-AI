import discord
from discord import app_commands
from discord.ext import commands
import subprocess
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot setup - minimal intents for slash commands only
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Path to the Swift executable
SWIFT_EXECUTABLE = "./SetReminder"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="setreminder", description="Create a reminder in your macOS Calendar")
@app_commands.describe(
    title="Title of the reminder",
    date="Date in YYYY-MM-DD format",
    start_time="Start time in HH:MM format (24-hour)",
    end_time="End time in HH:MM format (24-hour)",
    description="Description of the reminder"
)
async def set_reminder(
    interaction: discord.Interaction,
    title: str,
    date: str,
    start_time: str,
    end_time: str,
    description: str
):
    """Set a reminder using the Swift Calendar integration"""
    print("[DEBUG] /setreminder command invoked")
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await interaction.response.send_message(
            "❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2026-01-15)",
            ephemeral=True
        )
        return
    
    # Validate time formats
    try:
        datetime.strptime(start_time, "%H:%M")
        datetime.strptime(end_time, "%H:%M")
    except ValueError:
        await interaction.response.send_message(
            "❌ Invalid time format. Please use HH:MM in 24-hour format (e.g., 14:30)",
            ephemeral=True
        )
        return
    

    # Defer the response since the FastAPI server might take a moment
    await interaction.response.defer()
    
    try:
        import requests
        print("[DEBUG] Sending POST to FastAPI /setreminder endpoint...")
        response = requests.post(
            "http://localhost:8000/setreminder",
            json={
                "title": title,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "description": description
            },
            timeout=3
        )
        print(f"[DEBUG] FastAPI response status: {response.status_code}")
        print(f"[DEBUG] FastAPI response body: {response.text}")
        
        data = response.json()
        if data.get("status") == "success":
            embed = discord.Embed(
                title="✅ Reminder Created",
                description=f"Your reminder has been added to your Calendar!",
                color=discord.Color.green()
            )
            embed.add_field(name="Title", value=title, inline=False)
            embed.add_field(name="Date", value=date, inline=True)
            embed.add_field(name="Time", value=f"{start_time} - {end_time}", inline=True)
            embed.add_field(name="Description", value=description, inline=False)
            embed.set_footer(text=f"Created by {interaction.user.display_name}")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                f"❌ Failed to create reminder:\n```{data.get('output', 'Unknown error')}```",
                ephemeral=True
            )

    except requests.Timeout:
        await interaction.followup.send(
            "❌ The calendar operation timed out. This may be due to:\n"
            "• Calendar access not granted to Terminal/IDE\n"
            "• Go to System Preferences → Security & Privacy → Privacy → Calendars\n"
            "• Add your Terminal or IDE to the allowed apps",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ An unexpected error occurred: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="reminderhelp", description="Get help on using the reminder bot")
async def reminder_help(interaction: discord.Interaction):
    """Show help information for the reminder bot"""
    
    embed = discord.Embed(
        title="📅 Reminder Bot Help",
        description="This bot creates reminders in your macOS Calendar app.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Command",
        value="`/setreminder`",
        inline=False
    )
    
    embed.add_field(
        name="Parameters",
        value=(
            "• **title**: Name of your reminder\n"
            "• **date**: Date in YYYY-MM-DD format\n"
            "• **start_time**: Start time in HH:MM (24-hour)\n"
            "• **end_time**: End time in HH:MM (24-hour)\n"
            "• **description**: Details about the reminder"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Example",
        value=(
            "```\n"
            "/setreminder\n"
            "title: Team Meeting\n"
            "date: 2026-01-15\n"
            "start_time: 14:00\n"
            "end_time: 15:00\n"
            "description: Discuss Q1 goals\n"
            "```"
        ),
        inline=False
    )
    
    embed.set_footer(text="Note: This bot requires macOS Calendar access")
    
    await interaction.response.send_message(embed=embed)

# Error handler for command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `/reminderhelp` for available commands.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")

# Run the bot
if __name__ == "__main__":
    import sys
    
    # Check for token
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN environment variable not set")
        print("\nTo set your token:")
        print("  export DISCORD_BOT_TOKEN='your-token-here'")
        print("\nOr create a .env file with:")
        print("  DISCORD_BOT_TOKEN=your-token-here")
        sys.exit(1)
    
    bot.run(TOKEN)
