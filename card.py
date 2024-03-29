#yibanPython.py 
import json
import os
import time
from captcha import Captcha
from selenium import webdriver

class Card:
    def __init__(self):
        # Set browser UA/Location/Frame size
        UA ="Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/4.9.4"
        mobileEmulation = {"deviceMetrics": {},"userAgent": UA}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        options.add_argument('--incognito')
        options.add_argument('appversion=4.9.5')
        options.add_argument('X-Requested-With=com.yiban.app')
        options.add_argument('headless')
        self.hour = time.strftime("%H", time.localtime())
        if self.hour in ['06','07','08']:
            self.exec_method = '晨检上报'
            self.frame_abbr = ['field_1588749561_2922','field_1588749738_1026','field_1588749759_6865','field_1588749842_2715']
        else:
            self.exec_method = '午检上报'
            self.frame_abbr = ['field_1588750276_2934','field_1588750304_5363','field_1588750323_2500','field_1588750343_3510']
        self.browser = webdriver.Chrome('chromedriver',options=options)
        self.params = {
            "latitude": 34.203139,
            "longitude": 108.923318,
            "accuracy": 100
        }

    def clock_yiban(self,account,session_url,location):
        browser = self.browser
        params = self.params
        browser.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
        # Login
        browser.set_window_size(428,926)
        try:
            # print(session_url)
            browser.get(session_url)

        except Exception as e:
            browser.quit()
            print('打开页面失败！尝试清空DNS缓存……')
            print(e)
            fDNS = os.system('ipconfig /flushdns')
            print(fDNS)
            return(False)
        time.sleep(3)
        return(self.main_process(browser,account,location))
    
    def clock_yiban_backup(self,account,password,phone,location):
        browser = self.browser
        params = self.params
        browser.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
        # Login
        browser.set_window_size(428,926)
        try:
            browser.get('http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/form.html')
            browser.find_element_by_id('oauth_uname_m').send_keys(phone)
            browser.find_element_by_id('oauth_upwd_m').send_keys(password)
            browser.find_element_by_xpath('/html/body/main/section[2]/div/div[4]/button').click()
            time.sleep(5)
            browser.get('http://f.yiban.cn/iapp610661')
            time.sleep(5)
            try:
                browser.find_element_by_xpath('/html/body/main/section[2]/div/div[2]/button').click()
            except:
                pass
            time.sleep(5)
            cur_url = browser.current_url
            self.update_url(account,cur_url)
            return(self.main_process(browser,account,location))
        except:
            print('备用方案执行失败！')
            return(False)

    def update_url(self,account,url):
        print('检测到备用方案已启用！正在更新Url')
        with open('accounts.json','r',encoding='utf-8') as _accounts:
            a_lst = json.load(_accounts)
            _accounts.close()
        for i in range(len(a_lst)):
            if a_lst[i]['userid'] == account:
                a_lst[i]['url'] = url
                print('已更新{}的url为: {}'.format(a_lst[i]['name'],url))
        with open('accounts.json','w',encoding='utf-8') as _accounts:
            json.dump(a_lst, _accounts)
            print('已写入账号文件！')
            _accounts.close()
    
    def main_process(self,browser_var,account,location):
        browser = browser_var
        try:
            # Open specific iap
            browser.find_element_by_xpath('//p[text()="' + self.exec_method + '"]').click()
            time.sleep(3)
        except:
            browser.quit()
            print('找不到签到入口，请检查信息录入是否正确！')
            return(False)
        # Did u already finished the process?
        try:
            browser.find_element_by_xpath('//a[text()="验证二维码"]')
            print('已经打过卡了！')
            if not os.path.exists('./images/'+ account + '.png'):
                try:
                    browser.get_screenshot_as_file('./images/'+ account + '.png')
                    print('已保存截图')
                except Exception as e:
                    print('由于以下错误，未能保存截图')
                    print(e)
            browser.delete_all_cookies()
            browser.quit()
            return(True)
        except: 
            try:
                print('还没有打卡，即将开始……')
                # Remove Layer
                browser.execute_script("document.getElementsByClassName('weui-mask_transparent')[0].style.display='none'")
                browser.execute_script("document.getElementsByClassName('weui-toast weui_loading_toast weui-toast--visible')[0].style.display='none'")
                # Remove read-only attribute
                time.sleep(1)
                for abbr in self.frame_abbr:
                    browser.execute_script("$('input[id=" + abbr + "]').removeAttr('readonly')")
                time.sleep(1)
                # Fill in blanks
                browser.find_element_by_id(self.frame_abbr[0]).send_keys('36.5')
                browser.find_element_by_id(self.frame_abbr[1]).send_keys(location)
                browser.find_element_by_id(self.frame_abbr[2]).send_keys('是')
                browser.find_element_by_id(self.frame_abbr[3]).send_keys('否')
                print('已填写个人信息')
                time.sleep(5)
                # Bypass Captcha
                captcha_encrypted = browser.find_element_by_id('captcha').get_attribute('src')
                captcha_result = Captcha().decrypt_captcha(captcha_encrypted, 1902)
                browser.find_element_by_id('yanzhengma').send_keys(captcha_result['pic_str'])
                check = browser.find_element_by_id('weuiAgree')
                browser.execute_script("arguments[0].value = 1", check)
                #Submit
                time.sleep(1)
                browser.find_element_by_id('btn').click()
                time.sleep(3)
                try:
                    browser.get_screenshot_as_file('./images/'+ account + '.png')
                    print('已保存截图')
                except Exception as e:
                    print('由于以下错误，未能保存截图')
                    print(e)
                try:
                    time.sleep(10)
                    browser.find_element_by_xpath('//a[text()="验证二维码"]')
                    print('打卡成功！')
                    browser.delete_all_cookies()
                    browser.quit()
                    return(True)
                except:
                    print('提交失败！')
                    return(False)
            except:
                print('遇到了问题')
                browser.quit()
                return(False)