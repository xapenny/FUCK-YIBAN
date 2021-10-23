import jieba
import json
from numpy import packbits, save
from selenium import webdriver
from selenium.webdriver.remote import switch_to

class Initialize:
    def __init__(self):
        # Set browser UA/Location/Frame size
        UA ="Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 yiban_android"
        mobileEmulation = {"deviceMetrics": {},"userAgent": UA}
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('appversion=4.9.5')
        options.add_argument('X-Requested-With=com.yiban.app')
        self.browser = webdriver.Chrome('chromedriver',options=options)


    def init(self):
        browser = self.browser
        browser.set_window_size(428,926)
        browser.get('https://www.yiban.cn/login?go=http://f.yiban.cn/iapp610661')
        i = input('确定可以看见两个打卡的选项就可以在这里按回车键了，如果显示请重新登陆请输入error后回车，并在新的窗口中重新登录')
        if i == 'error':
            browser.quit()
            return([i])
        else:
            package = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]').text
            a = jieba.lcut(package)
            username = a[2]
            userid = a[-2]
            url = browser.current_url
            phone = input('请输入该用户的用户名(一般为手机号，用于备用方案)：')
            password = input('请输入该用户的密码(用于备用方案)：')
            userqq = input('请输入该用户的QQ号：')
            location = input('请输入地址(留空使用学校地址)：')
            if location == '':
                location = '陕西省西安市未央区龙朔路靠近陕西科技大学学生生活区'
            info = {'name':username, 'enable':1, 'location':location, 'url':url, 'userid':userid, 'userqq':userqq, 'password':password, 'phone':phone}
            browser.quit()
            return(info)

def confirm(question):
        result = input('请问还需要{}？(Y/N)'.format(question))
        while result not in ['y','n','Y','N']:
                result = input('输入错误！请重新输入！(Y/N)')
        if result in ['y','Y']:
            return True
        elif result in ['n','N']:
            return False

def save_data(file, data: dict):
    with open(file, 'w', encoding='utf-8') as target_file:
        json.dump(data, target_file)
        target_file.close()

def read_data(file):
    with open(file, 'r', encoding='utf-8') as target_file:
        _var = json.load(target_file)
        target_file.close()
    return _var

class Account:
    def __init__(self):
        try:
            self.account_list = read_data('accounts.json')
            print('\n[i]成功读取数据！\n')
            print('当前已经保存的数据 (共{}条)：\n'.format(len(self.account_list)))
            for i in range(len(self.account_list)):
                print('[{}] 姓名：{:<4}\t已启用：{}\n'.format(i, self.account_list[i]['name'], bool(self.account_list[i]['enable'])))
            print('\n')
        except:
            self.account_list = []
            print('\n[x]读取数据失败！\n')

    def info(self):
        input('\n按回车继续……')

    def add(self):
        input('按回车键开始设置打卡脚本，请在接下来弹出的窗口中登陆易班账号。登陆完成后在本窗口按回车键继续。')
        _add_new = [True]
        while _add_new:
            result = Initialize().init()
            self.account_list.append(result)
            _add_new = confirm('添加其他账号吗')
        save_data('accounts.json', self.account_list)

    def edit(self):
        account = input('请输入想编辑的用户编号：')
        try:
            if int(account) in range(len(self.account_list)):
                i = int(account)
                print('[1]姓名：\t{}\n[!]已启用：\t{}\n[2]学号：\t{}\n[3]手机号：\t{}\n[4]QQ号：\t{}\n[5]密码：\t{}\n[6]地址：\t{}\n'.format(self.account_list[i]['name'], bool(self.account_list[i]['enable']), self.account_list[i]['userid'], self.account_list[i]['phone'], self.account_list[i]['userqq'], self.account_list[i]['password'], self.account_list[i]['location']))
                opt_e = input('请输入想修改的项目编号：')
                if int(opt_e) in range(7):
                    if opt_e == '1':
                        self.account_list[i]['name'] = input('请输入新的姓名：')
                    elif opt_e == '2':
                        self.account_list[i]['userid'] = input('请输入新的学号：')
                    elif opt_e == '3':
                        self.account_list[i]['phone'] = input('请输入新的手机号：')
                    elif opt_e == '4':
                        self.account_list[i]['userqq'] = input('请输入新的QQ号：')
                    elif opt_e == '5':
                        self.account_list[i]['password'] = input('请输入新的密码：')
                    elif opt_e == '6':
                        self.account_list[i]['location'] = input('请输入新的地址：')
                    else:
                        print('输入错误！请重新输入！')
                    print('[1]姓名：{:>4}\t已启用：{}\n[2]学号：{:>4}\n[3]手机号：{:>4}\n[4]QQ号：{:>4}\n[5]密码：{:>4}\n[6]地址：{:>4}\n'.format(self.account_list[i]['name'], bool(self.account_list[i]['enable']), self.account_list[i]['userid'], self.account_list[i]['phone'], self.account_list[i]['userqq'], self.account_list[i]['password'], self.account_list[i]['location']))
                    j = input('上面是修改后的数据，确定修改输入1')
                    if j == '1':
                        save_data('accounts.json', self.account_list)
        except:
            input('遇到了一些问题，可能是输入错误！\n')

    def delete(self):
        account = input('请输入想删除的用户编号：')
        try:
            if int(account) in range(len(self.account_list)):
                del self.account_list[int(account)]
                print('成功删除数据！\n')
                save_data('accounts.json', self.account_list)
        except:
            input('遇到了一些问题，可能是输入错误！\n')

    def status(self, status):
        account = input('请输入想启用/禁用的用户编号：')
        try:
            if int(account) in range(len(self.account_list)):
                self.account_list[int(account)]['enable'] = status
                print('成功修改账号状态！\n')
                save_data('accounts.json', self.account_list)
        except:
            input('遇到了一些问题，可能是输入错误！\n')

