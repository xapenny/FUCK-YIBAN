#yibanPython.py 
import os
import time
from captcha import Captcha
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Card:
    def __init__(self):
        # Set browser UA/Location/Frame size
        UA ="Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 yiban_android"
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
        self.browser = webdriver.Chrome('chromedriver.exe',options=options)
        self.params = {
            "latitude": 34.203139,
            "longitude": 108.923318,
            "accuracy": 100
        }

    def clock_yiban(self,account,session_url):
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
            return(1)
        time.sleep(3)
        try:
            # Open specific iap
            browser.find_element_by_xpath('//p[text()="' + self.exec_method + '"]').click()
            time.sleep(3)
        except:
            browser.quit()
            print('找不到签到入口，请检查信息录入是否正确！')
            return(1)
        # Did u already finished the process?
        try:
            success_value = browser.find_element_by_xpath('//a[text()="验证二维码"]')
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
            return(0)
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
                print(self.frame_abbr[0])
                browser.find_element_by_id(self.frame_abbr[0]).send_keys('36.5')
                browser.find_element_by_id(self.frame_abbr[1]).send_keys('陕西省西安市未央区龙朔路靠近陕西科技大学学生生活区')
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
                browser.delete_all_cookies()
                browser.quit()
                return(0)
            except:
                print('遇到了问题')
                return(1)