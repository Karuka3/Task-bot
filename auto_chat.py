import os
from slacker import Slacker
from plugins import bot_modules as bot
from datetime import datetime


def main():
    time = datetime.now().hour
    slack = Slacker(os.getenv("HUBOT_API_TOKEN"))
    if time == 9:
        task = bot.get_task(date="今日")
    elif time == 13:
        task = bot.get_task(date="今日")
    elif time == 18:
        task = bot.get_task(date="明日")

    slack.chat.post_message(channel='to-do', text=task, as_user=True)


if __name__ == "__main__":
    main()
