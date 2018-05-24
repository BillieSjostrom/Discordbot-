import discord
import asyncio
import logging
import os
import random
from random import randint
import re
from ordsprak import ordsprok_list as ord_list, hangman_words

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

hangman = {'state': 'waiting'}


if os.path.exists('.env'):
    logging.info('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


client = discord.Client()


@client.event
async def on_ready():
    logger.info('Logged in as {} ({}).'.format(client.user.name, client.user.id))



# @client.event
# async def on_message(message):
#     if message.content.startswith('!throw'):
#         r = re.match('^!throw (?P<num>\d+) d(?P<sides>\d+)$', message.content)
#
#         if r is not None:
#             num, sides = int(r.group('num')), int(r.group('sides'))
#             dice = [str(random.randint(1, sides)) for _ in range(num)]
#             logger.debug('Threw {} d{} ({})'.format(num, sides, ', '.join(dice)))
#             await client.send_message(message.channel, ', '.join(dice))
#         else:
#             await client.send_message(message.channel, 'Syntax is:\n!throw <number of dice> d<number of sides>')



@client.event
async def on_message(message):
    global hangman
    logger.debug('Hangman state: {}'.format(hangman))

    if message.content.startswith ('!info'):
        logger.info('Info event')
        await client.send_message(message.channel, 'Detta är en bot gjord av Billie')

    if message.content.startswith ('!ping'):
        logger.info('Info event')
        await client.send_message(message.channel, 'pong!')

    if message.content.startswith ('!ordspråk'):
         random.shuffle(ord_list)
         num = randint(1, len(ord_list))
         await client.send_message(message.channel, '{}'.format(ord_list[num - 1]))


    if message.content.startswith ('!hängagubbe'):
        if not hangman.get('lives'):
            hangman['lives'] = 3
        num = randint(1, len(hangman_words))
        hangman['word'] = hangman_words[num - 1]
        hangman['state'] = 'playing'


        if hangman['lives'] < 1:
            await client.send_message(message.channel, 'You lost!')
        await client.send_message(message.channel, 'guess a letter!')


    if message.content.startswith ('!letter'):
        # Kolla att vi är i rätt 'state', hangman['state'] == 'playing'
        # annars skriv ut instruktion om att starta spel

        args = message.content.split()[1:]
        letter = args[0].lower()

        valid_letters = 'abcdefghijklmnopqrstuvwxyzåäö'

        if not (len(letter) == 1 and letter in valid_letters):
            await client.send_message(message.channel, 'Invalid syntax. Write "!letter x" where x is your guess.')

        logger.debug('Hangman guess: {}'.format(letter))

        # Update list of guesses
        if hangman.get('guesses') is None:
            hangman['guesses'] = []
        hangman['guesses'].append(letter)

        logger.debug('Hangman list of guesses: {}'.format(hangman['guesses']))

        # Check for win
        # sätt hangman['state'] till ???
        # skriv ut meddelande
        if hangman['guesses'] == hangman['word']:
            await client.send_message(message.channel,'you won')



        # Check for game over
        # sätt hangman['state'] till 'gameover'
        # skriv ut meddelande

        # Produce a response to the player
        if letter in hangman['word']:
            # Correct guess
            response = 'You have guessed right\n'
        else:
            # Wrong guess
            # Räkna ner hangman['lives']
            response = 'Your guess is incorrect\n'

        for l in hangman['word']:
            if l in hangman['guesses']:
                response = response + l
            else:
                response = response + '[]'

        await client.send_message(message.channel, response)


# Start the bot
client.run(os.environ.get('TOKEN'))
