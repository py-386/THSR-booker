import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException #for the while loop #把抓不到元素的Exception 抓下來
import os

# my tools
from codes.tools.ocr import get_captcha_code


def create_driver():
    options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
    options.add_argument("--disable-blink-features=AutomationControlled") #把 AutomationControlled(自動測試) 的 features 關掉
    options.add_argument("--incognito") #無痕
    global driver
    driver = webdriver.Chrome(options=options)
    driver.get('https://irs.thsrc.com.tw/IMINT/')
    driver.implicitly_wait(2)

def driver_quit():
    driver.quit()

def booking_with_info(start_station, dest_station, start_time, start_date):
    ### 第一個頁面
    accept_cookie_button = driver.find_element(by=By.ID, value='cookieAccpetBtn')
    # time.sleep(0.5)
    accept_cookie_button.click()
    # time.sleep(0.5)

    #下拉式選單
    #出發站
    start_dropdown = driver.find_element(By.XPATH, "//select[@class='uk-select' and @name='selectStartStation']")  #找下拉選單
    start_select = Select(start_dropdown)
    start_select.select_by_visible_text(start_station)
    time.sleep(0.5)

    #抵達站
    destination_dropdown = driver.find_element(By.XPATH, "//select[@class='uk-select' and @name='selectDestinationStation']")
    destination_select = Select(destination_dropdown)
    destination_select.select_by_visible_text(dest_station)
    time.sleep(0.5)

    #出發時間
    start_time_dropdown = driver.find_element(By.NAME, 'toTimeTable')
    start_time_select = Select(start_time_dropdown)
    start_time_select.select_by_visible_text(start_time)
    time.sleep(0.5)

    #出發日期
    driver.find_element(By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()
    time.sleep(1)
    driver.find_element(By.XPATH,
            f"//span[(@class='flatpickr-day' or @class='flatpickr-day today selected') and @aria-label='{start_date}']").click()


    while True:
        #驗證碼-截圖
        captcha_img = driver.find_element(by=By.ID, value='BookingS1Form_homeCaptcha_passCode')
        captcha_img.screenshot('captcha.png') #截圖存成檔案

        #ocr 辨識
        captcha_code = get_captcha_code()
        time.sleep(1)

        #填入驗證碼
        captcha_input = driver.find_element(By.ID, 'securityCode')
        captcha_input.send_keys(captcha_code) #輸入驗證碼
        # time.sleep(1)

        #開始查詢
        driver.find_element(By.ID, 'SubmitButton').click()

        time.sleep(1)

        # check validation is success or not
        try:
            time.sleep(3)
            driver.find_element(by=By.ID, value='BookingS2Form_TrainQueryDataViewPanel') #第二頁的元素，要檢查兩頁有沒有重複的ID
            print("驗證碼正確，進到第二頁面")
            break
        except NoSuchElementException:
            print("驗證碼錯誤，重新嘗試")
            continue

    # 第二個頁面 (認證完後進入下個頁面)

    trains_info = list()
    trains = driver.find_element(
        By.CLASS_NAME, 'result-listing').find_elements(by=By.TAG_NAME, value='label')

    for train in trains:
        info = train.find_element(By.CLASS_NAME, 'uk-radio')
        trains_info.append(
            {
                'depart_time': info.get_attribute('querydeparture'),
                'arrival_time': info.get_attribute('queryarrival'),
                'duration': info.get_attribute('queryestimatedtime'),
                'train_code': info.get_attribute('querycode'),
                'radio_box': info,
            }
        ) # 前面都是加文字，只有raio_box 是 整個屬性，因為到時候選擇時還會用到
        

    # show trains codes
    for counter, train in enumerate(trains_info):
        print(f"""{counter:>3}. - {train['train_code']:>4} 車次，
            行駛時間: {train['duration']}， {train['depart_time']} -> {train['arrival_time']}""")

    return trains_info

def select_train_and_submit_booking(trains_info, booking_info, which_train=None):

    if which_train is None:
        #如果沒有選擇車次，則由使用者選擇(一般程式的執行流程，採用用CMD輸入)
        which_train = int(input("Choose your train. Enter from 0~9 : "))

    trains_info[which_train]['radio_box'].click()

    booking_info['train_code'] = trains_info[which_train]['train_code']

    # Submit booking requests 
    driver.find_element(by=By.NAME, value='SubmitButton').click()

    total_price = driver.find_element(by=By.ID, value='TotalPrice').text
    price = (total_price.split(' '))[-1]
    booking_info['price'] = int(price)
    print(booking_info)
    ###第三個頁面
    driver.find_element(
            By.CLASS_NAME, 'ticket-summary').screenshot('thsr_summary.png')

    #取票人資訊

    # ID_code_dropdown = driver.find_element(By.ID, 'idInputRadio')
    # ID_code_select = Select(ID_code_dropdown)
    # id_choose = input("0. 身分證字號  1. 護照/居留證/入出境許可證號碼 : ")
    # ID_code_select.select_by_value(id_choose)

    user_name = input("請輸入姓名 : ")

    personal_id = input("請輸入證號 : ")
    personal_id_box = driver.find_element(by=By.ID, value='idNumber')
    # personal_id = os.getenv('PERSONAL_ID')
    personal_id_box.send_keys(personal_id)
    


    user_phone_number = input("手機號碼或市話 : ")
    phone_number_box = driver.find_element(by=By.ID, value='mobilePhone')
    # user_phone_number = os.getenv('PERSONAL_PHONE_NUMBER')
    phone_number_box.send_keys(user_phone_number)

    user_email = input("請輸入你的 e-mail (選填) : ")
    email_box = driver.find_element(by=By.ID, value='email')
    # user_email = os.getenv('PERSONAL_EMAIL')
    email_box.send_keys(user_email)
    if user_email == "":
        user_email = None

    booking_info.update({
                        'user_phone_number': user_phone_number,
                        'user_email': user_email,
                        'user_name': user_name})

    print(booking_info)

    # time.sleep(1000)

    ##同意訂位提交按鈕
    # time.sleep(0.5)
    driver.find_element(by=By.XPATH, value="//input[@name='agree' and @class='uk-checkbox']").click()
    # time.sleep(1000)
    driver.find_element(by=By.ID, value='isSubmit').click()

    screenshot_filename = 'thsr_booking_result.png'
    driver.find_element(
        By.CLASS_NAME, 'ticket-summary').screenshot(screenshot_filename)
    print("\n訂票完成! 請在期限內繳款\n")

    driver.quit()
    return booking_info




