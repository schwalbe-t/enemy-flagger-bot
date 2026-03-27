
### Description

A simple discord bot that allows users to be flagged as `enemy`, `neutral` or `friend`, which can later be looked up at any time.

---

### Dependencies

Run the following command to install the bot dependencies locally:

```
pip install -r requirements.txt -t deps
```

Installing the dependencies locally means that they will be cleanly removed when the bot is deleted.

---

### Bot Setup

1. Install the dependencies using the above command
2. Register your bot in the [Discord Developer Portal](https://discord.com/developers/applications) and get its bot token.
3. Enable Discord developer options
4. Copy the server ID of the server that the bot will be operating in.
5. Copy the channel ID of the text channel for the `flag`-command. 
6. Create a `.env`-file next to the `main.py`-file with the following contents:
```
ENEMY_FLAGGER_BOT_TOKEN=<BOT-TOKEN>
ENEMY_FLAGGER_GUILD_ID=<SERVER-ID>
ENEMY_FLAGGER_FLAG_CHANNEL_ID=<CHANNEL-ID>
```
5. Run the `main.py` (the bot will be online as long as the program is running)

---

### Bot Usage

- Use `/flag <user> <status>` to flag a user as `enemy`, `neutral` or `friend`.
- Use `/lookup <user>` to see previous reports of any given user.
