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

    def key_check(self, item, key):
        try:
            result = item[key]
            return result
        except:
            return False

    def date_check(self, item, date):
        if self.key_check(item, 'due'):
            if item['due']['lang'] == 'ja':
                if date.replace('/', '-') in item['due']['date']:
                    return True
                elif '毎日' in item['due']['string']:
                    return True
            else:
                try:
                    date_time = datetime.strptime(item['due']['date'], '%Y-%m-%dT%H:%M:%SZ')
                    date_time = pytz.utc.localize(date_time).astimezone(pytz.timezone("Asia/Tokyo"))
                    if date == date_time.strftime('%Y/%m/%d'):
                        return True
                except ValueError:
                    pass
        return False

    def get_project_name(self, item):
        if self.key_check(item, 'project_id'):
            project_id = item['project_id']
        else:
            project_id = item['parent_id']
        project = self.api.projects.get_by_id(project_id)
        return project['name']

    def find_by_date(self, date):
        return [item for item in self.api['items'] if self.date_check(item, date)]
