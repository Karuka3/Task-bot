from slackbot.bot import respond_to
from plugins import todoist_modules as todo
from datetime import datetime, timedelta
from pytz import timezone
import os


def confirm_date(date):
    if date == "今日":
        target_date = datetime.now().astimezone(timezone('Asia/Tokyo')).strftime('%Y/%m/%d')
    elif date == "明日":
        tomorrow = datetime.now().astimezone(timezone('Asia/Tokyo')) + timedelta(days=1)
        target_date = tomorrow.strftime('%Y/%m/%d')
    else:
        target_date = datetime.strptime(date, '%Y/%m/%d').astimezone(timezone('Asia/Tokyo')).strftime('%Y/%m/%d')
    return target_date


def confirm_checked(item, date):
    mark = ':white_square:'
    if item['checked']:
        mark = ':white_check_mark:'
    else:
        if item['due']['is_recurring'] and date.replace('/', '-') not in item['due']['date']:
            mark = ':white_check_mark:'
    return mark


def split_datetime(item, date_string):
    time = ''
    if item['due']['lang'] == 'ja':
        if '毎週' in date_string:
            time = date_string.replace(' ', '').split('曜日')[1]
        else:
            time = date_string.replace('月', '/').replace(' ', '').split('日')[1]
    else:
        if 'every' in date_string:
            dt = date_string.split()
            if len(dt) == 3:
                time = dt[2]
        else:
            dt = date_string.split()
            if len(dt) == 3:
                time = dt[2]
    return time


def confirm_time(hour, date):
    if 7 <= hour < 12:
        output = "おはようございます！\n%sのタスクです！%sも頑張ってねっ！\n" % date
    elif 12 <= hour < 18:
        output = "午後からも頑張っていこうねっ！タスク確認です！\n"
    elif 18 <= hour < 21:
        output == "今日もお疲れさまだよっ！\n%sのタスクです！%sも頑張ってねっ！\n" % date
    else:
        output = "%sの予定です！\n確認してね！\n" % date
    return output


def get_task(date, hour):
    target_date = confirm_date(date)
    output = confirm_time(hour, date)
    texts = {}
    t = todo.TodoistItems("273a17fc849fd710d8736a7a43388c49af09d953")
    items = t.find_by_date(target_date)

    for i, item in enumerate(items):
        mark = confirm_checked(item, target_date)
        time = split_datetime(item, item['due']['string'])
        items[i]['time'] = time

        if time == '':
            index = '_' + str(i)
        else:
            index = time + '_' + str(i)

        param = {index: {
            'mark': mark,
            'time': time,
            'subject': item['content']
        }}
        texts.update(param)

    for _k, v in enumerate(sorted(texts)):
        output += "%s %s %s\n" % (texts[v]['mark'], texts[v]['time'], texts[v]['subject'])

    return output


@respond_to('^(.*)の予定$')
def task_list(message, date):
    output = get_task(date, 100)
    message.send(output)
