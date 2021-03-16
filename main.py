#yiban autoclock
import os
import time
import random
from card import Card
from notification import MiraiBot
from notification import ServerChan
from accounts import Accounts

USE_QQ_BOT = True #是否开启QQ推送 (基于Mirai框架)
USE_SVC = True #是否开启微信推送 (基于Server Chan)

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
    if USE_QQ_BOT:
        qqbot = MiraiBot()
    if USE_SVC:
        wechatbot = ServerChan()
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
                if os.path.exists('./images/' + userid + '.sent'):
                    print('Sent notification, skipping...')
                else:
                    if USE_QQ_BOT:
                        # Send to QQ
                        try:
                            send2qq = qqbot.send_image_from_file('./images/' + userid + '.png', userqq)
                            if send2qq:
                                print('Failed!')
                            else:
                                print('Sent to target qq!')
                                # Set mark
                                mark = open('./images/' + userid + '.sent', 'w+')
                                mark.close()
                        except Exception as eq:
                            print('Something went wrong when sending qq message...')
                            print(eq)
                    else:
                        pass
                print('Will continue after ' + str(pending) + 'secs...')
                time.sleep(pending)
            except Exception as e:
                print('Something went wrong! retrying after ' + str(pending) + 'secs...')
                print(e)
                time.sleep(pending)
                on_progress = 1
            # Overtry alert
            if try_times % 10 == 0:
                # Send QQ message to admin
                alert_payload = 'Operation failed! Keep trying... Trys: ' + str(try_times) 
                if USE_QQ_BOT:
                    try:
                        qqbot.alert_admin(alert_payload)
                        # Send Wechat message to alert admin
                        wechatbot.send_wechat_message(alert_payload)
                    except Exception as e:
                        print('FATAL ERROR')
                        print(e)
                else:
                    print(alert_payload)
    # Send summary to admin
    summary = 'Success username: ' + '、'.join(successed_users) + ' Total time: {:.1f}s'.format(time.time() - begin_time)
    if USE_SVC:
        wechatbot.send_wechat_message(summary)
    if USE_QQ_BOT:
        qqbot.alert_admin(summary)
        # Release mirai session
        qqbot.release_session()