from slackbot.bot import respond_to
from todoist_modules import TodoistItems
from datetime import datetime
from pytz import timezone
import os


def confirm_target_date(date):
    if date == "今日":
        target_date = datetime.now().astimezone(timezone('Asia/Tokyo')).strftime('%Y/%m/%d')
    elif date == "明日":
        tomorrow = datetime.now().astimezone(timezone('Asia/Tokyo')) + datetime.timedelta(days=1)
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


def fix_date_time(item, date_string):
    if item['due']['lang'] == 'ja':
        if '毎週' in date_string:
            date, time = date_string.replace(' ', '').split('曜日')
        else:
            date, time = date_string.replace('月', '/').replace(' ', '').split('日')
    else:
        if 'every' in date_string:
            if 'at' in date_string:
                date, time = date_string.replace(' ', '').replace('sat', 'sa').split('at')
            else:
                date = date_string.replace(' ', '')
                time = '12:00'
        else:
            date, time = date_string.replace('-', '/').split(' ')
    return date, time


def get_task(date):
    target_date = confirm_target_date(date)
    output = "%sの予定だよ\n確認してね!\n" % target_date
    texts = {}
    t = TodoistItems(os.environ["TODOIST_API_TOKEN"])
    items = t.find_by_date(target_date)

    for i, item in enumerate(items):
        date_string = item['due']['string']
        mark = confirm_checked(item, target_date)
        date, time = fix_date_time(item, date_string)
        items[i]['date'] = date
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
    output = get_task(date)
    message.send(output)
