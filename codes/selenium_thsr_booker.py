import time

# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 下拉式選單使用
from selenium.common.exceptions import NoSuchElementException
from ocr import get_captcha_code
from pprint import pprint

import constants
import web_element
from util import inatall_driver
from execute import Driver


inatall_driver()
driver = Driver(driver_arg=constants.CHROME_DRIVER_ARGS)
driver.go_to_url(constants.THST_URL)


### 第一個頁面
# acc_button = driver.find_element(by=By.XPATH, value=(web_element.accapt_acckie_btn))
# acc_button.click()
# acc_button = driver.find_element(by=By.ID, value="cookieAccpetBtn")
# time.sleep(1)
# acc_button.click()
# time.sleep(1)
driver.wait_element_visible_and_click(xpath=web_element.accapt_acckie_btn)

# 下拉式選單
# 出發站
# start_dropdown = driver.find_element(
#     By.XPATH, "//select[@class='uk-select' and @name='selectStartStation']"
# )  # 找下拉選單

# start_select = Select(start_dropdown)
# start_select.select_by_visible_text("台中")
# time.sleep(1)
driver.select_item_in_menu(menu=web_element.start_dropdown, target_text="台中")

# 抵達站
# destination_dropdown = driver.find_element(
#     By.XPATH, "//select[@class='uk-select' and @name='selectDestinationStation']"
# )
# destination_select = Select(destination_dropdown)
# destination_select.select_by_visible_text("台北")
# time.sleep(1)
driver.select_item_in_menu(menu=web_element.destination_dropdown, target_text="台北")


# 出發時間
to_time_dropdown = driver.find_element(By.NAME, "toTimeTable")
to_time_select = Select(to_time_dropdown)
to_time_select.select_by_visible_text("10:30")
time.sleep(1)

# 出發日期
driver.find_element(
    By.XPATH, "//input[@class='uk-input' and @readonly='readonly']"
).click()
time.sleep(1)

start_date = "二月 25, 2025"
driver.find_element(
    By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']"
).click()

while True:
    # 驗證碼-截圖
    captcha_img = driver.find_element(
        by=By.ID, value="BookingS1Form_homeCaptcha_passCode"
    )
    captcha_img.screenshot("captcha.png")  # 截圖存成檔案

    # ocr 辨識
    captcha_code = get_captcha_code()

    # 填入驗證碼
    captcha_input = driver.find_element(By.ID, "securityCode")
    captcha_input.send_keys(captcha_code)  # 輸入驗證碼
    time.sleep(2)

    # 開始查詢
    driver.find_element(By.ID, "SubmitButton").click()

    time.sleep(2)

    # check validation is success or not
    try:
        time.sleep(3)
        driver.find_element(
            by=By.ID, value="BookingS2Form_TrainQueryDataViewPanel"
        )  # 第二頁的元素，要檢查兩頁有沒有重複的ID
        print("驗證碼正確，進到第二頁面")
        break
    except NoSuchElementException:
        print("驗證碼錯誤，重新嘗試")
        continue


# 第二個頁面 (認證完後進入下個頁面)

trains_info = list()
trains = driver.find_element(By.CLASS_NAME, "result-listing").find_elements(
    by=By.TAG_NAME, value="label"
)

for train in trains:
    info = train.find_element(By.CLASS_NAME, "uk-radio")
    trains_info.append(
        {
            "depart_time": info.get_attribute("querydeparture"),
            "arrival_time": info.get_attribute("queryarrival"),
            "duration": info.get_attribute("queryestimatedtime"),
            "train_code": info.get_attribute("querycode"),
            "radio_box": info,
        }
    )  # 前面都是加文字，只有raio_box 是 整個屬性，因為到時候選擇時還會用到


# Choose train

for counter, train in enumerate(trains_info):
    print(
        f"{counter+1:>3}. - {train['train_code']:>4} 車次， 行駛時間: {train['duration']}， {train['depart_time']} -> {train['arrival_time']}"
    )

which_train = int(input("Choose your train. Enter from 1~10 : "))
trains_info[(which_train - 1)]["radio_box"].click()


# Submit booking requests

driver.find_element(by=By.NAME, value="SubmitButton").click()


# 顯示票價及擷取車票資訊
total_price = driver.find_element(by=By.ID, value="TotalPrice").text
print(f"\n你的票價為 {total_price} 元\n")


###第三個頁面

# 取票人資訊

ID_code_dropdown = driver.find_element(By.ID, "idInputRadio")
ID_code_select = Select(ID_code_dropdown)
id_choose = input("0. 身分證字號  1. 護照/居留證/入出境許可證號碼 : ")
ID_code_select.select_by_value(id_choose)

id_numbers = input("請輸入證號 : ")
id_numbers_box = driver.find_element(by=By.ID, value="idNumber")
id_numbers_box.send_keys(id_numbers)

phonenumber = input("手機號碼或市話 (選填) : ")
phone_number_box = driver.find_element(by=By.ID, value="mobilePhone")
phone_number_box.send_keys(phonenumber)

email = input("請輸入你的 e-mail (選填) : ")
email_box = driver.find_element(by=By.ID, value="email")
email_box.send_keys(email)

time.sleep(5)
driver.find_element(
    by=By.XPATH, value="//input[@name='agree' and @class='uk-checkbox']"
).click()

##訂位提交按鈕
time.sleep(3)
driver.find_element(by=By.ID, value="isSubmit").click()


driver.find_element(By.CLASS_NAME, "ticket-summary").screenshot(
    "thsr_booking_result.png"
)
print("\n訂票完成! 請在期限內繳款\n")


time.sleep(5)
driver.quit()
