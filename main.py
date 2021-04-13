#yiban autoclock
import os
import time
import random
from card import Card
from notification import MiraiBot
from notification import ServerChan
from notification import Bark
from accounts import Accounts

USE_QQ_BOT = True #是否开启QQ推送 (基于Mirai框架)
USE_SVC = True #是否开启微信推送 (基于Server Chan)
USE_BARK = True #是否开启Bark推送

if __name__ == '__main__':
    print('Preparing to start...')
    # Get time
    begin_time = time.time()
    # Cleaning cache...
    for userid in Accounts.user_info:
        notification_mark = './images/' + userid[0] + '.sent'
        if os.path.exists(notification_mark):
            mark_time = os.path.getmtime(notification_mark)
            delta = begin_time - mark_time
            # Is the mark expired?
            if delta > 10800:
                os.remove(notification_mark)
    # Set bots
    if USE_SVC:
        wechatbot = ServerChan()
    if USE_BARK:
        barkbot=Bark()
    # Set success user
    successed_users = []
    # Clocking
    for (userid,passwd,location,username,userqq) in Accounts.user_info:
        on_progress = 1
        try_times = 0
        while on_progress:
            pending = random.randint(1,10)
            try:
                clock_process = Card()
                try_times += 1  # Count total trys
                on_progress = clock_process.clock_yiban(userid,passwd,location)
                print('User ' + username + ' clocked successfully!')
                successed_users.append(username)
                
                print('Will continue after ' + str(pending) + 'secs...')
                time.sleep(pending)
            except Exception as e:
                print('Something went wrong! retrying after ' + str(pending) + 'secs...')
                print(e)
                time.sleep(pending)
                on_progress = 1
            # Overtry alert
            if try_times % 10 == 0:
                alert_payload = 'Operation failed! Keep trying... Trys: ' + str(try_times) 
                if USE_SVC:
                        # Send Wechat message to alert admin
                        wechatbot.send_wechat_message(alert_payload)
                else:
                    print(alert_payload)
    # Send summary to admin
    summary = '本次打卡成功！' + ' 共耗时{:.1f}s 用户：'.format(time.time() - begin_time) + '、'.join(successed_users) 
    if USE_SVC:
        wechatbot.send_wechat_message(summary)
    if USE_QQ_BOT:
        qqbot = MiraiBot()
        for userid in Accounts.user_info:
            if os.path.exists('./images/' + userid[0] + '.sent'):
                        print('Sent notification, skipping...')
            else:
                # Send to QQ
                try:
                    send2qq = qqbot.send_image_from_file('./images/' + userid[0] + '.png', userid[4])
                    if send2qq:
                        print('Failed!')
                    else:
                        print('Sent to target qq!')
                        # Set mark
                        mark = open('./images/' + userid[0] + '.sent', 'w+')
                        mark.close()
                except Exception as eq:
                    print('Something went wrong when sending qq message...')
                    print(eq)
        qqbot.alert_admin(summary)
        # Release mirai session
        qqbot.release_session()
    if USE_BARK:
        barkbot.send_bark_alert(summary)