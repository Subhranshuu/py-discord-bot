import datetime
import random
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass


BOT_TOKEN = "MTQxNjI1MTAxNTYwNjMwODk4NQ.Gmqsk5.2NOfE0uqRiLhZSfNsVVsgPDHttXXH2VLMZn60o"
CHANNEL_ID = 1416253660035420191
MAX_SESSION_TIME_MINUTES = 45


@dataclass
class Session:
    is_active: bool = False
    start_time: datetime.datetime = None

session = Session()
daily_study_time = datetime.timedelta(0)


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

MOTIVATIONAL_QUOTES = [
    "Keep going! 🚀 You’re doing amazing!",
    "Focus and breathe. You’ve got this! 💪",
    "One step at a time, success is near! 🌟",
    "Stay consistent! Small efforts matter. 📚",
    "Believe in yourself. Every effort counts! ✨",
]

BREAK_MESSAGES = [
    "Stretch your legs! 🦵",
    "Time for a coffee ☕ or water 💧",
    "Dance a little 💃🕺",
    "Check the memes! 😆",
    "Close your eyes for 2 mins 💤",
]

STUDY_TIPS = [
    "Pomodoro technique: 25 mins study, 5 mins break ⏳",
    "Take notes by hand for better memory 📝",
    "Teach someone else what you learned today 👩‍🏫",
    "Remove distractions: phone on silent 📵",
    "Review your notes before sleeping 🛌",
    "Set small achievable goals daily 🎯",
    "Use diagrams and colors to remember concepts 🌈",
]

FUN_MESSAGES = [
    "You’re a study ninja! 🥷",
    "Keep grinding, success is near! 💎",
    "Brain muscles activated! 🧠💪",
    "Knowledge is power! ⚡",
    "Stay awesome! 😎",
]


@bot.event
async def on_ready():
    print("✅ Study Bot is online!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("📚 Hello! Study Bot is ready! Type `!start` to begin studying.")
    
   
    reset_daily_time.start()


@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES)
async def break_reminder():
    if session.is_active:
        channel = bot.get_channel(CHANNEL_ID)
        message = random.choice(BREAK_MESSAGES)
        await channel.send(f"⏱️ **Break time!** {message}")

@tasks.loop(hours=1)
async def motivation_loop():
    if session.is_active:
        channel = bot.get_channel(CHANNEL_ID)
        quote = random.choice(MOTIVATIONAL_QUOTES)
        await channel.send(f"💡 Motivation: {quote}")

@tasks.loop(minutes=30)
async def fun_message_loop():
    if session.is_active:
        channel = bot.get_channel(CHANNEL_ID)
        message = random.choice(FUN_MESSAGES)
        await channel.send(f"🎉 Fun boost: {message}")


@tasks.loop(hours=24)
async def reset_daily_time():
    global daily_study_time
    daily_study_time = datetime.timedelta(0)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("🗓️ Daily study time has been reset!")


@bot.command()
async def start(ctx):
    if session.is_active:
        return await ctx.send("⚠️ A session is already active!")

    session.is_active = True
    session.start_time = datetime.datetime.now()
    break_reminder.start()
    motivation_loop.start()
    fun_message_loop.start()
    await ctx.send(f"✅ New session started at {session.start_time.strftime('%H:%M:%S')}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        return await ctx.send("⚠️ No session is active!")

    session.is_active = False
    duration = datetime.datetime.now() - session.start_time
    global daily_study_time
    daily_study_time += duration
    break_reminder.stop()
    motivation_loop.stop()
    fun_message_loop.stop()
    await ctx.send(f"🛑 Session ended! Total duration: {duration}\n📊 Today you studied: {daily_study_time}")

@bot.command()
async def status(ctx):
    if session.is_active:
        elapsed = datetime.datetime.now() - session.start_time
        await ctx.send(f"📌 Session active! Elapsed time: {elapsed}")
    else:
        await ctx.send("❌ No session is active right now.")

@bot.command()
async def tip(ctx):
    tip = random.choice(STUDY_TIPS)
    await ctx.send(f"💡 Study Tip: {tip}")

@bot.command()
async def motivate(ctx):
    quote = random.choice(MOTIVATIONAL_QUOTES)
    await ctx.send(f"💡 Motivation: {quote}")

@bot.command()
async def fun(ctx):
    message = random.choice(FUN_MESSAGES)
    await ctx.send(f"🎉 Fun boost: {message}")

@bot.command()
async def breaktime(ctx):
    message = random.choice(BREAK_MESSAGES)
    await ctx.send(f"⏱️ Break reminder: {message}")

@bot.command()
async def daily(ctx):
    await ctx.send(f"📊 Total study time today: {daily_study_time}")


bot.run(BOT_TOKEN)
