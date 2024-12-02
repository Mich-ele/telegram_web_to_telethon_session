from telethon.sessions import StringSession
from telethon.sync import TelegramClient
import base64
import ipaddress
import struct
import asyncio

api_id = 0
api_hash = ""

tg_servers = {
    "dc1": "149.154.175.53",
    "dc2": "149.154.167.51",
    "dc3": "149.154.175.100",
    "dc4": "149.154.167.91",
    "dc5": "91.108.56.130"
}

def generate_string_session(dc_id, auth_key):
    server_address = tg_servers[f"dc{dc_id}"]
    port = 443
    _STRUCT_PREFORMAT = '>B{}sH256s'
    CURRENT_VERSION = '1'
    auth_key_bytes = bytes.fromhex(auth_key)
    ip_packed = ipaddress.ip_address(server_address).packed
    session_data = struct.pack(
        _STRUCT_PREFORMAT.format(len(ip_packed)),
        dc_id,
        ip_packed,
        port,
        auth_key_bytes
    )
    encoded_session = base64.urlsafe_b64encode(session_data).decode('ascii')
    return CURRENT_VERSION + encoded_session

async def get_full_name(session_string):
    try:
        session = StringSession(session_string)
        client = TelegramClient(session, api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
        else:
            me = await client.get_me()
            full_name = f"{me.first_name} {me.last_name}".strip() if me.last_name else me.first_name
            return full_name
    except:
        pass

async def main():
    print("[-] Enter DC Id: ", end="")
    dc_id = int(input().strip())
    print("[-] Enter DC Auth Key: ", end="")
    dc_auth_key = input().strip()
    
    session_string = generate_string_session(dc_id, dc_auth_key)
    full_name = await get_full_name(session_string)
    
    if full_name:
        print(f"\n[+] Session: {session_string}")
        print(f"[+] Full name: {full_name}")
    else:
        print("\n[!] Error - Invalid auth key")

if __name__ == "__main__":
    asyncio.run(main())
