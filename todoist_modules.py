import os
import re
import pytz
from todoist import TodoistAPI
from datetime import datetime, timedelta


class TodoistItems:
    def __init__(self, token):
        self.weekdays = {
            0: ['mon', '月曜'],
            1: ['tue', '火曜'],
            2: ['wed', '水曜'],
            3: ['thu', '木曜'],
            4: ['fri', '金曜'],
            5: ['sat', '土曜'],
            6: ['sun', '日曜'],
        }
        self.api_token = token
        self.api = TodoistAPI(self.api_token)
        self.api.sync()


# api_token = "565a8c1cc785965dae2950a9cbec280132a4fbe7"
