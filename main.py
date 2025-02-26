from codes.thsr_booker_steps import (
                            create_driver,
                            booking_with_info,
                            select_train_and_submit_booking)
from codes.booking_info_extraction_flow import (
                                        ask_booking_information,
                                        ask_missing_information,
                                        convert_date_to_thsr_format)



def main():
    create_driver()
    # step 1
    booking_info = ask_booking_information()
    # step 2
    booking_info = ask_missing_information(booking_info)
    # step 3 調整日期設以便爬蟲使用 ex: '2025/02/25' -> '二月 25, 2025'
    booking_info = convert_date_to_thsr_format(booking_info)    
    # step 4
    trains_info = booking_with_info(
                start_station=booking_info['出發站'],
                dest_station=booking_info['到達站'],
                start_date=booking_info['出發日期'],
                start_time=booking_info['出發時辰'])
    # step 5
    select_train_and_submit_booking(trains_info)


if __name__ == "__main__":
    main()
