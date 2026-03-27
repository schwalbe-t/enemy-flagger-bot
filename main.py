#!/usr/bin/python

import sys
sys.path.insert(0, "./deps")

from typing import Literal
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import time
import discord
from discord import app_commands


load_dotenv()

botToken = os.getenv("ENEMY_FLAGGER_BOT_TOKEN")
guildId = os.getenv("ENEMY_FLAGGER_GUILD_ID")


storage_path = Path("history.json")

def create_storage():
    print("Existing history not found - initializing empty history")
    return {}

def read_storage():
    print(f"Reading history fron '{storage_path}'")
    if not storage_path.exists() or not storage_path.is_file():
        return create_storage()
    try:
        return json.loads(storage_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return create_storage()

def write_storage(storage):
    print(f"Saving history to '{storage_path}'")
    serialized = json.dumps(storage, ensure_ascii=False, indent=4)
    storage_path.write_text(serialized, encoding="utf-8")

UserId = str
UserStatus = Literal["friend", "enemy", "neutral"]

def create_user_report(time: int, reporter_id: int, status: UserStatus):
    return {
        "time": time,
        "reporter_id": reporter_id,
        "status": status
    }

def create_user_data(history: list[UserReport] = []):
    return {
        "history": history
    }

def storage_get_user(storage, user_id):
    if user_id in storage:
        return storage[user_id]
    new_user = create_user_data()
    storage[user_id] = new_user
    return new_user

storage = read_storage()


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildId))
    print(f"Logged in as '{client.user}'")


@tree.command(
    name="flag",
    description="Flag a user as friendly or an enemy",
    guild=discord.Object(id=guildId)
)
async def flag(ctx, user: UserId, status: UserStatus):
    reporter_id = ctx.user.id
    now = int(time.time())
    user_data = storage_get_user(storage, user)
    user_data["history"].append(create_user_report(now, reporter_id, status))
    write_storage(storage)
    await ctx.response.send_message(f"Flagged user `{user}` as **{status}**.")
    pass

@tree.command(
    name="lookup",
    description="Look up the history of a user",
    guild=discord.Object(id=guildId)
)
async def lookup(ctx, user: UserId):
    user_data = storage_get_user(storage, user)
    user_reports = user_data["history"]
    if not user_reports:
        await ctx.response.send_message(
            f"User `{user}` has no recorded reports."
        )
        return
    result = ""
    result += f"### History of `{user}`:\n"
    result += "\n"
    last_report = user_reports[-1]
    result += f"Last flagged as **{last_report["status"]}** by <@{last_report["reporter_id"]}> (<t:{last_report["time"]}:R>).\n"
    result += "\n"
    report_counts: dict[str, int] = {
        "friend": 0,
        "neutral": 0,
        "enemy": 0
    }
    last_report_times: dict[str, int] = {
        "friend": 0,
        "neutral": 0,
        "enemy": 0
    }
    for report in user_reports:
        report_counts[report["status"]] += 1
        last_report_times[report["status"]] = max(
            last_report_times[report["status"]],
            report["time"]
        )
    result += f":green_circle: Friend: **{report_counts["friend"]}** time(s)"
    if last_report_times["friend"] != 0:
        result += f" (last <t:{last_report_times["friend"]}:R>)"
    result += "\n"
    result += f":yellow_circle: Neutral: **{report_counts["neutral"]}** time(s)"
    if last_report_times["neutral"] != 0:
        result += f" (last <t:{last_report_times["neutral"]}:R>)"
    result += "\n"
    result += f":red_circle: Enemy: **{report_counts["enemy"]}** time(s)"
    if last_report_times["enemy"] != 0:
        result += f" (last <t:{last_report_times["enemy"]}:R>)"
    result += "\n"
    await ctx.response.send_message(
        result,
        allowed_mentions=discord.AllowedMentions(users=[])
    )


if __name__ == "__main__":
    client.run(botToken)