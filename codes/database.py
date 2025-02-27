import mysql.connector



#將資訊存入資料庫
def data_to_database(user_info):
    try:
        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="my_database"
    )

        cursor = conn.cursor()
        sql = "SELECT id from users WHERE phone_number = %s"
        cursor.execute(sql, (user_info['user_phone_number'],))
        user= cursor.fetchone()

        if user:
            user_id = user[0]
            print("此電話號碼已有訂購紀錄")
        else:
            user_email = user_info.get('user_email', None) #可有可無的資訊先抓

            sql = "INSERT INTO users (name, email, phone_number) VALUES (%s, %s, %s)"
            cursor.execute(sql, (
                        user_info['user_name'],
                        user_email,
                        user_info['user_phone_number'])
                        )
            
            user_id = cursor.lastrowid
            #當你執行 INSERT INTO 語句時，資料庫會自動產生一個 id（如果 id 是 AUTO_INCREMENT），
            # 這時候 cursor.lastrowid 會 回傳剛剛插入的那一筆資料的 id。
            conn.commit()
            print("此電話號碼無紀錄..")
            print("您的電話號碼已存檔")


        sql = "INSERT INTO tickets (user_id, start_date, start_time, start_station, dest_station, train_code, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
                            user_id, user_info['出發日期_database'], user_info['出發時辰'], 
                            user_info['出發站'], user_info['到達站'],
                            user_info['train_code'], user_info['price']))
        conn.commit()
        print("已儲存訂票資訊")

    except Exception as e:
        print(f"\n資料庫錯誤: {e}\n")

    finally:
        cursor.close()
        conn.close()
