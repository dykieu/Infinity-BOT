# Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Discord API
import discord
from discord.utils import get
import asyncio
from decouple import config

# Google Sheet Info
googleDrive = gspread.service_account(filename='budget-tracker-285216-8c68f0609fb9.json')
gSheets = googleDrive.open('discord')
wSheet = gSheets.worksheet('Sheet1')

# Gets discord client
client = discord.Client()

# Bot command symbol
command = '!'

# Emoji [Must have these added to the server]
emojiPoll = ['pepoyes:812471635336626216', 'pepono:812471765238022163']
pepoYes = '<:pepoyes:812471635336626216>'
pepoNo = '<:pepono:812471765238022163>'

# List of Current Commands for the bot
commandList = '```\
BOT COMMANDS\n\
##############################\n\
!help - displays all commands\n\
!hello - says hello to the bot\n\
```'

# Raid Message Text
borutaEnd = ' EST (SERVER TIME)\n```\n Use the following emojis to indicate your availability: \n'
borutaStart = '** BORUTA RAID:**\n```ini\nDate: '
borutaTime = '\nTime: '

# Storage messages
Storage = []

# Client Event To Decorate / register an event
# When bot has logged in
@client.event
async def on_ready():
    print('Bot successfully connected')
    print('{0.user}'.format(client))

# On a Message event
@client.event
async def on_message(message):
    # Ignore author messages
    if message.author == client.user:
        return
    
    #!boruta [Time]
    if message.content.startswith( command + 'boruta'):
        print('[!boruta command Received]')

        # Grabs Time and Date from message
        times = message.content[13:]
        date = message.content[8:13]
        date = date.strip()
        times = times.strip()

        # If message within specs
        if ( times and ( len(times) <= 13 )):
            # Display recruitment Message
            sentMsg = await message.channel.send(borutaStart + date + '\n' + borutaTime + times + borutaEnd + '\n' + pepoYes + ' - YES\n' + pepoNo + '- NO\n' )
            Storage.append(sentMsg)

            # Add Reaction to Message
            for emoji in emojiPoll:
                await sentMsg.add_reaction(emoji)
        
        # If invalid command format
        else:
            await message.channel.send( 'Incorrect use of command' )

    # !hello Command
    if message.content.startswith( command + 'hello' ):
        print('[!hello command Received]')
        await message.channel.send('Hello!\n')

    # !help Command [Displays Help message]
    if message.content.startswith( command + 'help' ):
        print('[!help command Received]')
        await message.channel.send(commandList)

    # !end [Ends current poll]
    if message.content.startswith( command + 'end'):
        print('[!end command Received]')
        # If there is an active message
        if len(Storage) != 0:
            # For all active messages
            for msg in Storage:
                # Grabs channel and message details
                chanID = msg.channel
                getMsg = await chanID.fetch_message(msg.id)
                reactions = getMsg.reactions[0]

                # For all users the reacted, insert into google api
                users = await reactions.users().flatten()
                for x in users:
                    if x.bot == False:
                        wSheet.append_row([str(x.name), 'yes'])

        # If no valid polls
        else:
            await message.channel.send('No valid polls available to end')

if __name__ == '__main__':
    # Start Discord Bot Client
    print('starting App')
    client.run(config('DISCORD_TOKEN'))