#yibanPython.py 
import time
import captcha
import accounts
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set browser UA/Location/Frame size
UA ="Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 yiban_android"
mobileEmulation = {"deviceMetrics": {},"userAgent": UA}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)
options.add_argument('appversion=4.9.5')
options.add_argument('X-Requested-With= com.yiban.app')
browser = webdriver.Chrome('chromedriver.exe',options=options)
params = {
    "latitude": 34.203139,
    "longitude": 108.923318,
    "accuracy": 100
}
browser.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
# Login
browser.get('http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/form.html')
browser.find_element_by_id('oauth_uname_w').send_keys(accounts.account)
browser.find_element_by_id('oauth_upwd_w').send_keys(accounts.password)
browser.find_element_by_css_selector('.oauth_check_login').click()
# wait for redirection
element = WebDriverWait(browser,20).until(EC.url_matches('yiban.sust.edu.cn'))
time.sleep(3)
browser.get("http://f.yiban.cn/iapp610661")
browser.set_window_size(414,896)
# Open specific iap
browser.find_element_by_xpath('//p[text()="寒假信息上报"]').click()
time.sleep(3)
# Remove Layer
try:
    layer = browser.find_element_by_class_name('weui-mask_transparent')
    browser.execute_script("arguments[0].removeAttribute(argument[1])",layer)
except(NoSuchElementException):
    print('已经打过卡了')
    browser.quit()
# Fill in blanks
browser.find_element_by_id('field_1587635120_1722').send_keys('36.5')
browser.find_element_by_id('field_1587635142_8919').send_keys('正常')
browser.find_element_by_id('field_1587635252_7450').send_keys('YOUR LOCATION')
browser.find_element_by_id('field_1587635509_7740').send_keys('否')
browser.find_element_by_id('field_1587998777_8524').send_keys('否')
time.sleep(60)
# Bypass Captcha
captcha_encrypted = browser.find_element_by_class_name('captcha').get_attribute('src')
captcha_result = captcha.main(captcha_encrypted)
browser.find_element_by_id('yanzhengma').send_keys(captcha_result)
check = browser.find_element_by_id('weuiAgree')
browser.execute_script("arguments[0].value = 1", check)
#Submit
browser.find_element_by_id('btn').click()