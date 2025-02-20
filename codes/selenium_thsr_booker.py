import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用
from ocr import get_captcha_code

driver = webdriver.Chrome() 

driver.get('https://irs.thsrc.com.tw/IMINT/')

driver.implicitly_wait(2)

acc_button = driver.find_element(by=By.ID, value='cookieAccpetBtn')
time.sleep(1)
acc_button.click() # 按按鈕

#下拉式選單
#出發站
start_dropdown = driver.find_element(By.XPATH, "//select[@class='uk-select' and @name='selectStartStation']")  #找下拉選單
start_select = Select(start_dropdown)
start_select.select_by_visible_text('台中')

#抵達站
destination_dropdown = driver.find_element(By.XPATH, "//select[@class='uk-select' and @name='selectDestinationStation']")
destination_select = Select(destination_dropdown)
destination_select.select_by_visible_text('台北')

#出發時間
to_time_dropdown = driver.find_element(By.NAME, 'toTimeTable')
to_time_select = Select(to_time_dropdown)
to_time_select.select_by_visible_text('06:30')

#出發日期
driver.find_element(By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()
time.sleep(1)

start_date = "二月 21, 2025"
driver.find_element(By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']").click()

#驗證碼-圖
captcha_img = driver.find_element(by=By.ID, value='BookingS1Form_homeCaptcha_passCode')
captcha_img.screenshot('captcha.png') #截圖存成檔案

#ocr 辨識
captcha_code = get_captcha_code()

#填入驗證碼

captcha_input = driver.find_element(By.ID, 'securityCode')
captcha_input.send_keys(captcha_code) #輸入驗證碼


#開始查詢

driver.find_element(By.ID, 'SubmitButton').click()


time.sleep(5)
driver.quit()



