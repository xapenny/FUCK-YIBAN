import jieba
from numpy import packbits
from selenium import webdriver

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
            info = [True,{'name':username, 'url':url, 'userid':userid, 'userqq':userqq, 'password':password, 'phone':phone}]
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

if __name__ == '__main__':
    # 账号设置
    account_list = []
    input('按回车键开始设置打卡脚本，请在接下来弹出的窗口中登陆易班账号。登陆完成后在本窗口按回车键继续。')
    result = [True]
    while result[0]:
        result = Initialize().init()
        account_list.append(result[1])
        result[0] = confirm('添加其他账号吗')
    with open('account.json','w') as accounts_file:
        accounts_file.write(str(tuple(account_list)))
        accounts_file.close()
    # 其他设置
    input('\n\n接下来，我们将设置其他部分(按回车键继续)')
    settings_list = []
    use_qqbot = confirm('使用QQ机器人吗')
    if use_qqbot:
        if confirm('使用Mirai(Y)还是小栗子(N)作为机器人框架'):
            use_qqbot = 1
            # Mirai 狗都不用
        else:
            use_qqbot = 2
            # 设置小栗子框架
            botqq = input('请设置机器人的QQ号：')
            adminqq = input('请设置管理员的QQ号：')
            botauthkey = input('请输入为机器人设置的authkey：')
            botaddr = input('请输入机器人的连接地址(以http://开头)：')
            settings_list.append({'USE_QQBOT':use_qqbot,'botqq':botqq,'adminqq':adminqq,'botauthkey':botauthkey,'botaddr':botaddr})
    else:
        settings_list.append({'USE_QQBOT':use_qqbot})
    # 设置微信推送
    use_svc = confirm('使用微信推送(Server酱)吗')
    if use_svc:
        svc_key = input('请输入Server酱的SCKEY：')
        settings_list.append({'USE_SVC':use_svc,'svc_key':svc_key})
    else:
        settings_list.append({'USE_SVC':use_svc})
    # 设置Bark推送
    use_bark = confirm('使用Bark推送(仅iOS)吗')
    if use_bark:
        bark_push_key = input('请输入 Bark Push Key：')
        settings_list.append({'USE_BARK':use_bark,'bark_key':bark_push_key})
    else:
        settings_list.append({'USE_BARK':use_bark})
    # 设置验证码识别
    print('接下来将设置验证码识别api')
    captcha_username = input('请输入CYY验证码识别平台用户名：')
    captcha_passwd = input('请输入密码：')
    captcha_softid = input('请输入softid：')
    settings_list.append({'captcha_username':captcha_username,'captcha_passwd':captcha_passwd,'captcha_softid':captcha_softid})
    with open('settings.json','w') as settings:
        settings.write(str(tuple(settings_list)))
        settings.close()
    

