# DiscBoard
A simple API Wrapper to create discord bot web panels

# Instalation
```
pip3 install -U DiscBoard
```

# Example Usage
```py
from PyBoard import Application, Guild, DashConfig

DashConfig["BOT_TOKEN"] = "Your bot token"

my_bot = Application()
print(my_bot.get_guilds)

my_guild = Guild(guild_id=123)
print(my_guild.get_channels)

```
