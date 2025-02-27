
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import (
    InvalidSignatureError)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent)

import os
from datetime import date

# my tools
from codes.tools.chatgpt_sample import chat_with_chatgpt
from codes.booking_info_extraction_flow import (
                                extract_dict_from_string,
                                convert_date_to_thsr_format)

from codes.thsr_booker_steps import (
                    create_driver,
                    driver_quit,
                    booking_with_info,
                    select_train_and_submit_booking)



app = Flask(__name__)

# 從環境變數裏頭取得access token與channel secret
configuration = Configuration(
    access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

user_data = {}

today = date.today().strftime("%Y/%m/%d") # 今天日期
standard_format = {
    '出發站': '出發站名',
    '到達站': '到達站名',
    '出發日期': 'YYYY/MM/DD',
    '出發時辰': 'H:S'
}

def update_user_data(user_id, **info_dict):
    if user_id not in user_data:
        user_data[user_id] = info_dict
    else:
        info_has_value = {
            slot_name: slot_value
            for slot_name, slot_value in info_dict.items() if slot_value
        }
        user_data[user_id].update(info_has_value)

def get_user_data(user_id):
    return user_data.get(user_id, {})

@app.route("/callback", methods=['POST']) #POST 是帶加密帶訊息的傳遞方式
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text
    user_data = get_user_data(user_id)
    necessary_slots = ['出發站', '到達站','出發日期', '出發時辰']

    if user_data.get("intent", "") != "訂高鐵" and user_message == "訂高鐵":
        update_user_data(user_id, intent="訂高鐵") # 更新意圖為 "訂高鐵"
        # 問第一個問題: "請輸入你的高鐵訂位資訊..."
        bot_response = "請輸入您的高鐵訂位資訊，包含: 出發站、到達站、出發日期、出發時辰: "

    elif user_message == "取消":
        update_user_data(user_id, intent = "")
        
        bot_response = "流程取消"
        

    elif user_data.get("intent") == "訂高鐵": #意圖判斷
        #上一輪的資訊狀態
        unfilled_slots = [
            key for key in necessary_slots if not user_data.get(key)] # 未填的資訊
        
        # user message information extraction
        system_prompt = f"""
            我想要從回話取得訂票資訊，包含：{"、".join(unfilled_slots)}。
                            並與{user_data}合併，今天是{today}，若有明天或後天的指令請幫我推算日期，
                            請把資料整理成python dictionary格式，例如: {standard_format}，
                            不知道就填空字串，且回傳不包含其他內容。
            """
        booking_info = extract_dict_from_string(chat_with_chatgpt(user_message, system_prompt))
        update_user_data(user_id, **booking_info)

        # 判斷已填的資訊
        user_data = get_user_data(user_id) # 重新讀取一次user_data

        filled_slots = [
            key for key in necessary_slots if user_data.get(key)] # 已填的資訊
        unfilled_slots = [
            key for key in necessary_slots if not user_data.get(key)] # 未填的資訊

        app.logger.info(f"filled_slots: {filled_slots}")
        app.logger.info(f"unfilled_slots: {unfilled_slots}")

        if len(unfilled_slots) == 0: # 全部填完
            #依照訊息送出訂位，直到選車為止
            user_data = convert_date_to_thsr_format(user_data)
            create_driver() #目前只支援單人，driver是global的
            trains_info = booking_with_info(
                                start_station=user_data['出發站'],
                                dest_station=user_data['到達站'],
                                start_time=user_data['出發時辰'],
                                start_date=user_data['出發日期'])

            # show train info and choose train
            train_message = ""
            for counter, train in enumerate(trains_info):
                train_message += f"""\n{counter:>3}. - {train['train_code']:>4} 車次，
行駛時間: {train['duration']}分，\n {train['depart_time']} -> {train['arrival_time']}\n"""
                
            bot_response = f"已為您找到以下車次，請依照編號輸入0~9: \n{train_message}"

            # 更改 intent 為 "選高鐵"，並更新車次查詢結果
            update_user_data(user_id, intent="選高鐵", trains_info=trains_info)

        else: # 沒有全部填完
            # 問缺少的資訊
            bot_response = f"請補充你的高鐵訂位資訊，包含：{', '.join(unfilled_slots)}: "


    elif user_data.get("intent") == "選高鐵":
        try:
            # 依照使用者選擇的車次，進行訂位
            which_train = int(user_message)
            trains_info = user_data.get("trains_info")
            select_train_and_submit_booking(trains_info, which_train)
            bot_response = "訂票完成！請儘速繳款取票！"
        except Exception as e:
            # 如果無法從使用者回覆取得數字
            app.logger.error(e)
            bot_response = "請輸入0~9的數字"

    else:
        bot_response = chat_with_chatgpt(
            user_message=user_message,
            system_prompt="回應二十字以內，並在換行後提示一句話: (請輸入'訂高鐵'開始訂票流程。)，並在換一行後提示: (輸入'取消'結束流程並重新開始。)"
        )
        
    response_messages = [TextMessage(text=bot_response)]

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=response_messages
            )
        )


if __name__ == "__main__":
    app.run(debug=True, port=5001)