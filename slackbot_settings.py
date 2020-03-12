import os

API_TOKEN = os.getenv("BOT_API_TOKEN")

# 知らない言葉を聞いた時のデフォルトの応答
DEFAULT_REPLY = "その言葉の意味は知りません"

# 外部ファイルを読み込み
PLUGINS = [
    'slackbot.plugins',
    'bot_modules',
]