def initialize():
    # 账号设置s
    Account().add()
    # 其他设置
    input('\n\n接下来，我们将设置其他部分(按回车键继续)')
    settings_dict = {}
    use_qqbot = confirm('使用QQ机器人吗')
    settings_dict['qq'] = {}
    if use_qqbot:
        if confirm('使用Mirai(Y)还是小栗子(N)作为机器人框架'):
            settings_dict['qq']['USE_QQBOT'] = 1
            # 设置 MAH
            settings_dict['qq']['botqq'] = input('请设置机器人的QQ号：')
            settings_dict['qq']['adminqq'] = input('请设置管理员的QQ号：')
            settings_dict['qq']['botauthkey'] = input('请输入为机器人设置的authkey：')
            settings_dict['qq']['botaddr'] = input('请输入机器人的连接地址(以http://开头)：')
        else:
            settings_dict['qq']['USE_QQBOT'] = 2
            # 设置小栗子HA
            settings_dict['qq']['botqq'] = input('请设置机器人的QQ号：')
            settings_dict['qq']['adminqq'] = input('请设置管理员的QQ号：')
            settings_dict['qq']['botauthkey'] = input('请输入为机器人设置的authkey：')
            settings_dict['qq']['botpass'] = input('请输入为机器人设置的连接密码：')
            settings_dict['qq']['botaddr'] = input('请输入机器人的连接地址(以http://开头)：')
    else:
        settings_dict['qq']['USE_QQBOT'] = use_qqbot
    # 设置微信推送
    settings_dict['wechat'] = {}
    settings_dict['wechat']['USE_SVC'] = confirm('使用微信推送(Server酱)吗')
    if settings_dict['wechat']['USE_SVC']:
        settings_dict['wechat']['svc_key'] = input('请输入Server酱的SCKEY：')
    # 设置Bark推送
    settings_dict['bark'] = {}
    settings_dict['bark']['USE_BARK'] = confirm('使用Bark推送(仅iOS)吗')
    if settings_dict['bark']['USE_BARK']:
        settings_dict['bark']['bark_key'] = input('请输入 Bark Push Key：')
    # 设置验证码识别
    print('接下来将设置验证码识别api')
    settings_dict['captcha'] = {}
    settings_dict['captcha']['username'] = input('请输入CYY验证码识别平台用户名：')
    settings_dict['captcha']['password']  = input('请输入密码：')
    settings_dict['captcha']['softid']  = input('请输入softid：')
    save_data('settings.json', settings_dict)

if __name__ == '__main__':
    while True:
        print('打卡信息管理'.center(30,'*'))
        print('1.初始化\t2.添加账号\n3.编辑账号\t4.删除账号\n5.禁用账号\t6.启用账号\n7.账号信息\t8.退出')
        opt = input('请输入选项：')
        if opt == '1':
            initialize()
        elif opt == '2':
            Account().add()
        elif opt == '3':
            Account().edit()
        elif opt == '4':
            Account().delete()
        elif opt == '5':
            Account().status(0)
        elif opt == '6':
            Account().status(1)
        elif opt == '7':
            Account().info()
        elif opt == '8':
            break
        else:
            input('输入错误！请重新输入！\n')