from thsr_booker.code.thsr_booker import (
    THSR_BOOKER,
    setup_user_info,
    setup_user_requirements,
)
from thsr_booker.config.models import UserInfo, UserRequirements
from thsr_booker.code.util import inatall_driver
from thsr_booker.config import constants

USER_INFO: UserInfo = setup_user_info()
USER_REQUIREMENTS: UserRequirements = setup_user_requirements()


def main():
    thsr_booker = THSR_BOOKER(driver_arg=constants.CHROME_DRIVER_ARGS)
    thsr_booker.go_to_homw_page()
    thsr_booker.select_requirements_info(USER_REQUIREMENTS)
    thsr_booker.check_captcha()
    thsr_booker.select_ticket(thsr_booker.get_train_info())
    thsr_booker.show_ticket_info()
    thsr_booker.input_user_info(USER_INFO)
    thsr_booker.submit_booking()
    thsr_booker.close()


if __name__ == "__main__":
    inatall_driver()
    main()
