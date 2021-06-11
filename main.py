#yiban autoclock
import os
import time
import random
from card import Card
from notification import MiraiBot
from notification import ServerChan
from notification import Bark
from notification import XiaoLzBot

settings = []
with open('settings.json','r') as setting_file:
    settings = eval(setting_file.read())
    setting_file.close()

accounts = []
with open('account.json','r',encoding='utf-8') as accounts_file:
    accounts = eval(accounts_file.read())
    accounts_file.close()

USE_QQ_BOT = settings[0]['USE_QQBOT'] #是否开启QQ推送 (0:关闭；1:基于Mirai框架；2:基于小栗子框架) 
USE_SVC = settings[1]['USE_SVC'] #是否开启微信推送 (基于Server Chan)
USE_BARK = settings[2]['USE_BARK'] #是否开启Bark推送

if __name__ == '__main__':
    print('准备开始打卡'.center(30,'#'))
    # Get time
    begin_time = time.time()
    # Cleaning cache...
    for accounts_info in accounts:
        notification_mark = './images/{}.sent'.format(accounts_info['userid'])
        if os.path.exists(notification_mark):
            mark_time = os.path.getmtime(notification_mark)
            delta = begin_time - mark_time
            # Is the mark expired?
            if delta > 10800:
                os.remove(notification_mark)
    for notification_mark in ['bark', 'wechat']:
        if os.path.exists('./images/{}.sent'.format(notification_mark)):
            mark_time = os.path.getmtime('./images/{}.sent'.format(notification_mark))
            delta = begin_time - mark_time
            # Is the mark expired?
            if delta > 10800:
                os.remove('./images/{}.sent'.format(notification_mark))
    # Set bots
    if USE_SVC:
        wechatbot = ServerChan()
    if USE_BARK:
        barkbot=Bark()
    # Set success user
    successed_users = []
    # Clocking
    for accounts_info in accounts:
        on_progress = 1
        try_times = 0
        while on_progress:
            pending = random.randint(1,5)
            error = ''
            try:
                try_times += 1  # Count total trys
                print("\n>> {} 的第{}次尝试开始！尝试使用主方案(Url)...".format(accounts_info['name'],try_times))
                on_progress = Card().clock_yiban(accounts_info['userid'],accounts_info['url'])
                if on_progress == 0:
                    print('[O]尝试为 {} 打卡成功！'.format(accounts_info['name']))
                    successed_users.append(accounts_info['name'])
                else:
                    print('[!]尝试为 {} 打卡失败！尝试使用备用方案(Classic)...'.format(accounts_info['name']))
                    on_progress = Card().clock_yiban_backup(accounts_info['userid'],accounts_info['password'],accounts_info['phone'])
                    if on_progress:
                        print('[!]尝试为 {} 打卡失败！准备重试主方案(Url)...'.format(accounts_info['name']))
                    else:
                        print('[O]尝试为 {} 打卡成功！'.format(accounts_info['name']))
                        successed_users.append(accounts_info['name'])
                print('[i]将在{}秒后尝试下一位\n'.format(pending))
                time.sleep(pending)
            except Exception as err:
                print('[!]遇到了以下问题！将在{}秒后继续尝试\n'.format(pending))
                print(err)
                time.sleep(pending)
                on_progress = 1
                error = err
            # Overtry alert
            if try_times > 30:
                fail = '[!]已经尝试为{}打卡失败{}次，将不再尝试，请手动打卡！\n\n失败原因：{}'.format(accounts_info['name'], str(try_times), error)
                print(fail)
                on_progress = 0
                if os.path.exists('./images/{}.png'.format(accounts_info['userid'])):
                    os.remove('./images/{}.png'.format(accounts_info['userid']))
                if USE_QQ_BOT:
                    if USE_QQ_BOT == 2:
                        XiaoLzBot().send_to_friend(fail, settings[0]['adminqq'])
                        XiaoLzBot().send_to_friend(fail, accounts_info['userqq'])
                if USE_BARK:
                    barkbot.send_bark_alert('易班打卡失败通知', alert_payload)
            elif try_times % 10 == 0:
                alert_payload = '[!]尝试为{}打卡失败！已经尝试{}次，继续尝试中。。。\n\n失败原因：{}'.format(accounts_info['name'], str(try_times), error)
                print(alert_payload)
                if USE_SVC:
                        # Send Wechat message to alert admin
                        wechatbot.send_wechat_message(alert_payload)
                if USE_QQ_BOT:
                    if USE_QQ_BOT == 2:
                        XiaoLzBot().send_to_friend(alert_payload, settings[0]['adminqq'])
                        XiaoLzBot().send_to_friend(alert_payload, accounts_info['userqq'])
                if USE_BARK:
                    barkbot.send_bark_alert('易班打卡失败通知', alert_payload)
    # Notification
    print('\n')
    print('[i]开始推送通知'.center(30,'#'))
    print('\n')
    # Send summary to admin
    summary = '本次打卡成功！' + ' 共耗时{:.1f}s 用户：'.format(time.time() - begin_time) + '、'.join(successed_users) 
    if USE_BARK:
        if os.path.exists('./images/bark.sent'):
            print('[O]已经推送过Bark消息了，跳过……')
        else:
            print('[i]开始推送Bark消息')
            barkbot.send_bark_alert('易班打卡成功通知', summary)
            with open('./images/bark.sent','w') as b:
                b.close()
    if USE_SVC:
        if os.path.exists('./images/wechat.sent'):
            print("[O]已经推送过微信消息了，跳过……")
        else:
            wechatbot.send_wechat_message(summary)
            print('[i]开始推送微信消息')
            with open('./images/wechat.sent','w') as w:
                w.close()
    if USE_QQ_BOT:
        for user_info in accounts:
            if os.path.exists('./images/{}.sent'.format(user_info['userid'])):
                        print('[O]已经推送过QQ消息了，跳过……')
            else:
                # Send to QQ
                if USE_QQ_BOT == 1:
                    try:
                        print('[i]开始推送QQ消息')
                        qqbot = MiraiBot()
                        send2qq = qqbot.send_image_from_file('./images/{}.png'.format(user_info['userid']), user_info['userqq'])
                        if send2qq:
                            print('[!]发送QQ截图失败！')
                        else:
                            print('[!]已经将结果发送至目标QQ！')
                            # Set mark
                            mark = open('./images/{}.sent'.format(user_info['userid']), 'w+')
                            mark.close()
                    except Exception as eq:
                        print('[!]遇到了以下问题，推送QQ消息失败！')
                        print(eq)
                else:
                    try:
                        qqbot = XiaoLzBot()
                        payload = 'images\\' + user_info['userid'] + '.png'
                        if os.path.exists(payload):
                            send2qq = qqbot.send_image_to_friends(payload, user_info['userqq'])
                            if send2qq:
                                print('[!]发送QQ截图失败！')
                            else:
                                print('[O]已经将结果发送至目标QQ！')
                        # Set mark
                        mark = open('./images/{}.sent'.format(user_info['userid']), 'w+')
                        mark.close()
                    except Exception as eq:
                        print('[!]遇到了以下问题，推送QQ消息失败！')
                        print(eq)
    print('\n')
    print('结果通知'.center(30,'#'))
    print('\n')
    print('[i]打卡完成！5秒后退出...')
    time.sleep(5)