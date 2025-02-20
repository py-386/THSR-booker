import ddddocr



ocr = ddddocr.DdddOcr()



def get_captcha_code():
    image = open('captcha.png', "rb").read() # 'rb'是以二進位讀取進來
    result = ocr.classification(image)
    print("Get captcha code : ", result)
    return result
