import json
import os
import random

import discord
import requests
from discord.ext import commands

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


def get_image(setup):
  url = "https://image-search13.p.rapidapi.com/"
  querystring = {"q": setup, "hl": "en"}
  headers = {
      "X-RapidAPI-Key": "5cf393376fmsh9ee7aff0371de7bp19a155jsne283f6365e29",
      "X-RapidAPI-Host": "image-search13.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)
  response = response.json()
  url_img = ""
  n = random.randint(0, len(response["response"]["images"]) - 1)
  url_img = response["response"]["images"][n]["image"]["url"]
  return url_img


@bot.event
async def on_ready():
  print("we have loged in as {0.user}".format(bot))


@bot.command()
async def joineddate(ctx, member: discord.Member):
  await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.command()
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)


@bot.command()
async def women(ctx):
  await ctx.send("https://i.ytimg.com/vi/-gu0i3kX6h0/hqdefault.jpg")


@bot.command()
async def ping(ctx):
  await ctx.send(f"your ping is {round(bot.latency*1000)}ms")


@bot.command()
async def img(ctx, *args):
  setup = ' '.join(args)
  await ctx.send(get_image(setup))


@bot.command()
async def cl(ctx):
  t = [
      "joineddate", "inspire", "ping", "img '....'",
      "tictactoe @you @yourfriend"
  ]
  msg = f"${t[0]}" + " " * (30 - len(
      t[0])) + "#when a member joined\n" + f"${t[1]}" + " " * (30 - len(
          t[1])) + "#get a random quote\n" + f"${t[2]}" + " " * (30 - len(
              t[2])) + "#it tell the bot's ping\n" + f"${t[3]}" + " " * (
                  30 - len(t[3])
              ) + "#get a random image from the web\n" + f"${t[4]}" + " " * (
                  30 - len(t[4])) + "#play tictactoe with your friend"
  await ctx.send(msg)


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]


@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
  global count
  global player1
  global player2
  global turn
  global gameOver

  if gameOver:
    global board
    board = [
        ":white_large_square:", ":white_large_square:", ":white_large_square:",
        ":white_large_square:", ":white_large_square:", ":white_large_square:",
        ":white_large_square:", ":white_large_square:", ":white_large_square:"
    ]
    turn = ""
    gameOver = False
    count = 0

    player1 = p1
    player2 = p2

    # print the board
    line = ""
    for x in range(len(board)):
      if x == 2 or x == 5 or x == 8:
        line += " " + board[x]
        await ctx.send(line)
        line = ""
      else:
        line += " " + board[x]

    # determine who goes first
    num = random.randint(1, 2)
    if num == 1:
      turn = player1
      await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
    elif num == 2:
      turn = player2
      await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
  else:
    await ctx.send(
        "A game is already in progress! Finish it before starting a new one.")


@bot.command()
async def pl(ctx, pos: int):
  global turn
  global player1
  global player2
  global board
  global count
  global gameOver

  if not gameOver:
    mark = ""
    if turn == ctx.author:
      if turn == player1:
        mark = ":regional_indicator_x:"
      elif turn == player2:
        mark = ":o2:"
      if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
        board[pos - 1] = mark
        count += 1

        # print the board
        line = ""
        for x in range(len(board)):
          if x == 2 or x == 5 or x == 8:
            line += " " + board[x]
            await ctx.send(line)
            line = ""
          else:
            line += " " + board[x]

        checkWinner(winningConditions, mark)
        print(count)
        if gameOver is True:
          await ctx.send(mark + " wins!")
        elif count >= 9:
          gameOver = True
          await ctx.send("It's a tie!")

        # switch turns
        if turn == player1:
          turn = player2
        elif turn == player2:
          turn = player1
      else:
        await ctx.send(
            "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
        )
    else:
      await ctx.send("It is not your turn.")
  else:
    await ctx.send("Please start a new game using the $tictactoe command.")


def checkWinner(winningConditions, mark):
  global gameOver
  for condition in winningConditions:
    if board[condition[0]] == mark and board[condition[1]] == mark and board[
        condition[2]] == mark:
      gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please mention 2 players for this command.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Please make sure to mention/ping players).")


@pl.error
async def place_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please enter a position you would like to mark.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Please make sure to enter an integer.")


@bot.command()
async def endtic(ctx):
  global gameOver
  if gameOver is False:
    gameOver = True
    await ctx.send("game stopped")
  else:
    await ctx.send("game already stopped")


keep_alive()
bot.run(os.environ["TOKEN"])
