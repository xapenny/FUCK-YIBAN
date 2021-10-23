#yiban autoclock
import json
import os
import time
import random
from card import Card
from notification import MiraiBot
from notification import ServerChan
from notification import Bark
from notification import XiaoLzBot

settings = []
with open('settings.json','r',encoding='utf-8') as _settings:
    settings = json.load(_settings)
    _settings.close()

accounts = []
with open('accounts.json','r',encoding='utf-8') as _accounts:
    accounts = json.load(_accounts)
    _accounts.close()

USE_QQ_BOT = settings['qq']['USE_QQBOT'] #是否开启QQ推送 (0:关闭；1:基于Mirai框架；2:基于小栗子框架) 
USE_SVC = settings['wechat']['USE_SVC'] #是否开启微信推送 (基于Server Chan)
USE_BARK = settings['bark']['USE_BARK'] #是否开启Bark推送

if __name__ == '__main__':
    print('准备开始打卡'.center(30,'#'))
    #wa1t = random.randint(300,1800)
    #print('wa1ting {} secs...'.format(wa1t))
    #time.sleep(wa1t)
    print('\n')
    # Get time
    begin_time = time.time()
    # Cleaning cache...
    for accounts_info in accounts:
        notification_mark = f"./images/{accounts_info['userid']}.sent"
        if os.path.exists(notification_mark):
            mark_time = os.path.getmtime(notification_mark)
            delta = begin_time - mark_time
            # Is the mark expired?
            if delta > 10800:
                os.remove(notification_mark)
    for notification_mark in ['bark', 'wechat']:
        if os.path.exists(f'./images/{notification_mark}.sent'):
            mark_time = os.path.getmtime(f'./images/{notification_mark}.sent')
            delta = begin_time - mark_time
            # Is the mark expired?
            if delta > 10800:
                os.remove(f'./images/{notification_mark}.sent')
    # Set bots
    if USE_SVC:
        wechatbot = ServerChan()
    if USE_BARK:
        barkbot=Bark()
    # Set success user
    successed_users = []
    # Clocking
    for accounts_info in accounts:
        if not accounts_info['enable']:
            print(f"{accounts_info['name']} 的打卡功能已被禁用，尝试下一位……")
            continue
        on_progress = False
        try_times = 0
        while not on_progress:
            pending = random.randint(1,5)
            error = ''
            try:
                try_times += 1  # Count total trys
                print(f"\n>> {accounts_info['name']} 的第{try_times}次尝试开始！尝试使用主方案(Url)...")
                on_progress = Card().clock_yiban(accounts_info['userid'],accounts_info['url'],accounts_info['location'])
                if on_progress:
                    print(f"[O]尝试为 {accounts_info['name']} 打卡成功！")
                    successed_users.append(accounts_info['name'])
                else:
                    print(f"[!]尝试为 {accounts_info['name']} 打卡失败！尝试使用备用方案(Classic)...")
                    on_progress = Card().clock_yiban_backup(accounts_info['userid'],accounts_info['password'],accounts_info['phone'],accounts_info['location'])
                    if on_progress:
                        print(f"[O]尝试为 {accounts_info['name']} 打卡成功！")
                        successed_users.append(accounts_info['name'])
                    else:
                        print(f"[!]尝试为 {accounts_info['name']} 打卡失败！准备重试主方案(Url)...")
                print(f"[i]将在{pending}秒后尝试下一位\n")
                time.sleep(pending)
            except Exception as err:
                print(f"[!]遇到了以下问题！将在{pending}秒后继续尝试\n")
                print(err)
                if USE_QQ_BOT:
                    if USE_QQ_BOT == 1:
                        MiraiBot().send_to_friend(err, settings['qq']['adminqq'])
                    elif USE_QQ_BOT == 2:
                        XiaoLzBot().send_to_friend(err, settings['qq']['adminqq'])
                time.sleep(pending)
                on_progress = False
                error = err
            # Overtry alert
            if try_times > 30:
                fail = f"[!]已经尝试为{accounts_info['name']}打卡失败{str(try_times)}次，将不再尝试，请手动打卡！"
                print(fail)
                on_progress = True
                if os.path.exists(f"./images/{accounts_info['userid']}.png"):
                    os.remove(f"./images/{accounts_info['userid']}.png")
                if USE_QQ_BOT:
                    if USE_QQ_BOT == 1:
                        MiraiBot().send_to_friend(fail, settings['qq']['adminqq'])
                        MiraiBot().send_to_friend(fail, accounts_info['userqq'])
                    elif USE_QQ_BOT == 2:
                        XiaoLzBot().send_to_friend(fail, settings['qq']['adminqq'])
                        XiaoLzBot().send_to_friend(fail, accounts_info['userqq'])
                        XiaoLzBot().call_friend(accounts_info['userqq'])
                if USE_BARK:
                    barkbot.send_bark_alert('易班打卡失败通知【上海】', alert_payload)
            elif try_times % 10 == 0:
                alert_payload = f"[!]尝试为{accounts_info['name']}打卡失败！已经尝试{str(try_times)}次，继续尝试中。。。"
                print(alert_payload)
                if USE_SVC:
                        # Send Wechat message to alert admin
                        wechatbot.send_wechat_message(alert_payload)
                if USE_QQ_BOT:
                    if USE_QQ_BOT == 1:
                        MiraiBot().send_to_friend(alert_payload, settings['qq']['adminqq'])
                        MiraiBot().send_to_friend(alert_payload, accounts_info['userqq'])
                    elif USE_QQ_BOT == 2:
                        XiaoLzBot().send_to_friend(alert_payload, settings['qq']['adminqq'])
                        XiaoLzBot().send_to_friend(alert_payload, accounts_info['userqq'])
                if USE_BARK:
                    barkbot.send_bark_alert('易班打卡失败通知【上海】', alert_payload)
    # Notification
    print('\n')
    print('[i]开始推送通知'.center(30,'#'))
    print('\n')
    # Send summary to admin
    summary = '本次打卡成功！共耗时{:.1f}s 用户：'.format(time.time() - begin_time) + '、'.join(successed_users) 
    if USE_BARK:
        if os.path.exists('./images/bark.sent'):
            print('[O]已经推送过Bark消息了，跳过……')
        else:
            print('[i]开始推送Bark消息')
            barkbot.send_bark_alert('易班打卡成功通知【上海】', summary)
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
            if os.path.exists(f"./images/{user_info['userid']}.sent"):
                        print('[O]已经推送过QQ消息了，跳过……')
            elif not user_info['enable']:
                            print(f"[!]{user_info['name']}的账户被禁用，不推送消息")
            else:
                # Send to QQ
                payload_final = f"您好，{user_info['name']}\n现在是{time.strftime('%Y-%m-%d, %H:%M:%S')}\n已经完成了易班打卡！\n注意，如果已经收到过成功的消息即代表成功，此后2小时内的失败消息可以忽略。"
                if USE_QQ_BOT == 1:
                    if 1:
                        print('[i]开始推送QQ消息(Mirai)')
                        send2qq = MiraiBot().send_to_friend(payload_final, user_info['userqq'], f"./images/{user_info['userid']}.png")
                        if send2qq:
                            print('[!]已经将结果发送至目标QQ！')
                            # Set mark
                            mark = open(f"./images/{user_info['userid']}.sent", 'w+')
                            mark.close()
                        else:
                            print('[!]发送QQ截图失败！')
                    # except Exception as eq:
                    #     print('[!]遇到了以下问题，推送QQ消息失败！')
                    #     print(eq)
                elif USE_QQ_BOT == 2:
                    try:
                        print('[i]开始推送QQ消息(XiaoLz)')
                        payload = f"images\\{user_info['userid']}.png"
                        if os.path.exists(payload):
                            print(f"5秒后为{user_info['name']}推送消息...")
                            time.sleep(5)
                            send2qq = XiaoLzBot().send_to_friend(payload_final, user_info['userqq'])
                            if send2qq:
                                print('[O]已经将结果发送至目标QQ！')
                                # Set mark
                                mark = open(f"./images/{user_info['userid']}.sent", 'w+')
                                mark.close()
                            else:
                                print('[!]发送QQ截图失败！')
                    except Exception as eq:
                        print('[!]遇到了以下问题，推送QQ消息失败！')
                        print(eq)
    print('\n')
    print('结果通知'.center(30,'#'))
    print('\n')
    print('[i]打卡完成！5秒后退出...')
    if USE_QQ_BOT == 1:
        MiraiBot().release_session()
    time.sleep(5)