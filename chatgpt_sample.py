from openai import OpenAI

"""    
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # model name
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."  # 給他的人設
            },
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    )
"""

client = OpenAI() #跟openAI 溝通的物件，如果沒有給key的話會自動去環境變數裡抓看有沒有


#chat.completions 克漏字模型

def chat_with_chatgpt(user_message, system_prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # model name
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    print(completion.choices[0].message.content) #直接找到字串
    return completion.choices[0].message.content 




# print(completion) #這是這個服務給你的結果
# print(completion.choices[0].message) #預設有多個答案，但通常是一個，都擷取inx[0]
# print(completion.choices[0].message.content) #直接找到字串


# if __name__ == "__main__":
#     chat_with_chatgpt(
#         user_message="我要一杯珍珠奶茶微糖微冰",
#         system_prompt="你是一位飲料店的店員，有人向你點餐"
#     )
