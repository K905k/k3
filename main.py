from os import system, name, path
from time import sleep
from random import choice
import asyncio
from base64 import b64decode

try:
    from requests import get
except ImportError:
    system('pip install requests')
    from requests import get

try:
    from telebot import TeleBot
except ImportError:
    system('pip install telebot')
    from telebot import TeleBot

try:
    from telethon import TelegramClient, sync, errors, functions, types
    from telethon.tl.functions.account import CheckUsernameRequest, UpdateUsernameRequest
    from telethon.tl.functions.channels import JoinChannelRequest
except ImportError:
    system('pip install telethon')
    from telethon import TelegramClient, sync, errors, types, functions
    from telethon.tl.functions.account import CheckUsernameRequest, UpdateUsernameRequest
    from telethon.tl.functions.channels import JoinChannelRequest

try:
    from bs4 import BeautifulSoup as S
except ImportError:
    system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup as S

try:
    from fake_useragent import UserAgent
except ImportError:
    system('pip install fake_useragent')
    from fake_useragent import UserAgent

try:
    from datetime import datetime
except ImportError:
    system('pip install datetime')
    from datetime import datetime

me = "@skrawi" 
tokenBot = "6688042392:AAHCEQ1s1BUms3vxFhgo9-jf7Vsl30qI9N0"
idx = "1958060577"

def clear():
    system('cls' if name == 'nt' else 'clear')

# for check flood , error
async def channels2(client, username):
    di = await client.get_dialogs()
    for chat in di:
        if chat.name == f'Claim [ {username} ]' and not chat.entity.username:
            await client(functions.channels.DeleteChannelRequest(channel=chat.entity))
            return False
    return True

async def fragment(username):
	try:
		response = get(url="https://guarded-shelf-02443-eee4640adcbd.herokuapp.com/c/username="+str(username)).json()["result"]
		if response == "is taken":
			return "is taken"
		elif response == True:
			return True
		else:
			return False
	except:
		sleep(5)
		await fragment(username=username)

async def telegram(client, claim, username):
    if claim:
        text = f"⌯ New UserName\n⌯ UserName : @{username} .\n⌯ Claim? {claim} .\n⌯ Source : {me} ."
        try:
            TeleBot(token=tokenBot).send_message(idx, text=text)
        except Exception:
            pass
    else:
        text = f"⌯ New UserName\n⌯ UserName : @{username} .\n⌯ Claim? {claim} .\n⌯ Source : {me} ."
    await client.send_message('me', text)

async def claimed(client, username):
    result = await client(functions.channels.CreateChannelRequest(
        title=f'Claim [ {username} ]',
        about=f'Source - {me}',
        megagroup=False))
    try:
        await client(functions.channels.UpdateUsernameRequest(
            channel=result.chats[0],
            username=username))
        sleep(0.50)
        await client.send_message(username, f'⌯ Done Save UserName .\n⌯ UserName : @{username} .\n⌯ Date : {datetime.now().strftime("%H:%M:%S")} .\n⌯ Source : {me} .')
        return True
    except Exception as e:
        await client.send_message('me', f'⌯ Error Message .\nMessage : {e} .')
        return False

# for checking username
async def checker(username, client):
    try:
        check = await client(CheckUsernameRequest(username=username))
        if check:
            print('- Available UserName : ' + username + ' .')
            claimer = await claimed(client, username)
            if claimer and await fragment(username) == "is taken":
                claim = True
            else:
                claim = False
            print('- Claimer ? ' + str(claim) + '\n' + '_ ' * 20)
            await telegram(client, claim, username)
            flood = await channels2(client, username)
            if not flood:
                with open('flood.txt', 'a') as floodX:
                    floodX.write(username + "\n")
                    TeleBot(tokenBot).send_message(chat_id=idx, text=f"⌯ New UserName Flood\n⌯ UserName : @{username} .\n⌯ Source : {me} .")
        else:
            print('- Taken UserName : ' + username + ' .')
    except errors.rpcbaseerrors.BadRequestError:
        print('- Banned UserName : ' + username + ' .')
        open("banned4.txt", "a").write(username + '\n')
    except errors.FloodWaitError as timer:
        print('- Flood Account [ ' + str(timer.seconds) + ' Secound ] .')
    except errors.UsernameInvalidError:
        print('- Error UserName : ' + username + ' .')

# for generate username
def usernameG():
    k = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(1))
    n = ''.join(choice('1234567890') for _ in range(2))
    return k + k + k + n

# start checking
async def start(client, username):
    ok = await fragment(username)
    try:
        if not ok:
            await checker(username, client)
        elif ok == "is taken":
            print('- Taken UserName : ' + username + ' .')
        else:
            print('- UserName Availabe In Fragment.com : ' + username + ' .')
            open("fragment.txt", "a").write(username + '\n')
    except Exception as e:
        print(e)

# get client
async def clientX():
    client = await TelegramClient("aho3", b64decode("MjUzMjQ1ODE=").decode(), b64decode("MDhmZWVlNWVlYjZmYzBmMzFkNWYyZDIzYmIyYzMxZDA=").decode()).start()
    clear()
    return client

# start tool
async def work():
    session = await clientX()
    if not path.exists('banned4.txt'):
        with open('banned4.txt', 'w') as new:
            pass
    if not path.exists('fragment.txt'):
        with open('fragment.txt', 'w') as new:
            pass
    if not path.exists('flood.txt'):
        with open('flood.txt', 'w') as new:
            pass
    while True:
        username = usernameG()
        with open('banned4.txt', 'r') as file:
            check_username = file.read()
        if username in check_username:
            print('- Banned1 UserName : ' + username + ' .')
            continue
        with open('fragment.txt', 'r') as file:
            fragment = file.read()
        if username in fragment:
            print('- UserName Available In Fragment.com : ' + username + ' .')
            continue
        await start(session, username)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(work())
