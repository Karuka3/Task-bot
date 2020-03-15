import os
from slacker import Slacker
from plugins import bot_modules as bot
from datetime import datetime


def main():
    time = datetime.now().hour
    slack = Slacker(os.getenv("HUBOT_API_TOKEN"))
    if time == 18:
        target = "明日"
    else:
        target = "今日"
    task = bot.get_task(target, time)
    slack.chat.post_message(channel='to-do', text=task, as_user=True)


if __name__ == "__main__":
    main()
