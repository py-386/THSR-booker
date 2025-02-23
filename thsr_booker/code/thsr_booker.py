import time

from thsr_booker.config import constants, web_element
from thsr_booker.config.models import TrainInfo, UserInfo, UserRequirements
from thsr_booker.code.execute import Driver
from thsr_booker.code.ocr import get_captcha_code
from thsr_booker.code.util import read_yaml_file


def setup_user_info() -> UserInfo:
    return UserInfo(
        **read_yaml_file(file_name=constants.USER_INFO_FILE).get("user_info")
    )


def setup_user_requirements() -> UserRequirements:
    # mock
    # TODO -> get user requirements
    return UserRequirements(
        departure_station="台中",
        destination_station="台北",
        date="二月 25, 2025",
        time="10:30",
    )


class THSR_BOOKER(Driver):
    def __init__(self, driver_arg):
        Driver.__init__(self, driver_arg=driver_arg)

    def go_to_homw_page(self) -> None:
        self.go_to_url(constants.THST_URL)
        self._accept_cookie()

    def check_captcha(self) -> None:
        while True:
            self._save_captcha_img()
            self._input_captcha_code(get_captcha_code())
            self.wait_element_visible_and_click(web_element.submit_btn)
            if self._check_captcha_result():
                break
            time.sleep(1.5)

    def select_requirements_info(self, requirements: UserRequirements):
        self._select_departure_station(requirements.departure_station)
        self._select_destination_station(requirements.destination_station)
        self._select_departure_time(requirements.time)
        self._select_departure_date(requirements.date)

    def get_train_info(self) -> dict[int, TrainInfo]:
        train_list = self.wait_elements_visible(xpath=web_element.train_list)
        return {
            index + 1: self._parser_train_info(index=index + 1)
            for index, _ in enumerate(train_list)
        }

    def show_ticket_info(self) -> None:
        # TODO -> show other info
        total_price = self.get_element_text(xpath=web_element.total_price)
        print(f"\n你的票價為 {total_price} 元\n")

    def select_ticket(self, train_info: dict[int, TrainInfo]) -> None:
        self._show_train_info(train_info)
        index: int = int(input("Choose your train. Enter from 1~10 : "))
        if target_train := train_info.get(index):
            target_train.radio_box.click()
        self._confirm_ticket()

    def input_user_info(self, user_info: UserInfo) -> None:
        # TODO -> 身分證字號 or 護照/居留證/入出境許可證號碼
        self.input_text(xpath=web_element.id_input, text=user_info.id)
        self.input_text(
            xpath=web_element.phone_number_input, text=user_info.phone_number
        )
        self.input_text(xpath=web_element.e_mail_input, text=user_info.e_mail)

    def submit_booking(self):
        self._click_agree_rules_checkbox()
        self._click_finish_button()
        self._confirm_booking_results()

    def _accept_cookie(self) -> None:
        self.wait_element_visible_and_click(xpath=web_element.accept_cookie_btn)

    def _select_departure_station(self, departure_station: str) -> None:
        self.select_item_in_menu(
            menu=web_element.departure_station_dropdown, target_text=departure_station
        )

    def _select_destination_station(self, destination_staion: str) -> None:
        self.select_item_in_menu(
            menu=web_element.destination_station_dropdown,
            target_text=destination_staion,
        )

    def _select_departure_time(self, departure_time: str) -> None:
        self.select_item_in_menu(
            menu=web_element.departure_time, target_text=departure_time
        )

    def _select_departure_date(self, departure_date: str) -> None:
        date_xpath = (
            f"//span[@class='flatpickr-day' and @aria-label='{departure_date}']"
        )
        self.wait_element_visible_and_click(xpath=web_element.departure_date)
        self.wait_element_visible_and_click(xpath=date_xpath)

    def _input_captcha_code(self, captcha_code: str) -> None:
        self.input_text(xpath=web_element.captcha_input, text=captcha_code)

    def _save_captcha_img(self) -> None:
        captcha_img = self.wait_element_visible(xpath=web_element.captcha_img)
        captcha_img.screenshot("captcha.png")

    def _check_captcha_result(self) -> bool:
        if self.check_element_is_exist(web_element.train_query_data_view_panel):
            return True
        if self.check_element_is_exist(web_element.captcha_failed):
            return False
        return False

    def _parser_train_info(self, index: int) -> TrainInfo:
        xpath = (
            f"{web_element.train_result}//span[{index}]/label{web_element.train_info}"
        )
        info = self.wait_element_visible(xpath=xpath)
        return TrainInfo(
            depart_time=info.get_attribute("querydeparture"),
            arrival_time=info.get_attribute("queryarrival"),
            duration=info.get_attribute("queryestimatedtime"),
            train_code=info.get_attribute("querycode"),
            radio_box=info,
        )

    def _show_train_info(self, train_info: dict[int, TrainInfo]) -> None:
        for index, train in train_info.items():
            print(
                f"{index:>3}. - {train.train_code:>4} 車次， 行駛時間: {train.duration}， {train.depart_time} -> {train.arrival_time}"
            )

    def _confirm_ticket(self) -> None:
        self.wait_element_visible_and_click(xpath=web_element.confirm_ticket_btn)

    def _click_agree_rules_checkbox(self) -> None:
        self.wait_element_visible_and_click(xpath=web_element.agree_rules_checkbox)

    def _click_finish_button(self) -> None:
        self.wait_element_visible_and_click(xpath=web_element.finish_booking)

    def _confirm_booking_results(self):
        try:
            result = self.wait_element_visible(xpath=web_element.ticket_summary)
            result.screenshot("result.png")
            print("\n訂票完成! 請在期限內繳款\n")
        except:
            self.driver.get_screenshot_as_png()
            print("\n訂票失敗!\n")
