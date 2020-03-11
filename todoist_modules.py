import os
import re
from datetime import datetime, timedelta
from todoist import TodoistAPI

api_token = "565a8c1cc785965dae2950a9cbec280132a4fbe7"
api = TodoistAPI(api_token)
api.sync()

project1 = api.projects.add('テストプロジェクト')
task1 = api.items.add('テストタスク')
api.commit()
