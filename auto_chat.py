import os
from slacker import Slacker
from plugins import bot_modules as bot


def main():
    task = bot.get_task(date="今日")
    slack = Slacker(os.getenv("HUBOT_API_TOKEN"))
    slack.chat.post_message(channel='to-do', text=task, as_user=True)


if __name__ == "__main__":
    main()
