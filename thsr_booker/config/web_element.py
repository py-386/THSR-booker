# cookie alert
accept_cookie_btn = "//*[@id='cookieAccpetBtn']"


# select ticket info
departure_station_dropdown = "//select[@class='uk-select'][@name='selectStartStation']"
destination_station_dropdown = (
    "//select[@class='uk-select'][@name='selectDestinationStation']"
)
departure_time = "//select[@name='toTimeTable']"
departure_date = "//input[@class='uk-input' and @readonly='readonly']"


# captcha
captcha_img = "//img[@id='BookingS1Form_homeCaptcha_passCode']"
captcha_input = "//input[@id='securityCode']"
submit_btn = "//*[@id='SubmitButton']"
captcha_failed = "//span[@class='feedbackPanelERROR']"
reload_captcha = "//button[@class='btn-reload']"
train_query_data_view_panel = "//div[@id='BookingS2Form_TrainQueryDataViewPanel']"


# train info
train_result = "//div[@class='result-listing']"
train_list = "//div[@class='result-listing']//label"
train_info = "//input[@class='uk-radio']"
confirm_ticket_btn = "//input[@name='SubmitButton']"


# ticket info
total_price = "//p[@id='TotalPrice']"
id_input = "//input[@id='idNumber']"
phone_number_input = "//input[@id='mobilePhone']"
e_mail_input = "//input[@id='email']"


# send booking
agree_rules_checkbox = "//input[@name='agree'][@type='checkbox']"
finish_booking = "//input[@id='isSubmit']"
ticket_summary = "//div[@class='ticket-summary']"
