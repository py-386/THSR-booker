from codes.tools.chatgpt_sample import chat_with_chatgpt
import json
from datetime import date
import re

today = date.today().strftime("%Y/%m/%d") # 今天日期
standard_format = {
    '出發站': '出發站名',
    '到達站': '到達站名',
    '出發日期': 'YYYY/MM/DD',
    '出發時辰': 'H:S'
}

def extract_dict_from_string(input_string):
    # 定義正則表達式來匹配字典內容
    pattern = r"\{\s*'[^']*':\s*'[^']*'(?:,\s*'[^']*':\s*'[^']*')*\s*\}"
    match = re.search(pattern, input_string)

    if match:
        dict_string = match.group(0)
        # 將單引號替換為雙引號以便於 json.loads 解析
        dict_string = dict_string.replace("'", "\"")
        print("After regular expression ....: ", dict_string)
        return json.loads(dict_string)
    else:
        raise ValueError("Information Extraction Failed.")

def ask_booking_information():
    print("Ask booking infomation.")

    user_response = input("請輸入你的高鐵訂位資訊，包含: 出發站,抵達站,出發日期,出發時辰。: ")

    system_prompt = f"""
            我想要從回話取得訂票資訊，包含：出發站、到達站、出發日期、出發時辰。
            今天是 {today}，若有明天或後天的指令請幫我推算日期，請把資料整理成python dictionary格式，例如：{standard_format}，
            不知道就填空字串，且回傳不包含其他內容。
            """
    booking_info = extract_dict_from_string(chat_with_chatgpt(user_response, system_prompt)) #正規表示式 處理結果
    return booking_info

def ask_missing_information(booking_info):
    print("Ask missing infomation.")
    
    missing_slots = [key for key, value in booking_info.items() if not value]
    if not missing_slots:
        print("All slots are filled.")
        return booking_info
    else:
        user_response = input(f"請補充您的高鐵訂位資訊，包含: {", ".join(missing_slots)}。: ")

        system_prompt = f"""我想要從回話取的訂票資訊，包含{", ".join(missing_slots)}，
                            並與{booking_info}合併，今天是{today}，若有明天或後天的指令請幫我推算日期，
                            請把資料整理成python dictionary格式，例如: {standard_format}，
                            不知道就填空字串，且回傳不包含其他內容。"""

        booking_info = extract_dict_from_string(chat_with_chatgpt(user_response, system_prompt))
        return booking_info

def convert_date_to_thsr_format(booking_info):
    map_number_to_chinese_word={
        "01": "一月", "02": "二月", "03": "三月",
        "04": "四月", "05": "五月", "06": "六月",
        "07": "七月", "08": "八月", "09": "九月",
        "10": "十月", "11": "十一月", "12": "十二月",
    }
    Year, Month, Day = booking_info['出發日期'].split('/')
    booking_info['出發日期'] = f"{map_number_to_chinese_word[Month]} {Day}, {Year}"
    print(f"格式轉換後......: {booking_info}")
    return booking_info



# if __name__ == "__main__":
#     # step 1
#     booking_info = ask_booking_information()

#     # step 2
#     booking_info = ask_missing_information(booking_info)
    
#     # step 3 調整日期設以便爬蟲使用 ex: '2025/02/25' -> '二月 25, 2025'
#     booking_info = convert_date_to_thsr_format(booking_info)

