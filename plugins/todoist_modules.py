import os
import re
import pytz
from todoist import TodoistAPI
from datetime import datetime
from dateutil.parser import parse


class TodoistItems:
    def __init__(self, token):
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
                    if date == parse(item['due']['date']).strftime('%Y/%m/%d'):
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
