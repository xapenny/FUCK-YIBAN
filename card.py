#yibanPython.py 
import os
import sys
import time
from captcha import Captcha
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Card:
    def __init__(self):
        # Set browser UA/Location/Frame size
        UA ="Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 yiban_android"
        mobileEmulation = {"deviceMetrics": {},"userAgent": UA}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        options.add_argument('appversion=4.9.5')
        options.add_argument('X-Requested-With= com.yiban.app')
        self.browser = webdriver.Chrome('chromedriver.exe',options=options)
        self.params = {
            "latitude": 34.203139,
            "longitude": 108.923318,
            "accuracy": 100
        }

    def clock_yiban(self,account,password,location):
        browser = self.browser
        params = self.params
        browser.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
        # Login
        browser.get('http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/form.html')
        browser.find_element_by_id('oauth_uname_w').send_keys(account)
        browser.find_element_by_id('oauth_upwd_w').send_keys(password)
        browser.find_element_by_css_selector('.oauth_check_login').click()
        # wait for redirection
        element = WebDriverWait(browser,20).until(EC.url_matches('yiban.sust.edu.cn'))
        time.sleep(3)
        browser.get("http://f.yiban.cn/iapp610661")
        browser.set_window_size(414,896)
        # Open specific iap
        browser.find_element_by_xpath('//p[text()="寒假信息上报"]').click()
        time.sleep(3)
        # Did u already finished the process?
        try:
            success_value = browser.find_element_by_xpath('//a[text()="验证二维码"]')
            print('Already done...')
            if not os.path.exists('./images/'+ account + '.png'):
                try:
                    browser.get_screenshot_as_file('./images/'+ account + '.png')
                    print('Saved screenshot!')
                except Exception as e:
                    print('Failed to save screenshot!')
                    print(e)
            browser.quit()
            return(0)
        except: 
            print('Haven\'t done yet...')
            # Remove Layer
            browser.execute_script("document.getElementsByClassName('weui-mask_transparent')[0].style.display='none'")
            browser.execute_script("document.getElementsByClassName('weui-toast weui_loading_toast weui-toast--visible')[0].style.display='none'")
            # Remove read-only attribute
            browser.execute_script("$('input[id=field_1587635120_1722]').removeAttr('readonly')")
            browser.execute_script("$('input[id=field_1587635142_8919]').removeAttr('readonly')")
            browser.execute_script("$('input[id=field_1587635252_7450]').removeAttr('readonly')")
            browser.execute_script("$('input[id=field_1587635509_7740]').removeAttr('readonly')")
            browser.execute_script("$('input[id=field_1587998777_8524]').removeAttr('readonly')")
            time.sleep(1)
            # Fill in blanks
            browser.find_element_by_id('field_1587635120_1722').send_keys('36.5')
            #browser.find_element_by_id('field_1587635120_1722').click()
            browser.find_element_by_id('field_1587635142_8919').send_keys('正常')
            browser.find_element_by_id('field_1587635252_7450').send_keys(location)
            browser.find_element_by_id('field_1587635509_7740').send_keys('否')
            browser.find_element_by_id('field_1587998777_8524').send_keys('否')
            print('filled!')
            time.sleep(1)
            # Bypass Captcha
            captcha_bypass = Captcha()
            captcha_encrypted = browser.find_element_by_id('captcha').get_attribute('src')
            captcha_result = captcha_bypass.decrypt_captcha(captcha_encrypted)
            browser.find_element_by_id('yanzhengma').send_keys(captcha_result)
            check = browser.find_element_by_id('weuiAgree')
            browser.execute_script("arguments[0].value = 1", check)
            #Submit
            time.sleep(1)
            browser.find_element_by_id('btn').click()
            time.sleep(3)
            try:
                browser.get_screenshot_as_file('./images/'+ account + '.png')
                print('Saved screenshot!')
            except Exception as e:
                print('Failed to save screenshot!')
                print(e)
            return(0)