# Telegram Web to Telethon session

Script to convert telegram web session into Telethon string session. In order to use it you need to extract the dc[x]_auth_key from local storage.

It will generate a string session that you can use with telethon like this:
```python
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

session = StringSession("put your session here")
client = TelegramClient(session, "api_id", "api_hash")
```

<img src="https://i.imgur.com/p3VaxDW.png" alt="tool"/>
